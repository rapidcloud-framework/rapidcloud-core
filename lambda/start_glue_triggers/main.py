__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import sys
import json
import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_PROFILE = os.environ['AWS_PROFILE']
DMS_TASK_CDC_UPDATES = AWS_PROFILE + '-dms-task-cdc-updates'
GLUE_TRIGGER_MAIN = AWS_PROFILE + '.glue-trigger-main'
GLUE_TRIGGER_CDC_PREFIX = AWS_PROFILE + '.glue-trigger-cdc'

def init(lamda_mode):
    global dms_client
    global glue_client

    if lamda_mode:
        session = boto3.Session()
    else:
        session = boto3.Session(profile_name=AWS_PROFILE)

    dms_client = session.client('dms')
    glue_client = session.client('glue')


def get_cdc_triggers():
    global cdc_count
    response = glue_client.list_triggers()
    cdc_count = 0
    for trigger in response['TriggerNames']:
        if GLUE_TRIGGER_CDC_PREFIX in trigger:
            cdc_count += 1

    logger.info('CDC Count: ' + str(cdc_count))        
    return response
        

def get_dms_task_info(dms_task_id):
    response = dms_client.describe_replication_tasks(
        Filters = [{'Name': 'replication-task-id', 'Values': [dms_task_id]}]
    )
    logger.info(response)
    return response

def start_glue_triggers():
    logger.info("starting trigger: " + GLUE_JOB_PREFIX + GLUE_TRIGGER_MAIN)
    response = dms_client.start_trigger(Name = GLUE_TRIGGER_MAIN)
    logger.info(response)

    for i in range(1, cdc_count + 1): 
        TRIGGER_NAME = GLUE_TRIGGER_CDC_PREFIX + '-' + str(i)
        logger.info("starting trigger: " + TRIGGER_NAME)
        response = dms_client.start_trigger(Name = TRIGGER_NAME)
        logger.info(response)

def lambda_handler(event, context):
    logger.info('Input event: ' + json.dumps(event, indent=4, sort_keys=True))

    init(True) # lambda mode

    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info('Event message: ' + json.dumps(message, indent=4, sort_keys=True))

    id_link = str(message['Identifier Link'])
    index = id_link.index('SourceId') + 9
    dms_task_id = id_link[index:].strip()
    event = message['Event Message']

    dms_task_info = get_dms_task_info(dms_task_id)['ReplicationTasks'][0]  
    logger.info('DMS task info: ')
    logger.info(dms_task_info)

    arn = dms_task_info['ReplicationTaskArn']
    status = dms_task_info['Status']
    created_on = dms_task_info['ReplicationTaskCreationDate']
    started_on = dms_task_info['ReplicationTaskStartDate']
  
    logger.info('DMS task arn: ' + arn)
    logger.info('DMS task status: ' + status)
    logger.info('DMS task created_on: ' + str(created_on))
    logger.info('DMS task started_on: ' + str(started_on))

    if status.lower() in ['stopped', 'ready']: 
        if dms_task_id == DMS_TASK_CDC_UPDATES:
            # Message : Replication task has stopped. Stop Reason FULL_LOAD_ONLY_FINISHED.
            if 'FULL_LOAD_ONLY_FINISHED' in event:
                # trigger small tables refresh and all CDC jobs
                start_glue_triggers()   


# ----------------------------------------------------
# testing 
# ----------------------------------------------------
def main():
    init(False) # not lambda mode

    response = get_cdc_triggers()
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()

