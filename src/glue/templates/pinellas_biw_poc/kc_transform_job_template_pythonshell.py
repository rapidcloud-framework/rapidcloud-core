import os
import sys
import json
import boto3
import datetime
import contextlib
import logging
import awswrangler as wr
import pandas as pd
# from awsglue.utils import getResolvedOptions

logging.basicConfig()
logger = logging.getLogger("transform")
logger.setLevel(logging.INFO)

def df_info(df, msg, count=3):
    logger.info(f"\n{msg}: {len(df.index)}")
    logger.info(df.iloc[0:count])

try:
    # args = getResolvedOptions(sys.argv,[
    #         "job_name",
    #         "env",
    #         "region",
    #         "dataset",
    #         "source_bucket",
    #         "target_bucket",
    #         "source_glue_database",
    #         "target_glue_database",
    #         "base_datasets"
    #     ]
    # )

    args = {
        "job_name": "test",
        "env": "pinellas_biw_poc",
        "region": "us-gov-west-1",
        "dataset": "alife",
        "source_bucket": "pinellas-biw-poc-raw",
        "target_bucket": "pinellas-biw-poc-analysis",
        "source_glue_database": "pinellas_biw_poc_rawdb",
        "target_glue_database": "pinellas_biw_poc_analysisdb",
        "base_datasets": "alife"
    }

    job_name = args['job_name']
    env = args['env']
    region = args['region']
    dataset = args['dataset']
    source_bucket = args['source_bucket']
    target_bucket = args['target_bucket']
    source_glue_database = args['source_glue_database']
    target_glue_database = args['target_glue_database']
    base_datasets = args['base_datasets']

    logger.info(f"job_name: {job_name}")
    logger.info(f"region: {region}")
    logger.info(f"dataset: {dataset}")
    logger.info(f"source_location: {source_bucket}")
    logger.info(f"target_location: {target_bucket}")
    logger.info(f"source_glue_database: {source_glue_database}")
    logger.info(f"target_glue_database: {target_glue_database}")
    logger.info(f"base_datasets: {base_datasets}")

    # Start transformation logic

    # Read from s3 where person_id is present and match_status = 'Exact'
    
    # query = f"SELECT * FROM {dataset} WHERE match_status = 'Exact'"
    # query = f"SELECT * FROM {dataset} where ssn != 'unobtainable' LIMIT 10"
    # exact_df = wr.athena.read_sql_query(
    #     sql=query, 
    #     database=source_glue_database, 
    #     ctas_approach=False, 
    #     s3_output=f"s3://{env.replace('_','-')}-query-results-bucket/output/",
    #     keep_files=False)
    # df_info(exact_df, "exact_df: Before transformation")
    

    # Read from s3 where person_id is present and match_status = 'Proposed'
    
    # query = f"SELECT * FROM {dataset} WHERE match_status = 'Proposed'"
    # query = f"SELECT * FROM {dataset} where ssn = 'unobtainable' LIMIT 10"
    # proposed_df = wr.athena.read_sql_query(
    #     sql=query, 
    #     database=source_glue_database, 
    #     ctas_approach=False, 
    #     s3_output=f"s3://{env.replace('_','-')}-query-results-bucket/output/",
    #     keep_files=False)
    # df_info(proposed_df, "proposed_df: Before transformation")


    # Read from RDS/proposed_match with status in ['accepted', 'manually_matched', 'new_person_created']
    # 0,1,2,3 -> Pending, Accepted, Manually Matched, New Person, Rejected
    
    con=wr.catalog.get_engine(connection=f"{env}_human_services_bi_rds_postgresql_instance")
    print(con)
    accepted_df = wr.db.read_sql_query(
        # sql="SELECT * FROM human_services.proposed_match WHERE match_status in (1,2,3)",
        sql="SELECT * FROM human_services.proposed_match",
        con=con
    )
    df_info(accepted_df, "accepted_df: Before transformation")


    # join proposed_df and accepted_df
    # TODO
    proposed_and_accepted_df = proposed_df

    # Write results to analysis bucket
    # destination = f"s3://{target_bucket}/transformations/{dataset}/"
    # wr.s3.to_parquet(
    #     df=df,
    #     path=f"s3://{target_bucket}/transformations/{dataset}/",
    #     dataset=True,
    #     mode="overwrite"
    # )
    # End transformation logic

    logger.info(f"The Glue Job: {job_name} has successfully completed")

except Exception as e:
    exception_msg = f"Exception occurred inside this glue etl ==> {job_name} with this exception ==> {e}"
    logger.log("ERROR", exception_msg)
    raise Exception(exception_msg)

