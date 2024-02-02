__author__ = "Jeffrey Planes"
__license__ = "MIT"


import sys
import os
import json
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Secrets:
    def __init__(self, job_name, secret_key, region="us-east-1", credential_name=None,aws_service='secretsmanager'):
        self.job_name = job_name
        self.secret_key = secret_key
        self.region = region
        self.credential_name = credential_name
        self.aws_service = aws_service

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

    def get_secret(self):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

        try:

            if self.credential_name is not None:
                session = boto3.session.Session(profile_name=self.credential_name)
            else:
                session = boto3.session.Session()

            aws_secrets = session.client(self.aws_service, self.region)
            secret = aws_secrets.get_secret_value(SecretId=self.secret_key).get( "SecretString")
            secret = json.loads(secret)

            return secret

        except Exception as e:
            msg = e.args
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_message)
            raise Exception(exception_message)
