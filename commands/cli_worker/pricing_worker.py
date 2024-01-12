#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging

from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.pricing import Pricing 

class PricingWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def pricing(self):
        if self.args.command == 'init':
            Pricing(self.args).init()
        else:
            Pricing(self.args).get_pricing()
