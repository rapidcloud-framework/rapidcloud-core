__author__ = "Igor Royzis"
__license__ = "MIT"


import logging
import os
import json


FILESYSTEM = "filesystem"
DYNAMODB = "dynamodb"

logger = logging.getLogger(__name__)

with open('config/kc_config.json') as f:
    config_storage = json.load(f).get("config_storage", FILESYSTEM)


def get_config(name):
    if config_storage == FILESYSTEM:
        filename = f"./config/{name}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            return {}
    else:
        logger.error(DYNAMODB + " config storage has not been implemented yet")


def save_config(name, config):
    if config_storage == FILESYSTEM:
        filename = f"./config/{name}.json"
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
    else:
        logger.error(DYNAMODB + " config storage has not been implemented yet")
