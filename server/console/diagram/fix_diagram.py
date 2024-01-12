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


def set_resource_type(file_name):
    diagram = get(file_name)
    for icon in diagram['icons']:
        icon['resource_type'] = ""
    save(file_name, diagram)


def move(file_name, up=0, right=0):
    print(f"moving diagram up by {up}")
    print(f"moving diagram right by {right}")
    diagram = get(file_name)
    for icon in diagram['icons']:
        icon['x'] = str(int(icon['x']) + right)
        icon['y'] = str(int(icon['y']) - up)
    for link in diagram['links']:
        for path in link['path']:
            path['x'] = str(int(path['x']) + right)
            path['y'] = str(int(path['y']) - up)
    save(file_name, diagram)


def stretch(file_name, up=0, right=0):
    print(f"moving Y up by {up}")
    print(f"moving X right by {right}")
    diagram = get(file_name)

    # stretch horizontally
    x, y = int(right), int(up)
    for icon in diagram['icons']:
        if icon['x'] != "0":
            icon['x'] = str(int(icon['x']) + x)
            x += 1
            if y != 0:
                icon['y'] = str(int(icon['y']) + y)
                y += 1

    # stretch vertically
    # x, y = int(right), int(up)
    # for link in diagram['links']:
    #     for path in link['path']:
    #         if path['x'] != "0":
    #             path['x'] = str(int(path['x']) + x)
    #             x += 1
    #             if y != 0:
    #                 path['y'] = str(int(path['y']) + y)
    #                 y += 1

    save(file_name, diagram)


def rename_icons():
    diagram_json = get("diagram")
    updates_json = get("icons_for_update")
    for name, icon in updates_json.items():
        if name != icon["name"]:
            print(f"updating {name} -> {icon['name']}")
            for d_icon in diagram_json['icons']:
                if d_icon['name'] == name:
                    d_icon['name'] = icon['name']
                    print("done")
                    break
    save("diagram", diagram_json)



if __name__ == "__main__":
    # python ./server/console/diagram/fix_diagram.py <action> <file_name> <up> <right>
    action = sys.argv[1]
    if action == "move":
        filename = sys.argv[2]
        up = int(sys.argv[3])
        right = int(sys.argv[4])
        move(filename, up, right)
    elif action == "stretch":
        filename = sys.argv[2]
        up = int(sys.argv[3])
        right = int(sys.argv[4])
        stretch(filename, up, right)
    elif action == "rename_icons":
        rename_icons()