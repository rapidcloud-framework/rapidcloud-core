__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import time
import json
import boto3
import logging
import os
import fnmatch, re
import urllib
from kc_common import metadata

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

def get_boto3_session(aws_region="us-east-1"):
    session = boto3.session.Session()
    return session

session = get_boto3_session()
lambda_client = session.client('lambda')
glue_client = session.client('glue')
dynamodb_resource = session.resource('dynamodb')


def call_lambda(function_name, event):
    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(event)
    )

def get_dataset(key):
    try:
        start = key.find('/') + 1
        end = key.find('/', start)
        dataset_name = key[start:end]
        dataset_fqn = f"{PROFILE}_{dataset_name}"
        logger.info(f"dataset {dataset_name}: {dataset_fqn}")

        # get dataset info from dataset_semi_structured metadata table
        dataset = metadata.query('dataset_semi_structured', 'fqn', dataset_fqn)[0]
        logger.info(json.dumps(dataset, indent=2))
        return dataset

    except Exception as e:
        logger.error(e.args)


def get_transform(dataset):
    try:
        transform = None
        transform_fqn = f"{PROFILE}_{dataset['name']}"
        logger.info(f"getting transformation {transform_fqn}")
        transforms = metadata.query('transformation', 'fqn', transform_fqn)
        if len(transforms) > 0:
            transform = transforms[0]
        else:
            transform_fqn = f"{PROFILE}_generic"
            logger.info(f"getting transformation {transform_fqn}")
            transforms = metadata.query('transformation', 'fqn', transform_fqn)
            if len(transforms) > 0:
                transform = transforms[0]

        logger.info(json.dumps(transform, indent=2))
        return transform

    except Exception as e:
        logger.error(e.args)


def check_and_run_glue_crawlers(dataset, phase):
    try:
        # check table and run crawler if needed
        tables = glue_client.get_table(
            DatabaseName=f"{PROFILE}_{phase}db",
            Name=dataset['name']
        )
    except Exception as e:
        logger.info(e)
        crawler_name = f"{PROFILE}_{phase}-semi-structured"
        try:
            logger.info(f"starting glue crawler: {crawler_name}")
            glue_client.start_crawler(Name=crawler_name)
            logger.info("sleeping for 60 sec to allow crawler to finish ...")
            time.sleep(60) # give crawler time to finish
        except Exception as e:
            logger.info(e)


def get_partitions(key):
    logger.info(key)
    key = urllib.parse.unquote(key)
    logger.info(key)
    for key_part in key.split("/"):
        logger.info(key_part)
        if 'datalake_year=' in key_part:
            datalake_year = key_part[14:]
        elif 'datalake_month=' in key_part:
            datalake_month = key_part[15:]
        elif 'datalake_day=' in key_part:
            datalake_day = key_part[13:]

    logger.info(f"datalake_year={datalake_year}")
    logger.info(f"datalake_month={datalake_month}")
    logger.info(f"datalake_day={datalake_day}")

    return datalake_year, datalake_month, datalake_day


def start_glue_job_old(dataset, transform, key):
    try:
        # datalake_year, datalake_month, datalake_day = get_partitions(key) 
        file_name = key.split("/")[-1]
        for i in range(10):
            if f"-{i}.parquet" in file_name:
                file_name = file_name.replace(f"-{i}.parquet", "")
                break
        if ".parquet" in file_name:
            file_name = file_name.replace(f".parquet", "")

        print(f"file_name={file_name}")

        job_name = f"{PROFILE}_transform_{transform['name']}"
        logger.info(f"starting transformation Glue job: {job_name}")
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments={
                "--dataset": dataset['name'],
                "--base_datasets": dataset['name'],
                "--transform_name": transform['fqn'],
                "--extra-arg-1": f"semistructured/{dataset['name']}/{file_name}"
            }
        )
        logger.info(json.dumps(response, indent=2))


    except Exception as e:
        logger.error(e.args)


def start_glue_job(dataset, transform, key):
    try:
        batch_no = 1
        for i in range(1, 21):
            if f"-{i}.parquet" in key:
                key = key.replace(f"-{i}.parquet", "")
                batch_no = i
                break
        if ".parquet" in key:
            key = key.replace(f".parquet", "")

        print(f"key={key}")

        job_name = f"{PROFILE}_transform_{transform['name']}"
        logger.info(f"starting transformation Glue job: {job_name}")
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments={
                "--dataset": dataset['name'],
                "--base_datasets": dataset['name'],
                "--transform_name": transform['fqn'],
                "--extra-arg-1": key,
                "--extra-arg-2": batch_no,
            }
        )
        logger.info(json.dumps(response, indent=2))

    except Exception as e:
        logger.error(e.args)


def lambda_handler(event, context):
    print(event)
    for record in event['Records']:

        try:
            bucket = event["Records"][0]["s3"]["bucket"]["name"]  
            key = record['s3']['object']['key']

            # CDC completed for semistrcutured dataset
            if fnmatch.fnmatch(key, '*semistructured*'):
                dataset = get_dataset(key)     
                if dataset is not None and dataset['enable_transform']:
                    transform = get_transform(dataset)
                    if transform is not None:
                        wait = check_and_run_glue_crawlers(dataset, "raw")
                        # check_and_run_glue_crawlers(dataset, "ingestion")
                        start_glue_job(dataset, transform, key)

        except Exception as e:
            logger.error(e.args)
