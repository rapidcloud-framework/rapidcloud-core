__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import os
import json
import datetime
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

def lambda_handler(event, context, test=False): 
    logger.info(json.dumps(event, indent=2))
    body = json.loads(event['body'].replace("\n","").replace("\r",""))
    body["timestamp"] = str(datetime.now())
    response = {
        'isBase64Encoded': False,
        'statusCode': 200,
        'body': json.dumps(body, default=str)
    }
    return response
