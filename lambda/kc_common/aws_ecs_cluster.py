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
ecs_client = session.client('ecs')

class Worker(AwsWorker):

    def __init__(self):
        super().__init__()

    def get_service_name(self):
        return "ECS Fargate"

    def pause(self, arn):
        try:
            name = arnparse(arn).resource

            # get services for ecs cluster
            logger.info(name)
            resp = ecs_client.list_services(
                cluster=name
            )

            if "serviceArns" in resp:
                for service_arn in resp["serviceArns"]:
                    # downsize to zero
                    resp = ecs_client.update_service(
                        cluster=name,
                        service=service_arn,
                        desiredCount=0
                    )
                    logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def resume(self, arn, details=None, tf_state=None):
        try:
            name = arnparse(arn).resource

            # get services for ecs cluster
            logger.info(name)
            resp = ecs_client.list_services(
                cluster=name
            )

            for res in tf_state["resources"]:
                if res["type"] == "aws_ecs_service":
                    # change desiredCount back to original value
                    service_arn = res["instances"][0]["attributes"]["id"]
                    desired_count = res["instances"][0]["attributes"]["desired_count"]
                    resp = ecs_client.update_service(
                        cluster=name,
                        service=service_arn,
                        desiredCount=desired_count
                    )
                    logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def status(self, arn):
        try:
            name = arnparse(arn).resource

            # get services for ecs cluster
            logger.info(name)
            resp = ecs_client.list_services(
                cluster=name
            )
            # print(json.dumps(resp, indent=2, default=str))
            if "serviceArns" in resp:
                resp = ecs_client.describe_services(
                    cluster=name,
                    services=resp["serviceArns"]
                )
            # print(json.dumps(resp, indent=2, default=str))

            status = []
            if "services" in resp:
                details = resp["services"]
                for service in details:
                    status.append(f"{service['serviceName']}: {service['desiredCount']}")
                return status, details
        except Exception as e:
            logger.error(e)
        return "?",{}
