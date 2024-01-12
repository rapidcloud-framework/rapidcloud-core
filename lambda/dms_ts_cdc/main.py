__author__ = "Jeffrey Planes"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "jplanes@kinect-consulting.com"

import os
import sys
import s3fs
import fnmatch, re
from   datetime import datetime
import pandas as pd
import awswrangler as wr
import boto3
import logging
from   boto3.dynamodb.conditions import Key, Attr
## May consider removing this Class Module all together in place of Igor's metadata module
from   kc_common.kc_cdc_log import CdcLog
from   kc_common.kc_metadata import Metadata

from kc_governance import rules
from kc_common import reformat

## Passed in an environment variables
profile = os.environ['PROFILE']
separater_path = '/'
aws_service = 'dynamodb'
dynamo_dataset_table = 'dataset'
dynamo_cdc_log_table = 'cdc_log'
file_compression = 'snappy'
to_parquet_mode = 'append'
cdc_action_pattern = '*action*'
replace_from = '%3D'
replace_to = '='
## Retrieve AWS Lambda Environmental Variables
aws_region = os.environ['AWS_REGION']
lambda_function = os.environ['AWS_LAMBDA_FUNCTION_NAME']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

## Instantiate the  CdcLog Class
cdc_logger = CdcLog(lambda_function,aws_region)
## Instantiate the  Metadata Class
metadata = Metadata(aws_region,aws_service)

def lambda_handler(event, context):
    
    try:
       
        ## parse out the S3 bucket
        s3_ingestion_bucket = event["Records"][0]["s3"]["bucket"]["name"]    
        ## parse out the S3 Object Key which is the file name without the S3 bucket
        s3_ingestion_key = event['Records'][0]['s3']['object']['key']
        ## If you execute the Lambda function from the event test (cdctest), the Lambda function successfully executes.
        ## I have found whenever triggering the file from the cdc location there are specidal characters where the equal signs ('=') are being substituded with %3D.
        ## Here is an example of what I was seeing --> atlas/atlas/inbound_call/action%3Du/year%3D2020/month%3D5/day%3D11/LOAD00000001.parquet
        s3_ingestion_key = s3_ingestion_key.replace(replace_from,replace_to)
        ## Get the file name in the s3_key
        file_name = s3_ingestion_key[s3_ingestion_key.rindex(separater_path)+1:]
        s3_ingestion_location = f's3://{s3_ingestion_bucket}/{s3_ingestion_key}'

        ## Query the event_log to get the indicate if the file has already been loaded before.
        ## Switch over to use Igor's metadata.is_file_loaded function.
        ## Returns either True/False
        is_loaded = metadata.is_file_loaded(dynamo_cdc_log_table,"fqn",s3_ingestion_location) 
        ## Evaluate if the file has already been loaded before
        if (not is_loaded):

            ingest_key_list = s3_ingestion_key.split(separater_path)
            ## Get the metadata from the path
            source_database = ingest_key_list[1]
            source_schema = ingest_key_list[2]
            dataset_name = ingest_key_list[3]
            cdc_action = ''
            
            logger.info(f'S3 Ingestion Bucket: {s3_ingestion_bucket}')
            logger.info(f'Source Database: {source_database}')
            logger.info(f'S3 Ingestion Key: {s3_ingestion_key}')
            logger.info(f'Schema Name: {source_schema}')
            logger.info(f'Dataset Name: {dataset_name}')
            logger.info(f'S3 Ingest Location: {s3_ingestion_location}')
            logger.info(f'Event File: {file_name}')
            logger.info(f'Profile: {profile}')
            logger.info(f'AWS region: {aws_region}')
            logger.info(f'File Compression: {file_compression}')
            logger.info(f'To Parquet Mode: {to_parquet_mode}')
            logger.info(f'CDC Action Pattern: {cdc_action_pattern}')
            logger.info(f'Ingest Key List: {ingest_key_list}')
            
            #Search for action in the path, if so capture that value to be added to the Dataframe
            for v in ingest_key_list:
                logger.info(f'Inside ingest_key_list loop: {v}')
                if fnmatch.fnmatch(v,cdc_action_pattern):
                    cdc_action = v.replace('action=','').replace('cdc_action=','')
            
            if cdc_action is None or cdc_action == '':
                exception_msg = f"Exception Occurred Inside this job {lambda_function} --> No cdc action found in path for {s3_ingestion_key}"
                raise Exception(exception_msg)
            
            logger.info(f'CDC Action: {cdc_action}')        

            ## df = pd.read_parquet(path=s3_ingestion_location)
            # Retrieving the data directly from Amazon S3
            df = wr.s3.read_parquet(path=s3_ingestion_location, dataset=True)
            ## Add in the cdc_action to the Dataframe
            df['cdc_action'] = cdc_action 
            
            ## Query the metadata to get the s3_raw_bucket
            response_dataset = metadata.get_dataset_metadata(dynamo_dataset_table,source_database,source_schema,dataset_name,profile)  
            
            ## Evaluate if the response object is empty
            if len(response_dataset) == 0:
                exception_msg = f"Exception Occurred Inside this job {lambda_function} --> No metadata returned for {dynamo_dataset_table}"
                raise Exception(exception_msg)
                
            for dataset in response_dataset:
                s3_raw_location = dataset['raw_location']
                raw_catalog = dataset['raw_catalog']
            
            # apply rules to final list of items
            data = rules.process(dataset_name, df)
            logger.info("After processing rules:")
            ##logger.info(data.iloc[:3])

            ## apply reformatting to final list of items
            data = reformat.process(dataset_name, df)
            logger.info("After reformatting:")

            logger.info(f's3 Raw Location: {s3_raw_location}')
            wr.s3.to_parquet(
                df=data
                ,path=s3_raw_location
                ,dataset=True
                ,database=raw_catalog
                ,table=dataset_name
                ,mode=to_parquet_mode
                ,compression=file_compression ## compression metadata column
            ) 

            ## cdc logs
            ##  Switch over to use Igor's metadata.mark_file_loaded function.
            cdc_logger.cdc_log(s3_ingestion_location,s3_ingestion_bucket,s3_ingestion_key,file_name,source_database,source_schema,dataset_name,cdc_action)
            return_message = f"Successfully processed event file ==> {s3_ingestion_location}"
            logger.info(return_message)
            logger.info(f"Ending lambda function ==> {lambda_function}")
        
        else:

            return_message = f"This file has aleady been loaded ==> {s3_ingestion_location}"
            logger.warning(return_message)
            logger.info(f"Ending lambda function ==> {lambda_function}")
        
        return {
            'statusCode': 200,
            'body': return_message
        }             
        
    except Exception as e:
        msg = e.args
        exception_msg = f"Exception Occurred Inside this method {lambda_function} --> Here is the exception Message {msg}"
        logger.error(exception_msg)
        raise e