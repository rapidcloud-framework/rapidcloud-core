import os
import sys
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import time
import contextlib
import logging
import awswrangler as wr
import pandas as pd
import numpy as np

#Test Mode
if sys.argv[1] != 'test_mode':
    from awsglue.utils import getResolvedOptions

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-7s %(name)-39s:  %(message)s')
logger = logging.getLogger("transform")

result_json = {
    "log": []
}

# zip code column names for each dataset
zip_col_by_dataset = {
    "ems_narcan": [
        "p_u_zip"
    ],
    "ems_suspected_overdoses": [
        "p_u_zip"
    ],
    "ems_suspected_overdoses_with_narcan": [
        "p_u_zip"
    ],
    "floridahealth_rx_drug_monitoring_program": [
        "patient_postal_code",
        "prescriber_postal_code",
        "dispensary_postal_code"
    ],
    "me_drug_related_deaths": [
        "death_zip",
        "injury_zip"
    ],
    "me_suicides": [
        "death_zip",
        "injury_zip"
    ],
    "jail_admitted": [
        "zip_code"
    ],
    "jail_released": [
        "zip_code"
    ],
    "sip_otf": [
        "death_zip",
        "injury_zip" 
    ]
}

# include cols by dataset
col_mappings_by_dataset = {
    "census": {
        "ZCTA": "Zip",
        "DP05_0001E": "Total population",
        "DP05_0002E": "Male population",
        "DP05_0003E": "Female population",
        "DP05_0005E": "Less than 5 years old population",
        "DP05_0006E": "5-9 years old population",
        "DP05_0007E": "10-14 years old population",
        "DP05_0008E": "15-19 years old population",
        "DP05_0009E": "20-24 years old population",
        "DP05_0010E": "25-34 years old population",
        "DP05_0011E": "35-44 years old population",
        "DP05_0012E": "45-54 years old population",
        "DP05_0013E": "55-59 years old population",
        "DP05_0014E": "60-64 years old population",
        "DP05_0015E": "65-74 years old population",
        "DP05_0016E": "75-84 years old population",
        "DP05_0017E": "Greater than 85 years old population",
        "DP05_0018E": "median age",
        "DP05_0037E": "White population",
        "DP05_0038E": "African-American population",
        "DP05_0039E": "American Indian or Alaska Native population",
        "DP05_0044E": "Asian population",
        "DP05_0052E": "Native Hawaiian and Pacific Islander population",
        "DP05_0057E": "Other race population",
        "DP05_0058E": "Two or more races population",
        "DP05_0070E": "Hispanic or Latino population"
    }
}


glue_client = boto3.client('glue')
sns_client = boto3.client('sns')
dynamodb_resource = boto3.resource('dynamodb')


def df_info(df, msg, count=5):
    msg = f"{msg}: {len(df.index)}"
    logger.info(msg)
    logger.info(df.iloc[0:count])
    result_json['log'].append(msg)


def send_sns_notification(status):
    if sys.argv[1] != 'test_mode':
        for topic in sns_client.list_topics()['Topics']:
            if f"{env}-transformations" in topic['TopicArn']:
                result_json['status'] = status
                sns_client.publish(
                    TopicArn=topic['TopicArn'],
                    Subject=f"{status} - {job_name} ({dataset})",    
                    Message=json.dumps(result_json, indent=2, default=str)    
                )


def query(table, key_attr, key_value):
    logger.info(f"getting {key_attr}={key_value} from {table}")
    return dynamodb_resource.Table(table).query(
        KeyConditionExpression=Key(key_attr).eq(key_value)
    )['Items']


def put_item(table, item):
    logger.info(f"\n\nsaving {table} metadata:\n" + json.dumps(item, indent=2, default=str))
    response = dynamodb_resource.Table(table).put_item(Item=item)
    logger.info(f"\n\nresponse:\n" + json.dumps(response, indent=2, default=str))


def get_transform_log(fqn):
    items = query("transform_log", "fqn", fqn)
    logger.info(json.dumps(items, indent=2, default=str))
    if items:
        return items[0]
    return None


def get_rds_conn():
    conn_name = glue_client.get_job(JobName=f"{env}_{job_name}")['Job']['Connections']['Connections'][0]
    logger.info(f"conn_name={conn_name}")
    return wr.postgresql.connect(conn_name)


def start_transform(env, dataset_name, job_name, job_arguments):
    fqn = f"{env}_{dataset_name}_{time.time() * 1000}"
    item = {
        "fqn": fqn,
        "profile": env,
        "dataset_name": dataset_name,
        "job_name": job_name,
        "job_arguments": job_arguments,
        "status": "started",
        "update_timestamp": str(datetime.datetime.now())            
    }
    put_item("transform_log", item)  
    return item


