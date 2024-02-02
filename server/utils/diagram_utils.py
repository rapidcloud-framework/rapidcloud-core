#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import os
import re
import sys
from csv import reader

from boto3.dynamodb.conditions import Attr, Key
from commands import boto3_utils, general_utils
from server.utils import aws_metadata_utils

logging.basicConfig()
logger = logging.getLogger("diagram_utils")
logger.setLevel(logging.INFO)


def gen_diagram(session, request, diagram_type):
    env = request.args['env']
    # logger.info(f"gen_diagrams called with env: {env}")
    # logger.info(f"gen_diagrams called with session: {session}")
    # logger.info(f"-----------------------------------------")
    # for k,v in session['tenant'].items():
    #     logger.info(f"key : {k}")
    #     logger.info(f"{json.dumps(v, indent=2)}")
    # logger.info(f"-----------------------------------------")


    cloud = general_utils.get_cloud_from_args(request.args, session).lower()
    if cloud == "aws" and diagram_type == "solution":
        try:
            if session['env_info']['x_acct_role_arn'] or session['tenant']['x-acct-roles'][env]['role']:
                logger.info(f"gen_diagrams, found x-acct-role {session['tenant']['x-acct-roles'][env]['role']} -> {env}")
                boto3_session = boto3_utils.get_boto_session(x_acct_role_arn=session['tenant']['x-acct-roles'][env]['role'], env_info=session.get("env_info"))
        except KeyError:
            boto3_session = boto3_utils.get_boto_session(env_info=session.get("env_info"))

        return gen_aws_current_state(env, boto3_session)
    else:
        with open(f"./server/console/diagram/{cloud}_{diagram_type}_diagram.json") as f:
            diagram_json = json.load(f)
            return diagram_json


def get_default_wizard(cloud, diagram_type):
    file_name = f'./server/console/diagram/{cloud}_{diagram_type}_wizard.json'
    logger.info(f"getting default wizard from {file_name}")
    if os.path.exists(file_name):
        with open(file_name) as f:
            return json.load(f)


def gen_aws_current_state(env, boto3_session):
    dynamodb_resource = boto3_session.resource("dynamodb")

    # get latest AWS infra state for this env (output of `kc status`)
    curr_resources = {}
    with open(f"./config/environments/{env}_status.csv", 'r') as status_file:
        csv_reader = reader(status_file)
        next(csv_reader)
        for item in csv_reader:
            # Created,AWS Resource Type,Resource Name,Command,ID
            # no,sns_topic,publishing,rds,create,20221012162153717970
            exists, type, name, phase, command = item[0], item[1], item[2], item[3], item[4]
            fqn = f"{type}::{phase}::{name}".replace(f"{env}_",'').replace(f"{env}_".replace('_','-'),'')
            curr_resources[fqn] = exists == "yes"

    # default resources
    try:
        env_exists = curr_resources[f"kms_key::init::{env}"]
    except KeyError as e:
        env_exists = None
        logger.info(f"gen_diagram no kms key in environment yet")

    quarantine_bucket_exists = boto3_session.resource('s3').Bucket(f"{env}-quarantine".replace("_","-")).creation_date is not None
    dft_resources = {
        'secrets': env_exists,
        's3_trend_scan_bucket': quarantine_bucket_exists,
        'athena': env_exists
    }
    curr_resources.update(dft_resources)


    # add data type info
    env_filter = Attr('profile').eq(env)
    src_enabled = {
        "rdbms": {
            "table": "source_database"
        },
        "files": {
            "table": "dataset_semi_structured"
        },
        "media": {
            "table": "dataset_unstructured"
        },
        "src_kinesis": {
            "table": "stream",
            "filter": Attr('type').eq("kinesis")
        },
        "src_kafka": {
            "table": "stream",
            "filter": Attr('type').eq("kafka")
        },
        "spice": {
            "table": "transformation",
            "filter": Attr('refresh_spice').eq(True)
        }
    }
    for src_type, info in src_enabled.items():
        filters = env_filter
        if "filter" in info:
            filters = env_filter & info["filter"]
        data = dynamodb_resource.Table(info["table"]).scan(FilterExpression=filters)['Items']
        if len(data) > 0:
            curr_resources[src_type] = True


    # logger.info("\n\nEnvironment Resources\n")
    # for res in sorted(curr_resources.keys()):
    #     logger.info((f" {'+' if curr_resources[res] else '-'} {res}"))

    # check resources against each diagram icon
    with open('./server/console/diagram/aws_solution_diagram.json') as f:
        diagram_json = json.load(f)
        # logger.info("\n\nIcons\n")
        diagram_json['icons'].sort(key=lambda x: x["name"])
        for icon in diagram_json['icons']:
            match = False
            rx = icon['name'].replace('*', '.*').replace('all::', '.*')
            for res in curr_resources:
                # rds_*::rds::*
                # rds_.*::rds::.*
                # rds_postgresql_instance::rds::pg1
                if rx.split("::")[0].split("_")[0] in res.split("::")[0]:
                    match = re.fullmatch(rx, res)
                    if match:
                        icon['display'] = True
                        icon['active'] = res in curr_resources and curr_resources[res]
                        break

            # logger.info(f" {'+' if match else '-'} {rx}")

        return diagram_json


def gen_icons_json(env, save=True):
    with open('./server/console/diagram/diagram.json') as f:
        diagram_json = json.load(f)
        diagram_json['icons'].sort(key=lambda x: x["name"])
        icons = {}
        duplicates = []
        for icon in diagram_json['icons']:
            name = icon['name']
            name_ = icon['name'].replace('*', '.*').replace('all::', '.*')
            if name not in icons:
                icons[icon['name']] = {
                    "name": icon['name'],
                    "text": icon['text'],
                    "name_": name_,
                    "new_name": ""
                }
            else:
                duplicates.append(name)
        print(json.dumps(icons, indent=2, default=str))
        with open('./server/console/diagram/icons.json', 'w') as f1:
            f1.write(json.dumps(icons, indent=2, default=str))
        print(f"\n\nDuplicates: {duplicates}\n\n")
        return icons



def gen_resources_json(env, save=True):
    resources = {}
    with open(f"./config/environments/{env}_status.csv", 'r') as status_file:
        csv_reader = reader(status_file)
        next(csv_reader)
        for item in csv_reader:
            type = item[1]
            name = item[2]
            phase = item[4]
            fqn = f"{type}::{phase}::{name}".replace(f"{env}_",'').replace(f"{env}_".replace('_','-'),'')
            if type not in resources:
                resources[type] = {}
            resources[type][name] = {
                "fqn": fqn,
                "active": item[0] == "yes"
            }
        print("\n\nEnvironment Resources\n")
        print(json.dumps(resources, indent=2, default=str))
        with open('./server/console/diagram/resources.json', 'w') as f1:
            f1.write(json.dumps(resources, indent=2, default=str))
        return resources


if __name__=="__main__":
    action = sys.argv[1]
    env = sys.argv[2]

    if action == "gen_icons_json":
        gen_icons_json(env)
    elif action == "gen_resources":
        gen_resources_json(env)
