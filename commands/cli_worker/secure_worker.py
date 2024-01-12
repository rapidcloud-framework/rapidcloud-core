#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging

from commands.colors import colors
from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.rule import Rule 

class SecureWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def secure(self):
        if self.args.command == 'add-rule':
            print("\nAdding PII rule...\n")
            Rule(self.args).save_rule()
            print(f"{colors.OKGREEN}You've successfully added PII rule!{colors.ENDC}\n")

