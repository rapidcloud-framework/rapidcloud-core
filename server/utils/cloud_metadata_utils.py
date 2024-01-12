#!/usr/bin/env python3

__author__ = "Sridhar Kammadanam"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import json
import logging
import os
from csv import reader
from commands.cli_worker.license_worker import LicenseWorker
from commands.cli_worker.provider import Provider
from server.utils import azure_metadata_utils, aws_metadata_utils, nested_json_utils
from commands import json_utils

logger = logging.getLogger("cloud_metadata_utils")
logger.setLevel(logging.INFO)

def get_provider(session):
    if session["cloud"] == "azure":
        return azure_metadata_utils
    elif session["cloud"] == "aws":
        return aws_metadata_utils

def get_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    via_http = params.get("via_http")
    flatten = params.get("flatten")
    table_name = params.get("table_name", params.get("type"))

    if table_name == 'profile':
        return get_all_environments(session, kc_args)
    
    elif table_name == 'kc_activation':
        return [LicenseWorker(kc_args).contact_lic_server("get_activation")]

    else:
        data = get_provider(session).get_data(kc_args, session, request, filters, params, dev_or_live, email, args)
        if len(data) == 0:
            return data
    
    # trim data if "result" parameter is provided
    if filters and filters["result"]:
        # only expecting one item back
        item = data[0]
        # logger.info(item)
        for result in filters["result"]:
            if result in item:
                item = item[result]
            else:
                item = None
            # logger.info(item)
        if item:
            data = json.loads(item.replace("\\","")) if type(item) == str else item
        else:
            data = {}

    # split each item into multiple based on nested_list parameter
    if "list_field" in request.args:
        data = nested_json_utils.get_nested(data, request.args["list_field"])

    # remove unnecessary variabbles from data
    if table_name == "aws_infra":
        data = [{k: v for k, v in d.items() if k != 'command_arguments'} for d in data]
        if via_http and 'params' in request.args and len(data) > 0:
            data = data[0]['params'][request.args['params']]
        if "field" in request.args:
            for item in data:
                v = item
                for fld in request.args['field_value'].split('.'):
                    v = v[fld]
                item[request.args['field']] = v
        data.sort(key=lambda x: x["resource_type"])

    elif table_name == 'profile':
        data.sort(key=lambda x: x["name"])

    elif table_name == 'metadata' and flatten:
        # flatten params and add CLI command
        if via_http and 'result' not in request.args:
            data = json_utils.flatten(data, 'params', exclude_cols=['cmd_id'])

    # rename "id" to "_id" - console is breaking "id" field
    if via_http and 'result' not in request.args:
        if len(data) > 0 and "id" in data[0].keys():
            for item in data: 
                if "id" in item:
                    item["_id"] = item.pop("id")

    return data


def get_paginated_data_info(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    # TODO add access to relational databases

    # default behavior is to get data from cloud native NoSQL (Dynamodb, Cosmos DB, Firestore)
    data = get_provider(session).get_paginated_data_info(kc_args, session, request, filters, params, dev_or_live, email, args)
    return data


def get_paginated_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    # TODO add access to relational databases
    
    # default behavior is to get data from cloud native NoSQL (Dynamodb, Cosmos DB, Firestore)
    data = get_provider(session).get_paginated_data(kc_args, session, request, filters, params, dev_or_live, email, args)
    return data


def get_form_data(session, request, filters, params, dev_or_live, kc_args):

    data = get_provider(session).get_form_data(session, request, filters, params, dev_or_live, kc_args)

    tables = request.args['type'].split('|')
    field = request.args.get('field', None)
    fields = request.args['field'].split(',') if field else []
    field_prefix = request.args.get('field_prefix', "")
    
    if field_prefix and len(data) > 0:
        for col in data[0].keys():
            if field_prefix in col and col not in fields:
                fields.append(col)
            elif col == 'params' and request.args['type'] == 'metadata':
                for param_col in data[0]['params'].keys():
                    if field_prefix in param_col and param_col not in fields:
                        fields.append(param_col)

    if len(fields) == 1:
        data.sort(key=lambda x: x[field])

    response = []
    default_option = request.args.get('default_option', None)
    if default_option:
        response.append({
            "type": "Theia::Option",
            "label": default_option,
            "value": {
                "type": "Theia::DataOption",
                "data": default_option,
                "value": default_option
            }
        })
    for elem in data:
        if tables[0] != 'profile' or tables[0] == 'profile' and 'enabled' in elem and elem['enabled']:
            for field in fields:
                value = elem[field] if not field_prefix else field.replace(field_prefix, '')
                response.append({
                    "type": "Theia::Option",
                    "label": value,
                    "value": {
                        "type": "Theia::DataOption",
                        "data": elem,
                        "value": value
                    }
                })
    return response

def get_status(env, session, kc_args):
    # get latest AWS infra state for this env
    logger.info("getting status...")
    cloud_infra = get_provider(session).get_environment(env, session)
    cloud_infra = [{k: v for k, v in d.items() if k != 'command_arguments'} for d in cloud_infra]

    status_by_res = {}
    env_status_file = f"./config/environments/{env}_status.csv"
    if not os.path.exists(env_status_file):
        # refresh status if CSV file not found
        setattr(kc_args, "env", env)
        setattr(kc_args, "cloud", session["cloud"])
        Provider(kc_args).get_infra().show_status()

    with open(env_status_file, 'r') as status_file:
        csv_reader = reader(status_file)
        for row in csv_reader:
            status_by_res[f"{row[1]}.{row[2]}"] = row[0]
    
    for item in cloud_infra:
        k = f"{item['resource_type']}.{item['resource_name']}"
        item['created'] = status_by_res[k] if k in status_by_res else "?"

    cloud_infra.sort(key=lambda x: x["resource_type"])
    return cloud_infra

def get_all_environments(session, kc_args):
    data = get_provider(session).get_all_environments(session, kc_args)
    data.sort(key=lambda x: x["name"])
    filtered_data = []
    curr_user = session["email"]
    for profile in data:
        if "wizard" in profile:
            profile.pop("wizard")
        if "diagram" in profile:
            profile.pop("diagram")
        created_by = profile["created_by"] if "created_by" in profile else profile["updated_by"]
        # logger.info(f"curr_user: {curr_user}, created_by: {created_by}")
        if created_by == "":
            profile["shared"] = True
            profile["shared_with"] = "all"
        # current user owns the environment
        show_env = created_by == curr_user

        if not show_env and profile.get("shared", True):
            # environment is shared with "all" or current user
            shared_with = profile.get("shared_with", "all")
            show_env = curr_user in shared_with or "all" in shared_with

        if show_env:
            profile["created_by"] = created_by
            filtered_data.append(profile)

    # console is expecting "account" and "vpc"
    if session["cloud"] in ["azure", "gcp"]:
        for profile in filtered_data:
            if session["cloud"] == "azure":
                profile["account"] = profile.get("subscription")
                profile["vpc"] = profile.get("vnet")
            else:
                profile["account"] = profile.get("project")
        
    return filtered_data


def get_environment_info(session):
    return get_provider(session).get_environment_info(session)
