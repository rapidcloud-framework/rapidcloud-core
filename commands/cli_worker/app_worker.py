#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

from commands.cli_worker.aws_worker import AwsWorker

class AppWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def add_mobile_app(self):
        self.logger.warn("Mobile apps are not supported in this version of RapidCloud")
        # TODO
        pass


    def add_web_app(self):
        self.logger.warn("Web applications are not supported in this version of RapidCloud")
        # TODO
        pass


    def app(self):
        if self.args.command == 'add-mobile-app':
            self.add_mobile_app()

        elif self.args.command == 'add-web-app':
            self.add_web_app()
