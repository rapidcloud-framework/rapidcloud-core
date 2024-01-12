__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import boto3
import logging
from datetime import datetime

from commands.cli_worker import CliWorker
from commands.colors import colors

class GcpWorker(CliWorker):
    
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        if 'default_region' in self.config:
            region = self.config['default_region']
            # try:
            #     if 'aws_profile' in self.config:
            #         aws_profile = self.config['aws_profile']
            #         self.boto_session = boto3.Session(profile_name=aws_profile, region_name=region)
            #     else:
            #         self.boto_session = boto3.Session(region_name=region)
            #     self.dynamodb_resource = self.boto_session.resource('dynamodb')
            # except Exception as e:
            #     self.logger.error(f"{colors.FAIL}{e}{colors.ENDC}")


    def get_item(self, table, pk_name, pk_value):
        # response = self.dynamodb_resource.Table(table).get_item(Key={pk_name: pk_value})
        # if 'Item' in response:
        #     return response['Item']
        # else:
        #     return None
        return None