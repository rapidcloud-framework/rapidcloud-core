#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.transformation import Transformation
from commands.modules import exec_module 

class TransformWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def transform(self):
        # make sure datalake was created already, if not, create it
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        if self.args.command == 'add-dataset':
            Transformation(self.args).save_transformation()