def update_transform(fqn, status, destination=[], error_msg=None):
    items = query("transform_log", "fqn", fqn)
    if items:
        item = items[0]
        item['status'] = status
        item['update_timestamp'] = str(datetime.datetime.now())
        item['destination'] = destination
        if error_msg is not None:
            item['error_msg'] = error_msg
    put_item("transform_log", item)  
    return item


def get_raw_query(match_status_clause=None):
    raw_query = f"SELECT * FROM {dataset}"
    
    if cdc_type in ["delta", "cumulative_year", "cumulative_month", "cumulative_day"]:
        if src_file_key and src_file_key != "tbd":
            raw_query = f"{raw_query} WHERE src_file_key = '{src_file_key}'"
            if src_file_batch_no and src_file_batch_no != "tbd":
                raw_query = raw_query + f" AND batch_no = {src_file_batch_no}"
    
    if match_status_clause:
        if 'WHERE' in raw_query:
            raw_query = f"{raw_query} AND {match_status_clause}"
        else:
            raw_query = f"{raw_query} WHERE {match_status_clause}"

    logger.info(raw_query)
    return raw_query


#
# Starts here
#

try:
    start = time.time()
    if sys.argv[1] != 'test_mode':
        logger.info(f"getting args from getResolvedOptions(..)")
        args = getResolvedOptions(sys.argv,[
                "job_name",
                "env",
                "region",
                "dataset",
                "source_bucket",
                "target_bucket",
                "source_glue_database",
                "target_glue_database",
                "base_datasets",
                "transform_name",
                "extra-arg-1"
                "extra-arg-2",
                # "extra-arg-3"
            ]
        )
    else:
        logger.info(f"getting args from command line args (test mode)")
        args = {
            "job_name": "transform",
            "env": sys.argv[2],
            "region": sys.argv[3],
            "dataset": sys.argv[4],
            "source_bucket": sys.argv[5],
            "target_bucket": sys.argv[6],
            "source_glue_database": sys.argv[7],
            "target_glue_database": sys.argv[8],
            "base_datasets": sys.argv[9],
            "transform_name": sys.argv[10],
            "extra_arg_1": sys.argv[11],  # src_file_key
            "extra_arg_2": sys.argv[12],  # batch_no (src_file_key split into multiple files)
            # "extra_arg_3": sys.argv[13] # datalake_day
        }

    result_json['args'] = args
        
    job_name = args['job_name']
    env = args['env']
    region = args['region']
    dataset = args['dataset']
    source_bucket = args['source_bucket']
    target_bucket = args['target_bucket']
    source_glue_database = args['source_glue_database']
    target_glue_database = args['target_glue_database']
    base_datasets = args['base_datasets']
    transform_name = args['transform_name']
    src_file_key = args['extra_arg_1']
    src_file_batch_no = args['extra_arg_2']
    # datalake_day = args['extra_arg_3']

    athena_query_results = f"s3://{env.replace('_','-')}-query-results-bucket/output/"
    for arg, value in args.items():
        logger.info(f"{arg}={value}")

    # transform_log
    transform_fqn = start_transform(env, dataset, job_name, args)['fqn']

    # transform metadata
    transform = query("transformation", "fqn", transform_name)[0]    
    logger.info("\n\ntransformation metadata:\n" + json.dumps(transform, indent=2, default=str))

    # dataset info
    dataset_semi_structured = query("dataset_semi_structured", "fqn", f"{env}_{dataset}")[0]   
    cdc_type = dataset_semi_structured['cdc_type']
    logger.info("\n\n" + json.dumps(dataset_semi_structured, indent=2, default=str))


    # -------------------------------------------------------------------
    # Start transformation logic
    # -------------------------------------------------------------------

    #
    # PII Matching is enabled
    #

    if dataset_semi_structured['enable_enrich']:
        logger.info(f"{dataset}: PII Matching is enabled")

        #
        # This job is triggered by CDC process while passing datalake_* arguments
        #
        if src_file_key and src_file_key != "tbd":

            # 
            # Read from s3 where match_status in ('New','Exact')    
            # 
            raw_query = get_raw_query("match_status in ('New','Exact')")
            final_df = wr.athena.read_sql_query(
                sql=raw_query, 
                database=source_glue_database, 
                ctas_approach=False, 
                s3_output=athena_query_results,
                keep_files=False)
            df_info(final_df, "final_df:")
    
        #
        # This job is triggered by PII Matching app (when proposed match queue is emptied)
        #
        else:

            # 
            # Read from s3 where match_status = 'Proposed'
            # 
            raw_query = get_raw_query("match_status = 'Proposed'")
            proposed_df = wr.athena.read_sql_query(
                sql=raw_query, 
                database=source_glue_database, 
                ctas_approach=False, 
                s3_output=athena_query_results,
                keep_files=False)
            proposed_df.person_id = proposed_df.person_id.astype(str)
            proposed_df = proposed_df.rename(columns={"person_id": "key"}).set_index('key')
            df_info(proposed_df, "proposed_df:")


            # 
            # Read from RDS/proposed_match with status in: (1,2,3)
            #   0,1,2,3,4 -> Pending, Accepted, Manually Matched, New Person, Rejected  
            # 
            accepted_df = None
            if len(proposed_df.index) > 0:
                raw_query = f"SELECT id, person_id FROM opioids.proposed_match WHERE LOWER(file_type) = '{dataset}' and status in (1,2,3)"
                logger.info(raw_query)
                accepted_df = wr.db.read_sql_query(
                    sql=raw_query,
                    con=get_rds_conn()
                )
                accepted_df.id = accepted_df.id.astype(str)
                accepted_df = accepted_df.rename(columns={"id": "key"}).set_index('key')
                df_info(accepted_df, "accepted_df:")


            # 
            # merge proposed_df and accepted_df
            # 
            final_df = None
            if len(proposed_df.index) > 0 and accepted_df is not None and len(accepted_df.index) > 0:
                logger.info(proposed_df.dtypes)
                logger.info(accepted_df.dtypes)
                final_df = proposed_df.merge(accepted_df, how="inner", on='key')
                df_info(final_df, "final_df:")


    #
    # PII Matching is disabled
    #

    else:
        logger.info(f"{dataset}: PII Matching is disabled")
        raw_query = get_raw_query()
        final_df = wr.athena.read_sql_query(
            sql=raw_query, 
            database=source_glue_database, 
            ctas_approach=False, 
            s3_output=athena_query_results,
            keep_files=False)
        # final_df.info(verbose=True)
        df_info(final_df, "Before transformation")
    
    #
    # Get city name from zip code
    #

    zip_codes = wr.s3.read_csv(f"s3://{source_bucket}/util/zip_code_database.csv", sep=",", skip_blank_lines=True)[["zip", "primary_city"]]
    # zip_codes = wr.s3.read_excel(f"s3://{source_bucket}/util/zip_code_database.xls", sheet_name="data")[["zip", "primary_city"]]
    zip_codes.rename(columns={"zip": "x_zip", "primary_city": "x_city"}, inplace=True)
    zip_codes["x_zip"] = zip_codes["x_zip"].astype(str)
    df_info(zip_codes, "zip_codes")

    if dataset in zip_col_by_dataset:
        for zip_col in zip_col_by_dataset[dataset]:
            final_df[f'{zip_col}_5'] = final_df[zip_col].astype(str).str[:5]
            final_df = pd.merge(final_df, zip_codes, how="left", left_on=f'{zip_col}_5', right_on='x_zip')
            final_df.drop(columns=[f'{zip_col}_5','x_zip'], inplace=True)
            final_df.rename(columns={"x_city": f"{zip_col}_city"}, inplace=True)

    df_info(final_df, "df_mapped")
    

    #
    # Filter and map columns
    #
    if dataset in col_mappings_by_dataset:
        cols = []
        for orig_col, new_col in col_mappings_by_dataset[dataset].items():
            final_df.rename(columns={orig_col.lower(): new_col}, inplace=True)
            cols.append(new_col)
        final_df = final_df[cols]


    # Write results to analysis bucket
    destination = f"s3://{target_bucket}/transformations/{dataset}/"
    if cdc_type == 'cumulative' or not src_file_key:
        mode = "overwrite"
    else:
        mode = "append"

    final_df['transform_fqn'] = transform_fqn
    wr.s3.to_parquet(
        df=final_df,
        path=f"s3://{target_bucket}/transformations/{dataset}/",
        dataset=True,
        partition_cols=['transform_fqn'],
        mode=mode
    )
    result_json['count'] = len(final_df.index)
    result_json['transform_fqn'] = transform_fqn
    
    #
    # End transformation
    #

    result_json['duration'] = time.time() - start
    logger.info(f"The Glue Job: {job_name} has successfully completed")
    send_sns_notification("SUCCESS")

    update_transform(transform_fqn, "completed", [destination])

except Exception as e:
    exception_msg = f"Exception occurred inside this glue etl ==> {job_name} with this exception ==> {e}"
    logger.log("ERROR", exception_msg)
    send_sns_notification("FAILED")

    # transform_log
    update_transform(transform_fqn, "failed", error_msg=[exception_msg])

    raise Exception(exception_msg)
