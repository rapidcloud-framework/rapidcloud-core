#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging
from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.aws_infra import AwsInfra 

class CustomResourceWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def run(self):
        if self.args.command == 'add-glue-job':
            AwsInfra(self.args).add_glue_job() 
        elif self.args.command == 'add-kinesis-stream':
            AwsInfra(self.args).add_kinesis_stream() 
        elif self.args.command == 'add-msk-cluster':
            AwsInfra(self.args).add_msk_cluster() 
