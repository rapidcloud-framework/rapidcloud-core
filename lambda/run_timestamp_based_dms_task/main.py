__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import json
import boto3
import datetime
from datetime import date
from boto3.dynamodb.conditions import Key, Attr
import os
import time
import logging
import copy

logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']
DMS_TASK_ID_INSERTS = os.environ['DMS_TASK_ID_INSERTS']
DMS_TASK_ID_UPDATES = os.environ['DMS_TASK_ID_UPDATES']

# boto3 clients and resources
if 'AWS_PROFILE' in os.environ:
    logger.info(os.environ['AWS_PROFILE'])
    session = boto3.Session(profile_name=os.environ['AWS_PROFILE'])
else:
    session = boto3.Session()

dynamodb_resource = session.resource('dynamodb')
dynamodb_client = session.client('dynamodb')
dms_client = session.client('dms')

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DATE_FORMAT = '%Y-%m-%d'

MAPPINGS = { 
    "rules": [
        { 
            "rule-type": "transformation", 
            "rule-id": "1", 
            "rule-name": "1", 
            "rule-target": "table", 
            "object-locator": { 
                "schema-name": "%", 
                "table-name": "%" 
            }, 
            "rule-action": "add-suffix", 
            "value": "<value>"
        }
    ] 
}

TABLE_INSERTS = { 
    "rule-type": "selection", 
    "rule-id": "<RULE_ID>", 
    "rule-name": "<RULE_NAME>", 
    "object-locator": { 
      "schema-name": "<VAR_SCHEMA>", 
      "table-name": "<VAR_TABLE>" 
    }, 
    "rule-action": "include", 
    "load-order": "<VAR_LOAD_ORDER>", 
    "filters": [ 
      { 
        "filter-type": "source", 
        "column-name": "<CREATION_DATE>", 
        "filter-conditions": [ 
          { 
            "filter-operator": "between", 
            "start-value": "<VAR_TIMESTAMP_START>", 
            "end-value": "<VAR_TIMESTAMP_END>" 
          } 
        ] 
      } 
    ] 
  }

TABLE_UPDATES = { 
    "rule-type": "selection", 
    "rule-id": "<VAR_RULE_ID>", 
    "rule-name": "<VAR_RULE_ID>", 
    "object-locator": { 
      "schema-name": "<VAR_SCHEMA>", 
      "table-name": "<VAR_TABLE>" 
    }, 
    "rule-action": "include", 
    "load-order": "<VAR_LOAD_ORDER>", 
    "filters": [ 
      { 
        "filter-type": "source", 
        "column-name": "<LAST_UPDATE_DATE>", 
        "filter-conditions": [ 
          { 
            "filter-operator": "between", 
            "start-value": "<VAR_TIMESTAMP_START>", 
            "end-value": "<VAR_TIMESTAMP_END>" 
          } 
        ] 
      }, 
      { 
        "filter-type": "source", 
        "column-name": "<CREATION_DATE>", 
        "filter-conditions": [ 
          { 
            "filter-operator": "ste", 
            "value": "<VAR_TIMESTAMP_START_MINUS_ONE_MILLI>" 
          } 
        ] 
      } 
    ] 
  }


def get_cdc_datasets():
    return dynamodb_resource.Table('dataset').scan(
        FilterExpression=Attr('profile').eq(PROFILE) & Attr('size').ne('small'), 
    )['Items']


def get_last_run_info(dms_task_arn):
    last_run_info = dynamodb_resource.Table('cdc_tracker').scan(        
        FilterExpression=Attr('dms_task_arn').eq(dms_task_arn) & Attr('task_status').eq('started') 
    )['Items']
    return last_run_info[0] if last_run_info else []


def save_current_run_info(dms_task_arn, dms_task_id, start, end):
    logger.info("Saving new run info...")  
    return dynamodb_resource.Table('cdc_tracker').put_item(
        Item={
            'profile': PROFILE,
            'dms_task_arn': dms_task_arn, 
            'dms_task_id': dms_task_id, 
            'cdc_start_timestamp': start, 
            'cdc_end_timestamp': end, 
            'modified_on': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 
            'task_status': 'started'
        }
    )


