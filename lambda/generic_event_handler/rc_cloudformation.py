__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import boto3
import botocore
import rc_trendmicro

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-5s %(name)-39s:  %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ.get('PROFILE')

session = boto3.Session()
cloudformation_client = session.client('cloudformation')


def handle_cloudformation_event(event):
    if event['detail']['status-details']['status'] == "CREATE_COMPLETE":
        stack_name = event['detail']['stack-id'].split('/')[1]
        if "TM-FSS" in stack_name:
            cf_stack = get_cf_stack(stack_name)
            rc_trendmicro.deploy_filestorage_stack(stack_name, cf_stack)


def get_cf_stack(stack_name):
    try:
        logger.info(f"getting CF stack {stack_name}")
        result = cloudformation_client.describe_stacks(StackName=stack_name)
        if "Stacks" in result and len(result['Stacks']) > 0:
            cf_stack = result['Stacks'][0]
            cf_stack['parsed'] = {
                "status": cf_stack['StackStatus'],
                "params": {},
                "outputs": {},
                "tags": {}
            }

            for param in cf_stack['Parameters']:
                cf_stack['parsed']['params'][param['ParameterKey']] = param['ParameterValue']

            for output in cf_stack['Outputs']:
                cf_stack['parsed']['outputs'][output['OutputKey']] = output['OutputValue']

            for tag in cf_stack['Tags']:
                cf_stack['parsed']['tags'][tag['Key']] = tag['Value']

            del cf_stack['Parameters']
            del cf_stack['Outputs']
            del cf_stack['Tags']

            logger.info(f"{stack_name} status -> {cf_stack['StackStatus']}")
            logger.info(json.dumps(cf_stack, indent=2, default=str))

            return cf_stack
    except Exception as e:
        logger.info(e)
        return None
