#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import logging
import os
from commands.kc_metadata_manager.azure_metadata import Metadata
from server.utils.azure_environment_utils import AzureConfigUtils
from typing import TypedDict

logger = logging.getLogger("azure_metadata_utils")
logger.setLevel(logging.INFO)


def get_metadata_manager(session):
    logger.info(f"Getting Azure metadata manager for {session['env']}")
    config = AzureConfigUtils.get_azure_environment_config(session['env'])
    args = {}
    if config is not None:
        for e in config:
            #setattr(args, e, config[e])
            args[e] = config[e]
    #setattr(args, 'cloud', 'azure')
    #setattr(args, 'env', 'session["env"]')
    args['cloud'] = "azure"
    args['env'] = session['env']
    args['mode'] = "console"
    metadata = Metadata(args)
    return metadata

def get_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    logger.info("in azure_metadata_utils.get_data")

    env = params.get("env")
    table_name = params.get("table_name")
    extra_filters = {}

    filter_expr = None
    if env and table_name != 'profile':
        extra_filters.update({"profile":env})
        if filters:
            for filter_name, filter_value in filters["filters"].items():
                extra_filters.update({filter_name:filter_value})
                # if isinstance(filter_value, list):
                #     filter_expr = filter_expr & Attr(filter_name).is_in(filter_value)
                # else:
                #     filter_expr = filter_expr & Attr(filter_name).eq(filter_value)

    # elif filters:
    #     filter_name = list(filters["filters"].keys())[0]
    #     filter_expr = Attr(filter_name).is_in(filters["filters"][filter_name])

    # get data        
    return get_metadata_manager(session).search_items(table_name,extra_filters)


def get_paginated_data_info(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    # TODO
    logger.warning("get_paginated_data_info has not been implemented for Azure")
    return {}


def get_paginated_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    # TODO
    logger.warning("get_paginated_data has not been implemented for Azure")
    return {}


def get_form_data(session, request, filters, params, dev_or_live, email=None, args=None):
    logger.info("in azure_metadata_utils.get_form_data")
    tables = request.args['type'].split('|')
    field = request.args.get('field', None)
    data = []
    for table_name in tables:
        logger.debug(f"getting data from {table_name}")

        if table_name != 'profile' and 'env' in request.args:
            extra_filters = {"profile", request.args['env']}

        if filters:
            for k,v in filters['filters'].items():
                extra_filters.update({k:v})

        if table_name == 'profile':
            profiles = get_all_environments(session)
            data_temp = []
            if field:
                for item in profiles:
                    data_temp.append({key: item[key] for key in item.keys() & dict.fromkeys(f"{field},enabled".split(","))})
            else:
                data_temp = profiles
            data = data + data_temp
        elif field:
        #     data = data + scan_dynamodb(table, filter_expr, cols=f"{field},enabled")
        # else:
            data = data + get_metadata_manager(session).search_items(table_name, extra_filters)

    return data

def get_all_environments(session, kc_args: None):
    logger.info("in azure_metadata_utils.get_all_envs")
    all_azure_envs = AzureConfigUtils.get_all_azure_environments()
    and_filters = {"enabled":True}
    data = []
    or_filters = []
    if all_azure_envs:
        for env, subscription in all_azure_envs.items():
            or_filters.append({"name":env, "subscription":subscription})
    data.extend(get_metadata_manager(session).search_items("profile", and_filters, or_filters))
        
    return data

def get_environment_info(session):
    logger.info("in azure_metadata_utils.get_environment_info")
    return get_metadata_manager(session).search_items("profile", {"name": session['env']})[0]

def get_environment(env, session):
    logger.info("in azure_metadata_utils.get_environment")
    return get_metadata_manager(session).search_items("azure_infra", {"profile": env})
