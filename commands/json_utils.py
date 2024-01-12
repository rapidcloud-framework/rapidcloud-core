# #!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import json
import logging

logger = logging.getLogger(__name__)

def flatten(items, sub_item_name, exclude_cols=[], fully_qualify_nested=False):

    # items example below
    # sub_item_name = "params"
    # exclude_cols (do not bring these columns into root)
    # fully_qualify_nested = prefix nested field with sub_item_name

    # {
        # "profile": "kc_100_qa",
        # "fqn": "kc_100_qa_lambda_test1",
        # "cmd_id": "20221109165825233907",
        # "command": "create",
        # "env": "kc_100_qa",
        # "lambda_enable_trend": false,
        # "lambda_env_vars": "{\\\"k1\\\":\\\"v1\\\"}",
        # "lambda_memory_size": "128",
        # "lambda_schedule": "0 4 * * ? *",
        # "lambda_timeout": "120",
        # "lambda_trend_app_security_group": "test1",
        # "mode": "console",
        # "module": "lambda",
        # "name": "test1",
        # "params": {
            # "profile": "kc_100_qa",
            # "fqn": "kc_100_qa_lambda_test1",
            # "cmd_id": "20221011171055632911",
            # "command": "create",
            # "env": "kc_100_qa",
            # "id": "test1",
            # "lambda_add_default_layers": "no",
            # "lambda_enable_trend": "false",
            # "lambda_env_vars": "{\\\"k1\\\":\\\"v1\\\"}",
            # "lambda_memory_size": "128",
            # "lambda_name": "test1",
            # "lambda_schedule": "0 4 * * ? *",
            # "lambda_timeout": "120",
            # "lambda_trend_app_security_group": "test1",
            # "mode": "console",
            # "module": "lambda",
            # "name": "test1",
            # "refresh_status": "True",
            # "timestamp": "2022-10-11 17:10:55.721975"
        # },
        # "refresh_status": "True",
        # "timestamp": "2022-11-09 16:58:25.353772"
    # }
    for item in items:
        # get out if sub_item_name (e.g. "params") is not in the dict
        if sub_item_name not in item:
            return item

        # remove all exclude_cols from "params"
        for col in exclude_cols:
            if col in item[sub_item_name]:
                del item[sub_item_name][col]

        # prefix all nested cols with sub_item_name (e.g. "params.colname")
        if fully_qualify_nested:
            for k,v in item[sub_item_name].items():
                item[f"{sub_item_name}.{k}"] = v
        else:
            for k,v in item[sub_item_name].items():
                # do not overwrite if col already exists in root
                if k not in item or "command" in item and item["command"] == "filestorage_create_stack" and "trendmicro_" in k:
                    item[k] = v
        # remove nested sub_item_name (e.g. "params")
        item.pop(sub_item_name)
    return items


if __name__ == "__main__":
    body = [{
        "action": "verify",
        "feature": "status",
        "command": None,
        "email": "iroyzis@kinect-consulting.com",
        "domain": None,
        "phone": "(305) 968-8160",
        "token": None,
        "tier": None,
        "hostname": "Igors-MacBook-Pro-2.local",
        "config": {
            "email": "iroyzis@kinect-consulting.com",
            "phone": "(305) 968-8160",
            "default_region": "us-east-1",
            "tier": "3",
            "aws_profile": "default",
            "hostname": "Igors-MacBook-Pro-2.local",
            "ipaddr": "127.0.0.1",
            "timestamp": "2022-08-24 10:38:34.582734",
            "env": "kc_tm_1"
        },
        "extra_params": {
            "one": "value1"
        },
        "env": "dev"
    }]
    
    body_flat = copy.deepcopy(body)
    print(json.dumps(flatten(body, "config", fully_qualify_nested=True), indent=2))
    print(json.dumps(flatten(body, "extra_params", fully_qualify_nested=True), indent=2))