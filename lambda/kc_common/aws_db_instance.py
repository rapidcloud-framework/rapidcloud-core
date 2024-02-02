__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import boto3
import logging
import os
from arnparse import arnparse
from kc_common.aws_worker import AwsWorker

logger = logging.getLogger("metadata")
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

session = boto3.Session()
rds_client = session.client('rds')

class Worker(AwsWorker):

    def __init__(self):
        super().__init__()

    def get_service_name(self):
        return "RDS"

    def pause(self, arn):
        try:
            instance_id = arnparse(arn).resource
            resp = rds_client.stop_db_instance(
                DBInstanceIdentifier=instance_id
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def resume(self, arn, details=None, tf_state=None):
        try:
            instance_id = arnparse(arn).resource
            resp = rds_client.start_db_instance(
                DBInstanceIdentifier=instance_id
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)
    

    def status(self, arn):
        try:
            instance_id = arnparse(arn).resource
            resp = rds_client.describe_db_instances(
                DBInstanceIdentifier=instance_id
            )
            # print(json.dumps(resp, indent=2, default=str))
            if "DBInstances" in resp:
                details = resp["DBInstances"][0]
                return details["DBInstanceStatus"], details
        except Exception as e:
            logger.error(e)
        return "?",{}
