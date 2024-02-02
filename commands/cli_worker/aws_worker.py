__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging

from commands import boto3_utils, general_utils
from commands.cli_worker import CliWorker


class AwsWorker(CliWorker):
    logger = logging.getLogger(__name__)
    def __init__(self, args):
        super().__init__(args)
        self.args = args
        env_info = None
        if hasattr(args, "env_info") and args.env_info is not None:
            env_info = args.env_info
        else:
            if args.env is not None:
                curr_env = args.env
            else:
                aws_profile_config = general_utils.load_json_file(f"./config/aws_profile.json")
                curr_env = aws_profile_config.get("env")

            if curr_env:
                env_config_file = f"./config/environments/{curr_env}_config.json"
                env_info = general_utils.load_json_file(env_config_file)

        if env_info:
            self.boto_session = boto3_utils.get_boto_session(region=env_info.get("region"), aws_profile=env_info.get("aws_profile"), x_acct_role_arn=env_info.get("x_acct_role_arn"))
            self.dynamodb_resource = self.boto_session.resource('dynamodb')


    def get_item(self, table, pk_name, pk_value):
        self.logger.info("AwsWorker Got Called")
        response = self.dynamodb_resource.Table(table).get_item(Key={pk_name: pk_value})
        if 'Item' in response:
            return response['Item']
        else:
            return None
