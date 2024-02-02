#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging

from server.utils import aws_metadata_utils, azure_metadata_utils, gcp_metadata_utils, cloud_metadata_utils

logger = logging.getLogger("generic_metadata_utils")
logger.setLevel(logging.INFO)


def get_data(kc_args, session, request, dev_or_live, email=None, args=None):
    filters, params = parse_filters(request)
    return cloud_metadata_utils.get_data(kc_args, session, request, filters, params, dev_or_live, email, args)


def get_form_data(session, request, dev_or_live, kc_args):
    filters, params = parse_filters(request)
    return cloud_metadata_utils.get_form_data(session, request, filters, params, dev_or_live, kc_args)


def get_paginated_data_info(kc_args, session, request, dev_or_live, email=None, args=None):
    filters, params = parse_filters(request)
    return cloud_metadata_utils.get_paginated_data_info(kc_args, session, request, filters, params, dev_or_live, email, args)


def get_paginated_data(kc_args, session, request, dev_or_live, email=None, args=None):
    filters, params = parse_filters(request)
    return cloud_metadata_utils.get_paginated_data(kc_args, session, request, filters, params, dev_or_live, email, args)


def parse_filters(request, args=None):
    filters = None
    filter_names, filter_values, result = None, None, None
    if not args and 'filter_name' in request.args:
        filter_names = request.args['filter_name'].split(",")
        if 'filter_value' in request.args:
            filter_values = request.args['filter_value'].split(",")
        if 'result' in request.args:
            result = request.args['result']
    elif args:
        if args.filter_name is not None:
            filter_names = args.filter_name.split(",")
            if args.filter_value is not None:
                filter_values = args.filter_value.split(",")
            if args.result is not None:
                result = args.result

    if filter_names:            
        filters = {
            "filters": {},
            "result": result.split(",") if result else []
        }

        def get_filter_value(filter_value):
            if filter_value == "True":
                filter_value = True
            elif filter_value == "False":
                filter_value = False
            return filter_value

        if len(filter_names) == len(filter_values):
            for i in range(len(filter_names)):
                filters["filters"][filter_names[i]] = get_filter_value(filter_values[i])
        else:
            filters["filters"][filter_names[0]] = get_filter_value(filter_values)
    
    if filters is not None:
        logger.info(json.dumps(filters, indent=2))

    # parameters
    if not args: # call via HTTP
        via_http = True
        flatten = request.args.get('flatten', "true") == "true"
        env = request.args['env'] if 'env' in request.args else None
        table_name = request.args['type'] if 'type' in request.args else "metadata"
        cols = "all"
    else: # call via CLI
        via_http = False
        flatten = True
        env = args.env if hasattr(args, 'env') else None 
        table_name = args.type if args.type else "metadata"
        if table_name == 'metadata' and not args.cols:
            cols = "module,command,name,timestamp,cmd_id"
        else:
            cols = args.cols if args.cols else "all"

    params = {
        "via_http": via_http,
        "flatten": flatten,
        "env": env,
        "table_name": table_name,
        "cols": cols
    }

    logger.debug(json.dumps(params, indent=2))

    return filters, params
