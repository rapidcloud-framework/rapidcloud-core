#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.analytics import Analytics 

class AnalyticsWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def analytics(self):
        if self.args.command == 'add-service':
            Analytics(self.args).save_analytics()

