__license__ = "MIT"

import sys
import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_PROFILE = os.environ['AWS_PROFILE']

lambda_client = session.client('s3')

def call_lambda(function_name, event):
    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(event)
    )

def lambda_handler(event, context):
    logger.info('Input event: ' + json.dumps(event, indent=2, sort_keys=True))
    key = event['Records'][0]['s3']['key']
    # if key.find('/analysis/') != -1:
    #     logger.info("processing kinesis event from " + key)
    #     call_lambda(AWS_PROFILE + '_event_transformation')


