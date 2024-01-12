__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

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
ec2_client = session.client('ec2')

class Worker(AwsWorker):

    def __init__(self):
        super().__init__()

    def get_service_name(self):
        return "EC2"

    def pause(self, arn):
        try:
            instance_id = arnparse(arn).resource
            resp = ec2_client.stop_instances(
                InstanceIds=[instance_id]
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def resume(self, arn, details=None, tf_state=None):
        try:
            instance_id = arnparse(arn).resource
            resp = ec2_client.start_instances(
                InstanceIds=[instance_id]
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def status(self, arn):
        try:
            instance_id = arnparse(arn).resource
            logger.info(instance_id)
            resp = ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )
            # print(json.dumps(resp, indent=2, default=str))
            if "Reservations" in resp:
                if "Instances" in resp["Reservations"][0]:
                    details = resp["Reservations"][0]["Instances"][0]
                    return details["State"]["Name"], details
        except Exception as e:
            logger.error(e)
        return "?",{}
