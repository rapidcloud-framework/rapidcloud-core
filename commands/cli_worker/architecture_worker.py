#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging
import json

from commands.cli_worker.aws_worker import AwsWorker

class ArchitectureWorker(AwsWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def architecture(self):
        if self.args.command == 'save-wizard':
            self.save_wizard(self.args.wizard, self.args.cloud, self.args.diagram_type)


    def save_wizard(self, wizard, cloud, diagram_type):
        profile_table = self.dynamodb_resource.Table('profile')
        col = f"{cloud}_{diagram_type}_wizard"
        self.logger.info(f"saving {col}")
        if type(wizard) == str:
            # convert to dict
            wizard = json.loads(wizard.replace('\\"', '"'))

        response = profile_table.update_item(
            Key={'name': self.args.env},
            UpdateExpression=f"set {col} = :w",
            ExpressionAttributeValues={
                ':w': wizard
            },
            ReturnValues="UPDATED_NEW"
        )
        # self.logger.debug(response)
