#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import copy

def get_nested(data, list_field):
    new_data = []
    for item in data:
        # example list_field: params.lambda_integrations
        nested_list = None
        for field in list_field.split("."):
            if nested_list is None:
                nested_list = item[field]
            else:
                nested_list = nested_list[field]
        if nested_list:
            for list_item in nested_list:
                nested_item = copy.deepcopy(item)
                for k,v in list_item.items():
                    nested_item[f"{list_field.split('.')[-1]}.{k}"] = v
                new_data.append(nested_item)

        else:
            new_data.append(item)
    return new_data
