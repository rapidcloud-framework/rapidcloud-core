__author__ = "Igor Royzis"
__license__ = "MIT"


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
ec2_client = session.client('ec2')


def handle_ec2_event(event):
    if event['detail']['state'] == "running":
        instance_id = event['detail']['instance-id']
        instance = ec2_client.describe_instances(
            InstanceIds=[instance_id],
        )
        for tag in instance['Reservations'][0]['Instances'][0]['Tags']:
            if tag['Key'] == 'trend_enabled' and tag['Value'] == "true":
                # thgis is done automatically by agent self-activation
                # rc_trendmicro.create_workload_computer(instance)
                pass