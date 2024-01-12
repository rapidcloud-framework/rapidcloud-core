__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Input event: ' + json.dumps(event, indent=2, sort_keys=True))
    key = event['Records'][0]['s3']['key']
    logger.info("processing kinesis event " + key)


