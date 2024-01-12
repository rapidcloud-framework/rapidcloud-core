__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import os
import sys
import boto3
from datetime import datetime
from  data_scripts.kc_logging import Logger
from  data_scripts.kc_process_log import ProcessLog


class ProcessExceptionLog:
    def __init__(
        self,
        job_name,
        aws_region="us-east-1",
        log_table="process_exception_log",
        aws_service="dynamodb",
        date_format="%Y-%m-%d %H:%M:%S",
        credential_name=None,
    ):
        self.job_name = job_name
        self.aws_region = aws_region
        self.log_table = log_table
        self.aws_service = aws_service
        _exception_log_timestamp = datetime.now()
        self.date_format = date_format
        self.exception_log_timestamp = _exception_log_timestamp.strftime(
            self.date_format
        )
        self.credential_name = credential_name

        if self.credential_name is not None:
            session = boto3.session.Session(
                profile_name=self.credential_name, region_name=self.aws_region
            )
        else:
            session = boto3.session.Session(region_name=self.aws_region)

        self.dynamo_db_table = session.resource(self.aws_service).Table(self.log_table)

    def process_exception(
        self, exception_msg, process_status="failed",
    ):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        glueEtl = self.job_name

        logger = Logger(self.job_name)
        logger.log("INFO", f"Inside method: {functionID}")

        try:

            ## End Process Logging for failed process
            process_log_conn = ProcessLog(
                self.job_name,
                self.aws_region,
                "process_log",
                self.aws_service,
                self.date_format,
                self.credential_name,
            )
            process_log_conn.process_log_end(process_status)

            response = self.dynamo_db_table.put_item(
                Item={
                    "job_name": self.job_name,
                    "exception_log_timestamp": self.exception_log_timestamp,
                    "exception_msg": exception_msg,
                }
            )

            logger.log("INFO", f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
