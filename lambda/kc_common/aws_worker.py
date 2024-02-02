__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import boto3
import logging
import os
from arnparse import arnparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

session = boto3.Session()
s3_resource = session.resource('s3')


class AwsWorker(object):
    
    def get_service_name():
        raise NotImplementedError

    def pause(arn):
        raise NotImplementedError

    def resume(arn, details, tf_state):
        raise NotImplementedError

    def status(arn):
        raise NotImplementedError


def get_existing_resource_arns():
    bucket = f"{PROFILE.replace('_','-')}-kc-big-data-tf-state"
    key = f"{PROFILE}/terraform.tfstate"
    resources = {}
    tf_state = {}
    try:
        logger.info(f"{bucket}/{key}")
        obj = s3_resource.Bucket(bucket).Object(key=key).get()
        tf_state = json.loads(obj['Body'].read().decode('utf-8'))
        for res in tf_state["resources"]:
            if res['type'] not in resources:
                resources[res['type']] = []

            if "instances" in res:
                for inst in res["instances"]:
                    if "attributes" in inst and "arn" in inst["attributes"]:
                        exis_res = {
                            "arn": inst["attributes"]["arn"],
                            "details": inst
                        }
                        resources[res['type']].append(exis_res)
                        # if res['type'] == "aws_ecs_cluster":
                        #     print(exis_res)
    except Exception as e:
        logger.warn(e)
    
    # print(resources["aws_ecs_cluster"])
    
    return resources, tf_state
