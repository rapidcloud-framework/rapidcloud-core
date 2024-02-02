#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

class ServerHelper(object):
    
    logger = logging.getLogger(__name__)

    def __init__(self, args, app_mode):
        self.args = args
        self.app_mode = app_mode

