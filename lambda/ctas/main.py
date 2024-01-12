__author__ = "Igor Royzis"
__copyright__ = "Copyright 2021, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import os
import sys
import json
import datetime
import time
import math
import threading
import boto3
import botocore
import pandas as pd
import pyarrow
import logging
import numpy as np

from  boto3.dynamodb.conditions import Key, Attr

from kc_governance import rules
from kc_common import s3
from kc_common import metadata
from kc_common import reformat

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(message)s')
logger = logging.getLogger()

PROFILE = os.environ['PROFILE']
DEFAULT_PARTITIONS = "year,month,day,timestamp"
JOB_NAME = "cdc"
MAX_BATCH_SIZE_BYTES = 4 * 1024 * 1024 # 4MB
MAX_BATCH_SIZE_ROWS = 5000 
MIN_BATCHES = 1 # run N batches at the same time

class Ctas(object):

    def __init__(self):        
        session = boto3.Session()
        self.s3_resource = session.resource('s3')
        self.dynamodb_resource = session.resource('dynamodb')
        self.athena_client = session.client('athena')
        self.sns_client = boto3.client('sns')
        
        self.result_json = {}


    def process_file(self, bucket, key):
        started = time.time()
        logger.info(f"processing {bucket}/{key}")
        self.result_json.clear()
        self.result_json['log'] = []
        self.result_json['destination'] = []
        self.result_json['started'] = datetime.datetime.now()
        self.result_json['source_bucket'] = bucket
        self.result_json['source_key'] = key
    
        try:
            # get dataset info 
            # key format for database: databases/schema/dataset_name/
            # "key": "databases/theia_sample/guest/orders/LOAD00000001.csv"
            parsed = key.split("/")
            source_database = parsed[1]
            source_schema = parsed[2]
            dataset_name = parsed[3]
            dataset = metadata.scan('dataset', {
                "source_database": source_database,
                "source_schema": source_schema,
                "source_table": dataset_name
            })[0]
            dataset_type = "dataset"

            logger.info(json.dumps(dataset, indent=2, default=self.json_converter))
            self.result_json['dataset_name'] = dataset_name

            # mark cdc_log as pending
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "pending")

            # file name
            start = key.rfind('/') + 1
            file_name = key[start:]
            self.result_json['file_name'] = file_name

            # TODO Add CTAS/INSERT logic here
            #   - use CTAS only for the first LOAD* file
            #       - https://docs.aws.amazon.com/athena/latest/ug/ctas.html
            #   - use INSERT INTO for the rest of LOAD* files
            #       - https://docs.aws.amazon.com/athena/latest/ug/insert-into.html

            # ...


            # mark file as processed    
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "processed", destination=self.result_json['destination'])

        except Exception as e:
            # mark cdc_log as failed
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "failed", error_msg=str(e))
            self.result_json['log'].append(e)
            logger.error(e.args)
            self.send_sns("FAILED")
            raise e

        self.result_json['finished'] = datetime.datetime.now()
        self.result_json['duration'] = time.time() - started
        
        # send completion notification
        self.send_sns("SUCCESS")


    def send_sns(self, status):
        for topic in self.sns_client.list_topics()['Topics']:
            if f"{PROFILE}_general_notifications" in topic['TopicArn']:
                self.sns_client.publish(
                    TopicArn=topic['TopicArn'],
                    Subject=f"{status} - {JOB_NAME} / {self.result_json['dataset_name']}",    
                    Message=json.dumps(self.result_json, indent=2, default=self.json_converter)    
                )



def lambda_handler(event, context, test=False): 
    logger.info(json.dumps(event, indent=2))
    for record in event['Records']:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]  
        key = record['s3']['object']['key'] 
        if test or not metadata.is_file_loaded(f"s3://{bucket}/{key}"):
            Ctas().process_file(bucket, key)
        else:
            logger.info("this file has already been processed")


TEST_DMS_INGESTION = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2021-10-18T18:19:21.670Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AWS:AROATTKLAGPXZW3QQE3KS:dms-session-for-replication-engine"
                },
                "requestParameters": {
                    "sourceIPAddress": "54.160.59.41"
                },
                "responseElements": {
                    "x-amz-request-id": "EA5C88HE3AHBMWPA",
                    "x-amz-id-2": "W1Q5AAT3RNtCUTbYMbKE1kolXsc62YH8ymcufCNYLDqr0FkLKj32PevXT4XqjSH/6c+yvKEWsAgP6ajSLvShqsF6qJvkVytt"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "tf-s3-lambda-2021060818254264810000001d",
                    "bucket": {
                        "name": "kinect-theia-2-ingestion",
                        "ownerIdentity": {
                            "principalId": "A2HE2OAPHXSZ2H"
                        },
                        "arn": "arn:aws:s3:::kinect-theia-2-ingestion"
                    },
                    "object": {
                        "key": "databases/theia_sample/guest/staffs/LOAD00000001.parquet",
                        "size": 2521,
                        "eTag": "72c7ea93f0848c4dc396379871a656f1",
                        "sequencer": "00616DBAA99EDF22A6"
                    }
                }
            }
        ]
    }


TEST_SEMIFILE_INGESTION = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2021-10-18T18:52:09.530Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDATTKLAGPXQKS3G3YUL'}, 'requestParameters': {'sourceIPAddress': '170.250.185.254'}, 'responseElements': {'x-amz-request-id': 'AQ2RH7XV6DK06RDZ', 'x-amz-id-2': 'WCKOslMNSGceBgpIVG7WeSvJrzwu041vuXn/U2Dhwk0g0jUXPGHHB6OpIEq2hgi5+sZ5Uv2WSn4hOg3UygpCqMp7I2ZeQiR5'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'tf-s3-lambda-2021060818254264810000001d', 'bucket': {'name': 'kinect-theia-2-ingestion', 'ownerIdentity': {'principalId': 'A2HE2OAPHXSZ2H'}, 'arn': 'arn:aws:s3:::kinect-theia-2-ingestion'}, 'object': {'key': 'semistructured/benefits/benefits_sample.csv', 'size': 147, 'eTag': '1dda1668b368a80da59b5a91281c49df', 'sequencer': '00616DC25977641BD3'}}}]}



def main():
    # lambda_handler(TEST_DMS_INGESTION, '', True)
    lambda_handler(TEST_SEMIFILE_INGESTION, '', True)

if __name__ == "__main__":
    main()
