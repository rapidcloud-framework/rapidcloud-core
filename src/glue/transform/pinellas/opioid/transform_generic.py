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
from data_scripts.kc_quicksight import QuicksightIntegration

if sys.argv[1] != 'test_mode':
    from awsglue.utils import getResolvedOptions

logging.basicConfig()
logger = logging.getLogger("transform")
logger.setLevel(logging.INFO)

result_json = {
    "log": []
}

sns_client = boto3.client('sns')
dynamodb_resource = boto3.resource('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')
quicksight_client = boto3.client('quicksight')

def df_info(df, msg, count=3):
    msg = f"{msg}: {len(df.index)}"
    logger.info(msg)
    logger.info(df.iloc[0:count])
    result_json['log'].append(msg)

def json_converter(obj):
    return str(obj)

def send_sns_notification(status):
    for topic in sns_client.list_topics()['Topics']:
        if f"{env}_transformations" in topic['TopicArn']:
            result_json['status'] = status
            sns_client.publish(
                TopicArn=topic['TopicArn'],
                Subject=f"{status} - {job_name} ({dataset})",    
                Message=json.dumps(result_json, indent=2, default=json_converter)    
            )

def query(table, key_attr, key_value):
    return dynamodb_resource.Table(table).query(
        KeyConditionExpression=Key(key_attr).eq(key_value)
    )['Items']

def put_item(table, item):
    response = dynamodb_resource.Table(table).put_item(Item=item)
    logger.info(json.dumps(item, indent=2))
    logger.info(json.dumps(response, indent=2))

def get_transform_log(fqn):
    items = query("transform_log", "fqn", fqn)
    logger.info(json.dumps(items, indent=2))
    if items:
        return items[0]
    return None


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
                "base_datasets"
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
            "base_datasets": sys.argv[9]
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

    logger.info(f"job_name: {job_name}")
    logger.info(f"region: {region}")
    logger.info(f"dataset: {dataset}")
    logger.info(f"source_location: {source_bucket}")
    logger.info(f"target_location: {target_bucket}")
    logger.info(f"source_glue_database: {source_glue_database}")
    logger.info(f"target_glue_database: {target_glue_database}")
    logger.info(f"base_datasets: {base_datasets}")

    # transform metadata
    profile = query("profile", "name", env)
    logger.info(json.dumps(profile, indent=2))
    transform = query("transform", "fqn", f"{profile['client']}_{profile['env']}_{dataset}")    
    logger.info(json.dumps(transform, indent=2))

    # transform_log
    transform_fqn = start_transform(env, dataset, job_name, args)['fqn']

    # -------------------------------------------------------------------
    # Start transformation logic
    # -------------------------------------------------------------------

    # 1. Read data
    query = f"SELECT * FROM {dataset} LIMIT 10"
    df = wr.athena.read_sql_query(
        sql=query, 
        database=source_glue_database, 
        ctas_approach=False, 
        s3_output=f"s3://{env.replace('_','-')}-query-results-bucket/output/",
        keep_files=False)
    df_info(df, "Before transformation")
    
    
    # 2. Transform as needed
    # TODO


    # 3. Write results to analysis bucket
    destination = f"s3://{target_bucket}/transformations/{dataset}/"
    wr.s3.to_parquet(
        df=df,
        path=f"s3://{target_bucket}/transformations/{dataset}/",
        dataset=True,
        mode="overwrite"
    )
    # End transformation logic


    # -------------------------------------------------------------------
    # Start QuickSight integration
    # -------------------------------------------------------------------
    quicksight_integration = QuicksightIntegration(transform, df.dtypes.to_dict(), region)
    
    if transform['create_quicksight_dataset']:
        quicksight_integration.create_quicksight_dataset_if_not_exists()
    
    if transform['refresh_spice']:
        quicksight_integration.refresh_spice()

    # End QuickSight integration


    result_json['duration'] = time.time() - start
    logger.info(f"The Glue Job: {job_name} has successfully completed")
    send_sns_notification("SUCCESS")

    # transform_log
    update_transform(transform_fqn, "completed", [destination])

except Exception as e:
    exception_msg = f"Exception occurred inside this glue etl ==> {job_name} with this exception ==> {e}"
    logger.log("ERROR", exception_msg)
    send_sns_notification("FAILED")

    # transform_log
    update_transform(transform_fqn, "failed", error_msg=[exception_msg])

    raise Exception(exception_msg)
