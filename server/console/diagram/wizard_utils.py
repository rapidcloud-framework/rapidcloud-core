__author__ = "Igor Royzis"
__copyright__ = "Copyright 2021, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import re
import sys
import json
import datetime
import time
import logging
import os
import random


def get(file_name):
    with open(f'./server/console/diagram/{file_name}.json') as f:
        diagram_json = json.load(f)
        return diagram_json


def save(file_name, diagram):
    with open(f'./server/console/diagram/{file_name}_test.json', 'w') as f:
        json.dump(diagram, f, indent=2)


def init_wizard(file_name, num_icons):
    ids = []
    for i in range(1,num_icons):
        ids.append(i)
    wizard = [
        {
            "id": 1,
            "text": "Show All",
            "ids": ids
        }
    ]
    save(file_name, wizard)


if __name__ == "__main__":
    # python ./server/console/diagram/wizard_utils.py <action> <file_name> <num_icons>
    action = sys.argv[1]
    if action == "init":
        file_name = sys.argv[2]
        num_icons = int(sys.argv[3])
        init_wizard(file_name, num_icons)
