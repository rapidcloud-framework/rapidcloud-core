#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.deployment import Deployment 

class DeployWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def deploy(self):

        if self.args.command == 'test':
            Deployment(self.args).test()

        elif self.args.command == 'run-crawlers':
            Deployment(self.args).run_crawlers()

        # elif self.args.command == 'post-transform':
        #     Deployment(self.args).post_transform()
                