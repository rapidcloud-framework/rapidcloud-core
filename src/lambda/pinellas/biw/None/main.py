__author__ = "Igor Royzis"
__license__ = "MIT"


import os
import sys
import json
import datetime
import time
import boto3
import pyarrow
import s3fs
import logging

logging.basicConfig()
logger = logging.getLogger(JOB_NAME)
logger.setLevel(logging.INFO)

def lambda_handler(event, context, test=False): 
    logger.info(json.dumps(event, indent=2))
