import os
import sys
import json
import boto3
import datetime
import time
import contextlib
import logging
import awswrangler as wr
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr
# from awsglue.utils import getResolvedOptions

logging.basicConfig()
logger = logging.getLogger("publish")
logger.setLevel(logging.INFO)

result_json = {
    "log": []
}

glue_client = boto3.client('glue')
sns_client = boto3.client('sns')
dynamo_resource = boto3.resource('dynamodb')


def df_info(df, msg, count=3):
    msg = f"{msg}: {len(df.index)}"
    log(msg)
    logger.info(df.iloc[0:count])
    result_json['log'].append(msg)


def log(msg):
    logger.info(msg)
    result_json['log'].append(f"{datetime.datetime.now()}: {msg}")


def json_converter(obj):
    return str(obj)


def send_sns_notification(status):
    for topic in sns_client.list_topics()['Topics']:
        if f"{args['env']}_general_notifications" in topic['TopicArn']:
            sns_client.publish(
                TopicArn=topic['TopicArn'],
                Subject=f"{status} - {args['job_name']} ({args['dataset']})",    
                Message=json.dumps(result_json, indent=2, default=json_converter)    
            )


def get_table_info():
    fqn = f"{args['env']}_{args['db_type']}_{args['db_engine']}_{args['db_name']}_{args['table']}"
    log(f"table fqn: {fqn}")
    return dynamo_resource.Table('publishing').query(
        KeyConditionExpression=Key('fqn').eq(fqn)
    )['Items'][0]


def get_conn():
    conn_name = glue_client.get_job(
        JobName=args['job_name']
    )['Job']['Connections']['Connections'][0]
    return wr.catalog.get_engine(connection=conn_name)


try:
    start = time.time()

    default_args = {
        "job_name": sys.argv[1],
        "env": "pinellas_biw_poc",
        "dataset": sys.argv[2],
        "db_type": sys.argv[3],
        "db_engine": sys.argv[4],
        "db_name": sys.argv[5],
        "db_schema": sys.argv[6],
        "table": sys.argv[7],
        "target_replace_key": sys.argv[8],
        "source_bucket": "pinellas-biw-poc-analysis"
    }

    logger.info(default_args.keys())

    # args = getResolvedOptions(sys.argv, default_args.keys())
    args = default_args

    result_json['args'] = args
    logger.info(json.dumps(args, indent=2))

    athena_query_results = f"s3://{args['env'].replace('_','-')}-query-results-bucket/output/"

    # 
    # Read dataset from s3   
    # 
    dataset_df = wr.s3.read_parquet(path=f"s3://{args['source_bucket']}/transformations/{args['dataset']}/")
    df_info(dataset_df, "dataset_df:")

    # 
    # Create temp table in rds postgres   
    # 
    temp_table = f"{args['dataset']}_{time.time()}".replace('.','_')
    ddl = pd.io.sql.get_schema(dataset_df.reset_index(), temp_table)
    logger.info(ddl)

    # map postgres data types
    cols = dataset_df.columns
    dtypes = dataset_df.dtypes
    for i in range(len(cols)):
        if dtypes[i] == 'object':
            logger.info(f"{cols[i]} from {dtypes[i]} to str")
            dataset_df[cols[i]] = dataset_df[cols[i]].astype('str') 

    # TODO start custom code if needed
    # ...

    # TODO /end custom code


    conn = get_conn()
    logger.info(conn)
    table_info = get_table_info()
    logger.info(json.dumps(table_info, indent=2))
    result = wr.db.to_sql(df=dataset_df, con=conn, name=temp_table, schema=args['db_schema'])
    logger.info(result)

    # 
    # Delete old data from table
    # 
    table_name = f"{args['db_schema']}.{args['table']}"
    with get_conn().connect() as conn:

        if args['target_replace_key'].lower() != 'n/a':
            # delete for specific target replace key (e.g. type, category, etc)
            sql = f"DELETE FROM {table_name} WHERE lower({args['target_replace_key']}) = '{args['dataset']}'"
        else:
            # truncate table 
            sql = f"TRUNCATE TABLE {table_name}"

        result = conn.execute(sql)
        logger.info(result)    
    log("deleted old data")

       
    # 
    # Copy data from temp table
    # 
    # table_name = args['dataset'] # TODO testing
    sql = f"INSERT INTO {args['db_schema']}.{table_name} SELECT * FROM {args['db_schema']}.{temp_table}"
    with get_conn().connect() as conn:
        result = conn.execute(sql)
        logger.info(result) 
        log("copied new data from temp table")

    # 
    # Delete temp table
    # 
    sql = f"DROP TABLE {args['db_schema']}.{temp_table}"
    with get_conn().connect() as conn:
        result = conn.execute(sql)
        logger.info(result) 
        log("droped temp table")


    logger.info(f"The Glue Job: {args['job_name']} has successfully completed")
    send_sns_notification("SUCCESS")

except Exception as e:
    exception_msg = f"Exception occurred inside this glue etl ==> {args['job_name']} with this exception ==> {e}"
    logger.log("ERROR", exception_msg)
    send_sns_notification("FAILED")
    raise Exception(exception_msg)
