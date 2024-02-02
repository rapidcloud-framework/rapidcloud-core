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
asg_client = session.client('autoscaling')

class Worker(AwsWorker):

    def __init__(self):
        super().__init__()

    def get_service_name(self):
        return "Auto Scaling Group"

    def pause(self, arn):
        try:
            # name = "tf-asg-20221104150716038800000001"
            name = arnparse(arn).resource
            resp = asg_client.update_auto_scaling_group(
                AutoScalingGroupName=name,
                MinSize=0,
                DesiredCapacity=0
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def resume(self, arn, details=None, tf_state=None):
        try:
            min_size = details['attributes']['min_size']
            desired_capacity = details['attributes']['desired_capacity']
            # name = "tf-asg-20221104150716038800000001"
            name = arnparse(arn).resource
            resp = asg_client.update_auto_scaling_group(
                AutoScalingGroupName=name,
                MinSize=min_size,
                DesiredCapacity=desired_capacity
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def status(self, arn):
        try:
            # name = "tf-asg-20221104150716038800000001"
            name = arnparse(arn).resource
            resp = asg_client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[name]
            )
            # print(json.dumps(resp, indent=2, default=str))
            if "AutoScalingGroups" in resp:
                details = resp["AutoScalingGroups"][0]
                return f"count: {len(details['Instances'])}", details
        except Exception as e:
            logger.error(e)
        return "?",{}
