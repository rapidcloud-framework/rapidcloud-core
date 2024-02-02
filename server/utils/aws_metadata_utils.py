#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import logging
from csv import reader

import numpy as np
import pandas as pd
from boto3.dynamodb.conditions import Attr
from commands import boto3_utils
from commands.cli_worker.license_worker import LicenseWorker
from commands.kc_metadata_manager.aws_profile import Profile

PAGE_LIMIT = 100

logger = logging.getLogger("aws_metadata_utils")
logger.setLevel(logging.INFO)


def dynamodb_resource(session):
    boto_session = boto3_utils.get_boto_session(region=session.get("region"), aws_profile=session.get("aws_profile"), x_acct_role_arn=session.get("x_acct_role_arn"), env_info=session.get("env_info"))
    if boto_session:
        return boto_session.resource('dynamodb')
    return None


def scan_dynamodb(table, filter_expr, cols="all"):
    if filter_expr:
        response = table.scan(FilterExpression=filter_expr)
    else:
        response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        last_key = response['LastEvaluatedKey']
        if filter_expr:
            response = table.scan(FilterExpression=filter_expr, ExclusiveStartKey=last_key)
        else:
            response = table.scan(ExclusiveStartKey=last_key)
        data.extend(response['Items'])

    logger.debug(f"scan size: {len(data)}")
    result = []
    if cols != "all":
        for item in data:
            result.append({key: item[key] for key in item.keys() & dict.fromkeys(cols.split(","))})
        data = result

    return data


def get_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    try:
        env = params.get("env")
        table_name = params.get("table_name", params.get("type"))
        cols = params.get("cols")

        filter_expr = None
        if env and table_name != 'profile':
            filter_expr = Attr('profile').eq(env)
            if filters:
                for filter_name, filter_value in filters["filters"].items():
                    if isinstance(filter_value, list):
                        filter_expr = filter_expr & Attr(filter_name).is_in(filter_value)
                    else:
                        filter_expr = filter_expr & Attr(filter_name).eq(filter_value)

        elif table_name == 'profile':
            return get_all_environments(session, kc_args)
        elif table_name == 'kc_activation':
            return [LicenseWorker(kc_args).contact_lic_server("get_activation")]
        elif filters:
            filter_name = list(filters["filters"].keys())[0]
            filter_expr = Attr(filter_name).is_in(filters["filters"][filter_name])

        # get data
        table = dynamodb_resource(session).Table(table_name)
        data = scan_dynamodb(table, filter_expr, cols)
    except AttributeError as e:
        logger.error(f"error getting data {e} returning empty list")
        data = []

    return data


def filter_data_by_keyword(data, request, params):
    search = request.args.get("search", None)
    if search is not None:
        logger.info(f"{params['table_name']}, size={len(data)}")
        df = pd.DataFrame.from_dict(data)
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        df = df.replace(np.nan, '', regex=True)
        data = df.to_dict('records')
    return data


def get_paginated_data_info(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    data = get_data(kc_args, session, request, filters, params, dev_or_live, email, args)
    data = filter_data_by_keyword(data, request, params)
    size = len(data)
    result = {
        "table_name": params['table_name'],
        "size": size,
        "limit": PAGE_LIMIT
    }
    # sort if requested
    sort_by = request.args.get("sort_by", None)
    if sort_by:
        sort_order = request.args.get("sort_order", None)
        if sort_order is None:
            sort_order = "asc"
        data.sort(key=lambda x: x[sort_by], reverse=sort_order=="desc")

    # save data in the session, because next client call is for this data
    session["cached_data"] = copy.copy(result)
    session["cached_data"]["data"] = data

    logger.info(json.dumps(result, indent=2))
    # logger.info(json.dumps(data[0], indent=2, default=str))
    return result


def get_paginated_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    # data = get_data(kc_args, session, request, filters, params, dev_or_live, email, args)
    # data = filter_data_by_keyword(data, request, params)
    if "cached_data" not in session or session["cached_data"] is None:
        get_paginated_data_info(kc_args, session, request, filters, params, dev_or_live, email, args)

    data = session["cached_data"]["data"]
    start = int(request.args.get('start','1')) - 1
    search = request.args.get("search", None)
    size = len(data)
    limit = PAGE_LIMIT if size - start > PAGE_LIMIT else size - start
    logger.info(f"{params['table_name']}, size={size}, start={start}, limit={limit}, search={search}")
    page = data[start:start+limit]
    return page


def get_form_data(session, request, filters, params, dev_or_live, kc_args):
    tables = request.args['type'].split('|')
    field = request.args.get('field', None)
    fields = request.args['field'].split(',') if field else []
    field_prefix = request.args.get('field_prefix', "")

    # data fields to return with each select option
    data_fields = []
    if "data_fields" in request.args:
        data_fields = request.args["data_fields"].split(',')
    if fields:
        data_fields = data_fields + fields
    if tables[0] != 'metadata':
        data_fields.append("enabled")

    data = []
    for table_name in tables:
        logger.info(f"getting data from {table_name}")
        table = dynamodb_resource(session).Table(table_name)

        filter_expr = None
        if table_name != 'profile' and 'env' in request.args:
            filter_expr = Attr('profile').eq(request.args['env'])

        if filters:
            for k,v in filters['filters'].items():
                if filter_expr:
                    filter_expr = filter_expr & Attr(k).eq(v)
                else:
                    filter_expr = Attr(k).eq(v)

        if table_name == 'profile':
            profiles = get_all_environments(session, kc_args)
            data_temp = []
            if field:
                for item in profiles:
                    data_temp.append({key: item[key] for key in item.keys() & dict.fromkeys(f"{field},enabled".split(","))})
            else:
                data_temp = profiles
            data = data + data_temp
        elif len(data_fields) > 0:
            data = data + scan_dynamodb(table, filter_expr, cols=",".join(data_fields))
        else:
            data = data + scan_dynamodb(table, filter_expr)

    return data

def get_environment_info(session):
    # logger.info(f"get env info: {session}")
    try:
        table = dynamodb_resource(session).Table('profile')
        resp = scan_dynamodb(table, filter_expr = Attr('name').eq(session['env']))
        if len(resp) > 0:
            return resp[0]
        else:
            return {}
    except AttributeError as e:
        ### TODO moti
        logger.error(f"could not get profile table {e}")
        return {}

def get_environment(env, session):
    try:
        table = dynamodb_resource(session).Table('aws_infra')
        return scan_dynamodb(table, filter_expr = Attr('profile').eq(env))
    except AttributeError as e:
        ### TODO moti
        logger.error(f"could not get aws_infra table {e}")
        return {}

def get_status(env, session):
    # get latest AWS infra state for this env
    logger.info("getting status...")
    logger.info({session})
    table = dynamodb_resource(session).Table('aws_infra')
    aws_infra = scan_dynamodb(table, filter_expr = Attr('profile').eq(env))
    aws_infra = [{k: v for k, v in d.items() if k != 'command_arguments'} for d in aws_infra]

    status_by_res = {}
    with open(f"./config/environments/{env}_status.csv", 'r') as status_file:
        csv_reader = reader(status_file)
        for row in csv_reader:
            status_by_res[f"{row[1]}.{row[2]}"] = row[0]

    for item in aws_infra:
        k = f"{item['resource_type']}.{item['resource_name']}"
        item['created'] = status_by_res[k] if k in status_by_res else "?"

    aws_infra.sort(key=lambda x: x["resource_type"])
    logger.info(f"get_status {aws_infra}")
    return aws_infra


def get_all_environments(session, kc_args):
    return Profile(kc_args).get_all_profiles()

