#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging

from commands.cli_worker import CliWorker
from commands.cli_worker.provider import Provider

class ActivationWorker(CliWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def activate(self):
        activator = Provider(self.args).get_activator()
        activator.activate(super())
        activator.print_post_activation_instructions()

    def update(self):
        Provider(self.args).get_activator().update()
    
    def uninstall(self):
        Provider(self.args).get_activator().uninstall()