def mark_completed(dms_task_arn, timestamp):
    logger.info("Marking as completed...")  
    dynamodb_resource.Table('cdc_tracker').update_item(
        Key={'dms_task_arn': dms_task_arn, 'timestamp': timestamp},
        UpdateExpression="set task_status = :p",
        ExpressionAttributeValues={':p': 'completed'}
    )


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
    dms_task = response['ReplicationTasks'][0]
    info = dms_task.get(key)
    if not info:
      info = ''
    logger.info(info)
    return info


def modify_dms_replication_task(dms_task_arn, table_mappings):
    logger.info("Updating DMS task...")    
    response = dms_client.modify_replication_task(
        ReplicationTaskArn = dms_task_arn,
        TableMappings = json.dumps(table_mappings) 
    )
    logger.info(response)


def start_replication_task(dms_task_arn):
    logger.info(f"Starting DMS task: {dms_task_arn}")    
    response = dms_client.start_replication_task(
        ReplicationTaskArn = dms_task_arn,
        StartReplicationTaskType='reload-target'
    )
    logger.info(response)


def lambda_handler(event, context):
    logger.info(event)
    task_type = event['task_type']
    if task_type == 'inserts':
        CDC_PARTITION = '/action=i'
        DMS_TASK_ID = DMS_TASK_ID_INSERTS
        TABLE = TABLE_INSERTS
    elif task_type == 'updates':
        CDC_PARTITION = '/action=u'
        DMS_TASK_ID = DMS_TASK_ID_UPDATES
        TABLE = TABLE_UPDATES
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Incorrect parameter, must be one of inserts|updates')
        }

    # get CDC datasets
    datasets = get_cdc_datasets()
    if not datasets:
        logger.warn('No datasets found for CDC')
        return
    else:
        for dataset in datasets:
            logger.info(f"dataset: {dataset['fqn']}")

    ## DMS Task ID and ARN
    DMS_TASK_ARN = get_dms_task_info(DMS_TASK_ID, 'ReplicationTaskArn')

    # Do not run if current DMS Task status is not ready or stopped
    status = get_dms_task_info(DMS_TASK_ID, 'Status')
    if status != 'stopped' and status != 'ready':
        return {
            'statusCode': 200,
            'body': json.dumps('Incorrect DMS Task status. Must be one of ready|stopped')
        }

    # Get last run info (timstamp and status)
    last_run_info = get_last_run_info(DMS_TASK_ARN)
    logger.info(json.dumps(last_run_info, indent=2))

    # Do not run inserts|updates if DMS Task ReplicationTaskStartDate is before 'modified-on' tag. 
    #   This means DMS task was modified for next CDC schedule, but did not run yet
    if 'modified_on' in last_run_info:
        modified_on = datetime.datetime.strptime(last_run_info['modified_on'], DATETIME_FORMAT)
        dms_task_started_on = get_dms_task_info(DMS_TASK_ID, 'ReplicationTaskStartDate') 
        if dms_task_started_on == '':
            modified_on = datetime.datetime.now()
            logger.info("DMS task never ran")
        else:    
            started_on = datetime.datetime.strptime(dms_task_started_on.strftime(DATETIME_FORMAT), DATETIME_FORMAT)
            logger.info("modified_on " + str(modified_on) + ", started_on " + str(started_on))
            if modified_on > started_on:
                # run it now and exit function    
                start_replication_task(DMS_TASK_ARN)
                return {'statusCode': 200, 'body': 'Timestamp based DMS task started'}

        # mark last run as completed
        mark_completed(DMS_TASK_ARN, last_run_info['timestamp'])

    else: # first run or last run has already been marked as completed
        modified_on = datetime.datetime.now()

    if 'cdc_start_timestamp' in last_run_info:
        last_timestamp_start = last_run_info['cdc_start_timestamp'] # ex: '2019-08-01 00:00:00.000'
        last_timestamp_end = last_run_info['cdc_end_timestamp'] # ex: '2019-08-02 00:00:00.000'
        logger.info('last_timestamp_start: ' + last_timestamp_start)
        logger.info('last_timestamp_end: ' + last_timestamp_end)
    else:
        logger.info("Last successful cdc-tracker not found. First run or or last run has already been marked as completed")
        # One day ago. If today is 2019-09-18, then last_timestamp_end is '2019-09-17 00:00:00.000'
        last_timestamp_end = (date.today() - datetime.timedelta(days=1)).strftime(DATE_FORMAT) + ' 00:00:00.000'

    logger.info("Calculating next CDC timestamps")
    last_date_end = datetime.datetime.strptime(last_timestamp_end, DATETIME_FORMAT).date()
    next_datetime_start = datetime.datetime.combine(last_date_end, datetime.time.min)
    next_datetime_start_str = next_datetime_start.strftime(DATETIME_FORMAT)    
    logger.info('next_datetime_start_str: ' + next_datetime_start_str)
    
    # determine next end timestamp
    next_date_end = date.today()
    next_datetime_end_str = next_date_end.strftime(DATE_FORMAT) + ' 00:00:00.000'
    logger.info('next_datetime_end_str: ' + next_datetime_end_str)
    
    # subtract one milli from new start timestamp. This is used for updates in order to not bring the same inserts twice
    next_datetime_start_minus_one_milli = next_datetime_start - datetime.timedelta(milliseconds=1)
    next_datetime_start_minus_one_milli_str = next_datetime_start_minus_one_milli.strftime(DATETIME_FORMAT)    
    logger.info('next_datetime_start_minus_one_milli_str: ' + next_datetime_start_minus_one_milli_str)

    # each inserts and updates DMS task result will be stored in 'day' specific structure
    #  ex (inserts): */action=i/year=2019/month=9/day=11/LOAD00000001.parquet
    #  ex (updates): */action=u/year=2019/month=9/day=11/LOAD00000001.parquet
    CDC_PARTITION += '/year=' + str(next_date_end.year) + '/month=' + str(next_date_end.month) + '/day=' + str(next_date_end.day)
    logger.info(CDC_PARTITION)
  
    # Go through each table and modify DMS task table mappings
    i = 2
    table_mappings = copy.deepcopy(MAPPINGS)
    table_mappings['rules'][0]['value'] = CDC_PARTITION
    for dataset in datasets:
        # changing DMS task table mapping
        table_mapping = copy.deepcopy(TABLE)
        table_mapping['rule-id'] = str(i)
        table_mapping['rule-name'] = str(i)
        table_mapping['object-locator']['schema-name'] = dataset['source_schema']
        table_mapping['object-locator']['table-name'] = dataset['source_table']
        table_mapping['load-order'] = i * 10
        
        if task_type == 'inserts':
            if dataset['insert_timestamp'] is None:
                continue
            table_mapping['filters'][0]['column-name'] = dataset['insert_timestamp']
            table_mapping['filters'][0]['filter-conditions'][0]['start-value'] = next_datetime_start_str
            table_mapping['filters'][0]['filter-conditions'][0]['end-value'] = next_datetime_end_str
        else:
            if dataset['update_timestamp'] is None:
                continue
            table_mapping['filters'][0]['column-name'] = dataset['update_timestamp']
            table_mapping['filters'][0]['filter-conditions'][0]['start-value'] = next_datetime_start_str
            table_mapping['filters'][0]['filter-conditions'][0]['end-value'] = next_datetime_end_str
            table_mapping['filters'][1]['column-name'] = dataset['insert_timestamp']
            table_mapping['filters'][1]['filter-conditions'][0]['value'] = next_datetime_start_minus_one_milli_str

        table_mappings['rules'].append(table_mapping)
        i += 1
        # end of loop

    logger.info(json.dumps(table_mappings, indent=2))

    modify_dms_replication_task(DMS_TASK_ARN, table_mappings)
    save_current_run_info(DMS_TASK_ARN, DMS_TASK_ID, next_datetime_start_str, next_datetime_end_str)

    logger.info("Getting DMS Task status, until it's ready to be started")
    status = get_dms_task_info(DMS_TASK_ID, 'Status')
    while status != 'stopped' and status != 'ready':
        time.sleep(2)
        status = get_dms_task_info(DMS_TASK_ID, 'Status')

    # start DMS task
    start_replication_task(DMS_TASK_ARN)
    return {'statusCode': 200, 'body': 'Timestamp based DMS task started'}


if __name__ == "__main__":
    event = {"task_type": "inserts"}
    # event = {"task_type": "updates"}
    lambda_handler(event, '')