__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import os
import sys
import boto3
from datetime import datetime
from   data_scripts.kc_logging import Logger


class ProcessLog:
    def __init__(
        self,
        job_name,
        aws_region="us-east-1",
        log_table="process_log",
        aws_service="dynamodb",
        date_format="%Y-%m-%d %H:%M:%S",
        credential_name=None,
    ):
        self.job_name = job_name
        self.aws_region = aws_region
        self.log_table = log_table
        self.aws_service = aws_service
        _log_start_timestamp = datetime.now()
        self.date_format = date_format
        self.log_start_timestamp = _log_start_timestamp.strftime(self.date_format)
        self.credential_name = credential_name

        if self.credential_name is not None:
            session = boto3.session.Session(
                profile_name=self.credential_name, region_name=self.aws_region
            )
        else:
            session = boto3.session.Session(region_name=self.aws_region)

        self.dynamo_db_table = session.resource(self.aws_service).Table(self.log_table)

    def process_log_start(
        self, log_status="started",
    ):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        glueEtl = self.job_name

        logger = Logger(self.job_name)
        logger.log("INFO", f"Inside method: {functionID}")

        try:

            response = self.dynamo_db_table.put_item(
                Item={
                    "job_name": self.job_name,
                    "log_start_timestamp": self.log_start_timestamp,
                    "log_end_timestamp": "9999-12-31 00:00:00.943914",
                    "log_status": log_status,
                }
            )

            logger.log("INFO", f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def process_log_end(
        self, log_status="completed",
    ):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        _log_end_timestamp = datetime.now()
        log_end_timestamp = _log_end_timestamp.strftime(self.date_format)

        logger = Logger(self.job_name)
        logger.log("INFO", f"Inside method: {functionID}")

        try:

            response = self.dynamo_db_table.update_item(
                Key={"job_name": self.job_name,},
                UpdateExpression="SET log_status = :log_status, log_end_timestamp = :log_end_timestamp",
                ExpressionAttributeValues={
                    ":log_status": log_status,
                    ":log_end_timestamp": log_end_timestamp,
                },
            )

            logger.log("INFO", f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
