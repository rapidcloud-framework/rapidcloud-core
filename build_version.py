#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import sys

v = sys.argv[1]

if not v or v == "rc":
    with open('./config/version.json', 'r') as f:
        version = json.load(f)
        print(version['version'])

elif v == "kc_common":
    with open('./config/kc_config.json', 'r') as f:
        kc_config = json.load(f)
        print(kc_config['utils']['version'])
