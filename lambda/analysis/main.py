__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init(lamda_mode):
    if lamda_mode:
        session = boto3.Session()
    else:
        session = boto3.Session(profile_name=AWS_PROFILE)


def lambda_handler(event, context):
    logger.info('Input event: ' + json.dumps(event, indent=2, sort_keys=True))

    init(True) # lambda mode


# ----------------------------------------------------
# testing 
# ----------------------------------------------------
def main():
    init(False) # CLI mode

if __name__ == "__main__":
    main()

