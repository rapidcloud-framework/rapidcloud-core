#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging

from commands.cli_worker.aws_worker import AwsWorker

class ConsoleWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


