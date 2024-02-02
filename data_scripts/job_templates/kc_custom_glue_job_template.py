__license__ = "MIT"

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
import numpy as np
from boto3.dynamodb.conditions import Key, Attr

if sys.argv[1] != 'test_mode':
    from awsglue.utils import getResolvedOptions

logging.basicConfig()
logger = logging.getLogger("publish")
logger.setLevel(logging.INFO)

result_json = {
    "log": []
}

glue_client = boto3.client('glue')
sns_client = boto3.client('sns')
dynamodb_resource = boto3.resource('dynamodb')



try:
    pass

except Exception as e:
    exception_msg = f"Exception occurred inside this glue etl ==> {job_name} with this exception ==> {e}"
    logger.log("ERROR", exception_msg)
    raise Exception(exception_msg)
