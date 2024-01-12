#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import sys
from boto3.dynamodb.conditions import Key, Attr

from commands import json_utils
from commands.modules.trendmicro import trend_api
from commands.modules.trendmicro import ModuleMetadata as TrendModule


logger = logging.getLogger("trend_utils")
logger.setLevel(logging.INFO)


def to_select_list(data, request, value_col='col'):
    response = []
    for item in data:
        if request.args['col'] in item:
            response.append({
              "type": "Theia::Option",
              "label": item[request.args['col']],
              "value": str(item[value_col])
            })
    return response


def get_trend_setup(boto3_session, user_session):
    trend_info = boto3_session.resource('dynamodb').Table("metadata").scan(
        FilterExpression=
            Attr('module').eq('trendmicro') & 
            Attr('command').eq('setup') & 
            Attr('profile').eq(user_session.get("env"))
    )['Items']
    if len(trend_info) > 0:
        env_trend_info = json_utils.flatten([trend_info[0]], 'params', exclude_cols=['cmd_id'])
        logger.info(json.dumps(env_trend_info, indent=2, default=str)) 
        for feature in ["trendmicro_enable_filestorage_security", 
                "trendmicro_enable_workload_security", 
                "trendmicro_enable_application_security"]:
            env_trend_info[0][feature] = env_trend_info[0][feature] == "true"
        return env_trend_info
    return {}


def get_trend_filestorage_stacks(request, boto3_session):
    env = request.args['env']
    # get RC stacks metadata
    table = boto3_session.resource('dynamodb').Table('metadata')
    filters = Key('profile').eq(env) & Attr('module').eq('trendmicro') & Attr('command').eq('filestorage_create_stack')
    rc_stacks = table.scan(FilterExpression=filters)['Items']

    # get Trend Micro Stacks
    tm_stacks = trend_api.call_api(env, trend_api.FILE_STORAGE_SECURITY, "GET", "stacks", boto3_session=boto3_session)
    rc_stacks = json_utils.flatten(rc_stacks, 'params', exclude_cols=['cmd_id'])
    for rc_meta in rc_stacks:
        rc_meta['cf_stack_name'] = ''
        if 'cf_stack' in rc_meta and 'stack_name' in rc_meta['cf_stack']:
            rc_meta['cf_stack_name'] = rc_meta['cf_stack']['stack_name']
        for tm_stack in tm_stacks['stacks']:
            if 'stackID' in rc_meta and rc_meta['stackID'] == tm_stack['stackID']:
                tm_stack = json_utils.flatten([tm_stack], 'details')[0]
                rc_meta['trendmicro_role_arn'] = tm_stack['managementRole']
                for k,v in tm_stack.items():
                    rc_meta[f'tm_fss_{k}'] = v

    return rc_stacks


def get_trend_application_groups(request, boto3_session):
    env = request.args['env']
    # get metadata
    table = boto3_session.resource('dynamodb').Table('metadata')
    filters = Key('profile').eq(env) & Attr('module').eq('trendmicro') & Attr('command').eq('application_create_group')
    metadata = table.scan(FilterExpression=filters)['Items']

    # get TM AS groups
    result = trend_api.call_api(env, trend_api.APPLICATION_SECURITY, "GET", "accounts/groups", boto3_session=boto3_session)
    # logger.info(json.dumps(result, indent=2, default=str))
    groups_by_name = {}
    for group in result:
        if env.upper() in group['name']:
            groups_by_name[group['name']] = group
    for item in metadata:
        group_name = f"{env}_{item['name']}".upper()
        if group_name in groups_by_name:
            for k,v in groups_by_name[group_name].items():
                item[f'tm_as_{k}'] = v
            for k,v in groups_by_name[group_name]['settings'].items():
                item[f'tm_as_{k}'] = v
    metadata = json_utils.flatten(metadata, 'params')
    # logger.info(json.dumps(metadata, indent=2, default=str))

    if len(metadata) > 0 and 'col' in request.args:
        metadata = to_select_list(metadata, request, value_col='trendmicro_name')
        # metadata = to_select_list(metadata, value_col='tm_as_group_id')

    return metadata


def get_trend_workload_groups(request, boto3_session):
    env = request.args['env']
    # get metadata
    table = boto3_session.resource('dynamodb').Table('metadata')
    filters = Key('profile').eq(env) & Attr('module').eq('trendmicro') & Attr('command').eq('workload_create_group')
    metadata = table.scan(FilterExpression=filters)['Items']

    # get TM Workload groups
    result = trend_api.call_api(env, trend_api.WORKLOAD_SECURITY, "GET", "computergroups", boto3_session=boto3_session)
    # logger.info(json.dumps(result, indent=2, default=str))
    groups_by_name = {}
    root_group = None
    for group in result['computerGroups']:
        if env.upper() in group['name']:
            groups_by_name[group['name']] = group
        if env.upper() == group['name']:
            root_group = group
    for item in metadata:
        group_name = f"{env}_{item['name']}".upper()
        if group_name in groups_by_name:
            for k,v in groups_by_name[group_name].items():
                item[f'tm_workload_{k}'] = v
    metadata = json_utils.flatten(metadata, 'params')

    # logger.info(json.dumps(metadata, indent=2, default=str))

    if len(metadata) > 0 and 'col' in request.args:
        # add root environment group
        metadata.insert(0, {
            "tm_workload_name": root_group['name'],
            "tm_workload_ID": root_group['ID']
        })
        metadata = to_select_list(metadata, request, value_col='tm_workload_ID')
        # allow to not select any group
        metadata.insert(0, {
            "type": "Theia::Option",
            "label": "Default (Computers)",
            "value": ""
        })

    return metadata


def get_trend_workload_policies(request, boto3_session, kc_args):
    policies = TrendModule(kc_args).workload_list_policies()
    if len(policies) > 0 and 'col' in request.args:
        for p in policies:
            p["ID"] = str(p["ID"])
            p["name"] = f"{p['name']} ({p['ID']})"
        select_list = to_select_list(policies, request, value_col='ID')
    return select_list