__author__ = "Igor Royzis"
__license__ = "MIT"


import sys
import json
import boto3
import logging
import os
import time
import datetime
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger("metadata")
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

session = boto3.Session()
dynamodb_resource = session.resource('dynamodb')


def json_converter(obj):
    return str(obj)


def get_property(key):
    return dynamodb_resource.Table('property').query(
        KeyConditionExpression=Key('profile').eq(PROFILE) & Key('name').eq(key)
    )['Items'][0]['value']


def get_properties(key_suffix):
    items = dynamodb_resource.Table('property').scan(
        FilterExpression=Attr('profile').eq(PROFILE) & Attr('name').begins_with(key_suffix)
    )['Items']
    props = {}
    for item in items:
        props[item['name']] = item['value']
    return props


def scan(table, filters=None):
    if filters is None:
        return dynamodb_resource.Table(table).scan(        
            FilterExpression=Attr('profile').eq(PROFILE) 
        )['Items']
    else:
        filter_expression = Attr('profile').eq(PROFILE)
        for key in filters:
            filter_expression = filter_expression & Attr(key).eq(filters[key])
        return dynamodb_resource.Table(table).scan(        
            FilterExpression=filter_expression
        )['Items']


def query(table, key_attr, key_value):
    return dynamodb_resource.Table(table).query(
        KeyConditionExpression=Key(key_attr).eq(key_value)
    )['Items']


def put_item(table, item):
    response = dynamodb_resource.Table(table).put_item(Item=item)
    logger.info(json.dumps(item, indent=2, default=json_converter))
    logger.info(json.dumps(response, indent=2))


def get_cdc_log(key):
    items = query("cdc_log", "fqn", key)
    if items:
        return items[0]
    return None


def is_file_loaded(key):
    items = query("cdc_log", "fqn", key)
    if items and items[0]['status'] == 'processed':
        return True
    return False


def mark_file(bucket, key, dataset_name, job_name, status, destination=[], dataset_status={}, error_msg=None):
    fqn = f"s3://{bucket}/{key}"
    items = query("cdc_log", "fqn", fqn)
    if items:
        item = items[0]
        item['status'] = status
        item['update_timestamp'] = str(datetime.now())
        item['job_name'] = job_name
        item['destination'] = destination
        if dataset_status:
            item['dataset_status'][dataset_name] = dataset_status
        if error_msg is not None:
            item['error_msg'] = error_msg
    else:
        env = bucket[0:bucket.rindex("-")].replace("-","_")
        item = {
            "fqn": fqn,
            "profile": env,
            "cdc_s3_bucket": bucket,
            "cdc_s3_key": key,
            "cdc_s3_file": '',
            "source_database": 'n/a',
            "source_schema": 'n/a',
            "dataset_name": dataset_name,
            "dataset_status": dataset_status,
            "cdc_action": 'n/a',
            "job_name": job_name,
            "cdc_timestamp": str(datetime.now()),
            "status": status,
            "update_timestamp": str(datetime.now())            
        }
    put_item("cdc_log", item)
    return item


def get_transform_log(fqn):
    items = query("transform_log", "fqn", fqn)
    logger.info(json.dumps(items, indent=2, default=json_converter))
    if items:
        return items[0]
    return None


def start_transform(env, dataset_name, job_name, job_arguments):
    fqn = f"{env}_{dataset_name}_{time.time() * 1000}"
    item = {
        "fqn": fqn,
        "profile": env,
        "dataset_name": dataset_name,
        "job_name": job_name,
        "job_arguments": job_arguments,
        "status": "started",
        "update_timestamp": str(datetime.now())            
    }
    put_item("transform_log", item)  
    return item


def update_transform(fqn, status, destination=[], error_msg=None):
    items = query("transform_log", "fqn", fqn)
    if items:
        item = items[0]
        item['status'] = status
        item['update_timestamp'] = str(datetime.now())
        item['destination'] = destination
        if error_msg is not None:
            item['error_msg'] = error_msg
    put_item("transform_log", item)  
    return item


def get_publish_log(fqn):
    items = query("publish_log", "fqn", fqn)
    logger.info(json.dumps(items, indent=2, default=json_converter))
    if items:
        return items[0]
    return None


def start_publish(env, dataset_name, job_name, job_arguments):
    fqn = f"{env}_{dataset_name}_{time.time() * 1000}"
    item = {
        "fqn": fqn,
        "profile": env,
        "dataset_name": dataset_name,
        "job_name": job_name,
        "job_arguments": job_arguments,
        "status": "started",
        "update_timestamp": str(datetime.now())            
    }
    put_item("publish_log", item)  
    return item


def update_publish(fqn, status, destination=[], error_msg=None):
    items = query("publish_log", "fqn", fqn)
    if items:
        item = items[0]
        item['status'] = status
        item['update_timestamp'] = str(datetime.now())
        item['destination'] = destination
        if error_msg is not None:
            item['error_msg'] = error_msg
    put_item("publish_log", item)  
    return item


def get_modules(module=None, command=None, name=None):
    table = dynamodb_resource.Table('metadata')
    filters = Key('profile').eq(PROFILE)
    if module:
        filters = filters & Attr('module').eq(module)
        if command is not None:
            filters = filters & Attr('command').eq(command)
        if name is not None:
            filters = filters & Attr('name').eq(name)
        items = table.scan(FilterExpression=filters)['Items']            
    else:
        items = table.query(KeyConditionExpression=filters)['Items']
    return items


def get_aws_infra():
    table = dynamodb_resource.Table("aws_infra")
    filters = Attr('profile').eq(PROFILE)
    response = table.scan(FilterExpression=filters)
    aws_infra = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=filters, 
            ExclusiveStartKey=response['LastEvaluatedKey'])
        aws_infra.extend(response['Items'])
    return aws_infra
