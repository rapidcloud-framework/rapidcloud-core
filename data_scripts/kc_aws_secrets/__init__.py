__license__ = "MIT"

import sys
import os
import json
import boto3
from    data_scripts.kc_logging import Logger


class Secrets:
    def __init__(self, job_name, secret_key, region_name="us-east-1", credential_name=None,aws_service='secretsmanager'):
        self.job_name = job_name
        self.secret_key = secret_key
        self.region_name = region_name
        self.credential_name = credential_name
        self.aws_service = aws_service

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        self.logger = Logger(self.job_name)
        self.logger.log("INFO", f"Inside method: {function_id}")

    def get_secret(self):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {function_id}")

        try:

            if self.credential_name is not None:
                session = boto3.session.Session(profile_name=self.credential_name, region_name=self.region_name)
            else:
                session = boto3.session.Session(region_name=self.region_name)

            aws_secrets = session.client(self.aws_service)
            secret = aws_secrets.get_secret_value(SecretId=self.secret_key).get( "SecretString")
            secret = json.loads(secret)

            return secret

        except Exception as e:
            msg = e.args
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exception_message)
            raise Exception(exception_message)
