__author__ = "Igor Royzis"
__copyright__ = "Copyright 2021, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import os
import sys
import json
import datetime
import time
import boto3
import logging
import base64

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

def lambda_handler(event, context, test=False):
    for record in event['Records']:
       #Kinesis data is base64 encoded so decode here
       payload=base64.b64decode(record["kinesis"]["data"])
       logger.info("Decoded payload: " + str(payload))

       # TODO implement business logic here
       # ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(message)s')
    # $ aws lambda invoke --function-name ProcessKinesisRecords --payload file://input.txt out.txt
    with open('./lambda/kinesis_consumer_lambda_template/payload.json') as f:
        lambda_handler(json.load(f), {})