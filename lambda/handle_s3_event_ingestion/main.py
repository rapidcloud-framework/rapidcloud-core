__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import json
import logging
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import fnmatch, re

from kc_common import metadata

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']
CDC_LAMBDA = f'{PROFILE}_cdc'
CTAS_LAMBDA = f'{PROFILE}_ctas'
EVENT_CDC_LAMBDA = f'{PROFILE}_event_cdc'
DMS_TS_CDC_LAMBDA = f'{PROFILE}_dms_ts_cdc' 
FILE_WORKFLOW_LAMBDA = f'{PROFILE}_file_workflow'


def get_lambda_memory_size(file_size):
    lambda_props = metadata.get_properties("lambda_")
    return lambda_props['lambda_memory_size_xlarge']
    # if file_size < lambda_props['lambda_file_size_small']:
    #     return lambda_props['lambda_memory_size_small']
    # elif file_size < lambda_props['lambda_file_size_medium']:
    #     return lambda_props['lambda_memory_size_medium']
    # elif file_size < lambda_props['lambda_file_size_large']:
    #     return lambda_props['lambda_memory_size_large']
    # elif file_size < lambda_props['lambda_file_size_xlarge']:
    #     return lambda_props['lambda_memory_size_xlarge']
    # else: # TODO use xlarge for now and hope it's not going to fail :)
    #     return lambda_props['lambda_memory_size_xlarge']


def call_lambda(function_name, event):
    logger.info(f"Calling lambda function: {function_name}")
    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(event, indent=2)
    )
   
def get_boto3_session(aws_region="us-east-1"):
    session = boto3.session.Session()
    return session

session = get_boto3_session()
lambda_client = session.client('lambda')
dynamodb_resource = session.resource('dynamodb')

def json_converter(self, obj):
    return str(obj)


def get_dataset(key, semistructured=True):
    try:
        start = key.find('/') + 1
        end = key.find('/', start)
        dataset_name = key[start:end]
        dataset_fqn = f"{PROFILE}_{dataset_name}"
        logger.info(f"dataset {dataset_name}: {dataset_fqn}")

        # get dataset info from dataset_semi_structured metadata table
        dataset = metadata.query(f"dataset{'_semi_structured' if semistructured else ''}", 'fqn', dataset_fqn)[0]
        logger.info(json.dumps(dataset, indent=2))
        return dataset

    except Exception as e:
        logger.error(e.args)


def get_database(key):
    try:
        dataset = get_dataset(key, False)
        source_database = dataset.get("source_database")
        source_database_fqn = f"{PROFILE}_{source_database}"
        database = metadata.query("source_database", "fqn", source_database_fqn)[0]
        return database

    except Exception as e:
        logger.error(e.args)


def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        ## parse out the S3 bucket
        s3_ingestion_bucket = event["Records"][0]["s3"]["bucket"]["name"]  
        key = record['s3']['object']['key']
        size = record['s3']['object']['size']
        ## Note: The actual key for the "cdc_log" table is the "fqn" and the value should be the fully qualified S3 bucket name concatenated 
        ## with the s3 prefix with key. This shoul also have the s3:// prefix.
        cdc_fqn = f's3://{s3_ingestion_bucket}/{key}'
        
        logger.info(f'S3 Ingestion Bucket: {s3_ingestion_bucket}')
        logger.info(f'Key: {key}')
        logger.info(f'Size: {size}')
        logger.info(f'Cdc Fqn: {cdc_fqn}')

        if size == 0:
            continue
        
        # make sure this S3 object has not been processed already
        cdc_log_item = None
        items = metadata.query('cdc_log', 'fqn', cdc_fqn)
        if items:
            cdc_log_item = items[0]
            logger.info(json.dumps(cdc_log_item, indent=2, sort_keys=True, default=json_converter))        

        if cdc_log_item is None or cdc_log_item['status'] != 'processed':
            logger.info(f"Processing {key}")

            # CDC via event streaming via kinesis
            if fnmatch.fnmatch(key, '*events*'):
                logger.info(f"processing kinesis event from {key}")
                call_lambda(EVENT_CDC_LAMBDA, event)
            
            # CDC for semi-structured data (csv, json, xml)
            elif fnmatch.fnmatch(key, '*semistructured*'):
                logger.info(f"processing file from  {key}")
                dataset = get_dataset(key)
                if dataset['enabled']: 
                    lambda_function_name = f"{CDC_LAMBDA}_{get_lambda_memory_size(size)}"
                    call_lambda(lambda_function_name, event)
                else:
                    logger.info(f"{dataset} is disabled")

            # CDC for unstructured data (documents, media)
            elif fnmatch.fnmatch(key, '*files*'):
                logger.info(f"processing file from  {key}")
                call_lambda(FILE_WORKFLOW_LAMBDA, event)
            
            # CDC via timestamp based DMS tasks
            elif fnmatch.fnmatch(key, '*databases*') and fnmatch.fnmatch(key, '*action*'):
                logger.info(f"processing timestamp based CDC from {key}")
                call_lambda(DMS_TS_CDC_LAMBDA, event)
            
            # CDC via DMS on-going replication tasks
            elif fnmatch.fnmatch(key, '*databases*'):
                logger.info(f"processing DMS built-in CDC from {key}")
                if fnmatch.fnmatch(key, '*LOAD*.csv'):
                    use_ctas = get_database(key).get('use_ctas')
                    if use_ctas == 'yes' or use_ctas is True:
                        logger.info(f"Calling ctas lambda")
                        # call_lambda(CTAS_LAMBDA, event)
                else:
                    lambda_function_name = f"{CDC_LAMBDA}_{get_lambda_memory_size(size)}"
                    call_lambda(lambda_function_name, event)

        else:
            logger.warn(f"Object {key} has already been processed")


