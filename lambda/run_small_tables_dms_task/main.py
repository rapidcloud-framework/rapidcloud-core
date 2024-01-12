__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import time
import copy
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']
DATABASE = os.environ['DATABASE']
DMS_TASK_ID = os.environ['DMS_TASK_ID']

MAPPINGS = { 
    "rules": [
    ] 
}

TABLE = { 
    "rule-type": "selection", 
    "rule-id": "<value>", 
    "rule-name": "<value>", 
    "object-locator": { 
        "schema-name": "<value>", 
        "table-name": "<value>",
        "table-type": "all"
    }, 
    "rule-action": "include", 
    "filters": [],
    "load-order": "<value>" 
}


def init(lamda_mode):
    global dynamodb_client
    global dynamodb_resource
    global dms_client

    if lamda_mode:
        session = boto3.Session()
    else:
        session = boto3.Session(profile_name=PROFILE)

    dynamodb_client = session.client('dynamodb')
    dynamodb_resource = session.resource('dynamodb')
    dms_client = session.client('dms')


def modfy_replication_task(dms_task_arn, table_mappings):
    # updating DMS task 
    logger.info("Updating DMS task...")    
    response = dms_client.modify_replication_task(
        ReplicationTaskArn=dms_task_arn,
        TableMappings=json.dumps(table_mappings),
        MigrationType='full-load'
    )
    logger.info(response)


def start_replication_task(dms_task_arn):
    # starting DMS task 
    status = ''
    while status != 'stopped' and status != 'ready':
        time.sleep(2)
        status = get_dms_task_info(DMS_TASK_ID, 'Status')

    logger.info("Starting DMS task...")    
    response = dms_client.start_replication_task(
        ReplicationTaskArn = dms_task_arn,
        StartReplicationTaskType='reload-target'
    )
    logger.info(response)


def get_dms_task_info(dms_task_id, key):
    logger.info("Getting DMS task info: " + dms_task_id + " | " + key)    
    response = dms_client.describe_replication_tasks(
        Filters = [
            {
                'Name': 'replication-task-id',
                'Values': [dms_task_id]
            }
        ]
    )
    logger.info("Got DMS task info")
    dms_task = response['ReplicationTasks'][0]
    info = dms_task.get(key)
    if not info:
      info = ''
    logger.info(info)
    return info


def update_table_mappings():
    # get small datasets
    datasets = dynamodb_resource.Table('dataset').scan(
        FilterExpression=Attr('profile').eq(PROFILE) & Attr('size').eq('small') & Attr('source_database').eq(DATABASE),
    )['Items']

    # construct DMS task table mappings json
    logger.info("constructing DMS task table mappings json...")    
    table_mappings = copy.deepcopy(MAPPINGS)
    i = 2
    for dataset in datasets:
        table_mapping = copy.deepcopy(TABLE)
        table_mapping['rule-id'] = str(i)
        table_mapping['rule-name'] = str(i)
        table_mapping['object-locator']['schema-name'] = dataset['source_schema']
        table_mapping['object-locator']['table-name'] = dataset['source_table']
        table_mapping['load-order'] = i * 10
        table_mappings['rules'].append(table_mapping)
        i += 1
    logger.info(json.dumps(table_mappings, indent=2))
    return table_mappings


def lambda_handler(event, context):
    logger.info("Event:")
    logger.info(event)
    logger.info("Context:")
    logger.info(context)

    init(True)
    dms_task_arn = get_dms_task_info(DMS_TASK_ID, 'ReplicationTaskArn')
    table_mappings = update_table_mappings()
    modfy_replication_task(dms_task_arn, table_mappings)
    start_replication_task(dms_task_arn)
