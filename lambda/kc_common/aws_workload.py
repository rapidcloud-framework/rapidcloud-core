__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import importlib
import json
import logging
import os
import sys
import traceback
import boto3

from kc_common import metadata
from kc_common import aws_worker


logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-5s %(name)-39s:  %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ.get('PROFILE')

session = boto3.Session()
ec2_client = session.client('ec2')


def get_enabled_resource_types():
    enabled = []
    for item in metadata.get_modules("workload", "enable_pause"):
        for elem, value in item.items():
            if "workload_module_" in elem and value:
                enabled.append(elem.replace("workload_module_", ""))
    return enabled


def get_workload_schedule_info(schedule_name):
    return metadata.get_modules("workload", "schedule", schedule_name)


def get_aws_worker_instance(res_type):
    worker_module = importlib.import_module(f"kc_common.{res_type}")
    return worker_module.Worker()


def pause_or_resume(event):
    action = event['action']

    # resource types enabled for current environment
    enabled_res_types = get_enabled_resource_types()
    logger.info(f"enabled_res_types: {enabled_res_types}")

    # schedule info (if running as part of schedule)
    res_types = []
    if 'schedule_name' in event:
        schedule_info = get_workload_schedule_info(event['schedule_name'])[0]
        logger.info(json.dumps(schedule_info, indent=2))
        res_types = schedule_info['params']["workload_resource_type"].split(",")
    elif 'resource_types' in event:
        if event["resource_types"] == "all":
            res_types = enabled_res_types
        else:
            res_types = event["resource_types"].split(",")
    logger.info(f"res_types to {action}: {res_types}")

    # get existing resource arns from tfstate
    existing_resources, tf_state = aws_worker.get_existing_resource_arns()
    if 'verbose' in event:
        # for res_type in existing_resources.keys():
        #     logger.info(res_type)
        with open(f"../testing/tf/existing_resources_for_pause.json", 'w') as f:
            f.write(json.dumps(existing_resources, indent=2, default=str))

    # process pause or resume for each resource type
    for res_type in res_types:
        logger.info("")
        logger.info(f"{action} {res_type}")
        if res_type in existing_resources:
            for res_info in existing_resources[res_type]:
                arn = res_info['arn']
                logger.info(arn)
                try:
                    worker_instance = get_aws_worker_instance(res_type)
                    func = getattr(worker_instance, action)
                    if action == "pause":
                        func(arn)
                    else:
                        func(arn, res_info['details'], tf_state)
                    logger.info("completed")
                except Exception as e:
                    logger.error("failed")
                    logger.error(e)
                    traceback.print_exc() 
        else:
            logger.info(f"{res_type} is not in current environment")


def status():
    existing_resources, tf_state = aws_worker.get_existing_resource_arns()
    enabled_res_types = get_enabled_resource_types()
    # logger.info(f"enabled_res_types: {enabled_res_types}")
    result = []
    for res_type, resources in existing_resources.items():
        if res_type in enabled_res_types:
            worker_instance = get_aws_worker_instance(res_type)
            logger.info(res_type)
            # logger.info(worker_instance)
            for res in resources:
                if "arn" in res and res['arn'] is not None:
                    # logger.info(res)
                    status, data = worker_instance.status(res['arn'])
                    result.append({
                        "service": worker_instance.get_service_name(),
                        "res_type": res_type,
                        "arn": res['arn'],
                        "status": status,
                        "describe_details": data
                    })
    
    result.sort(key=lambda x: x["service"])
    return result