# #!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import logging

logger = logging.getLogger(__name__)

def flatten(items, sub_item_name, exclude_cols=[], fully_qualify_nested=False):
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
