#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"



import logging

logger = logging.getLogger("custom_server")
logger.setLevel(logging.INFO)

def example_data():
    return [{
        "name": "example"
    }]

def custom_endpoint(action, params, boto3_session, user_session):
    logger.info(f"action={action}")
    
    if action == "example":
        return example_data()
    # TODO add custom actions here
    # elif action == "some_custom_action":
    #     return some_custom_action_function()
    

    return None
