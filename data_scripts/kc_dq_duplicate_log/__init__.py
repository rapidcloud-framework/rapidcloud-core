__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import os
import sys
import boto3
from datetime import datetime
from  data_scripts.kc_logging import Logger


class DQDuplicateCheck:
    def __init__(
        self,
        job_name,
        aws_region="us-east-1",
        log_table="dq_duplicate_count_log",
        aws_service="dynamodb",
        date_format="%Y-%m-%d",
        ##date_format="%Y-%m-%d %H:%M:%S",
        credential_name=None,
    ):
        self.job_name = job_name
        self.aws_region = aws_region
        self.log_table = log_table
        self.aws_service = aws_service
        _create_date = datetime.now()
        self.date_format = date_format
        self.create_date = _create_date.strftime(self.date_format)
        self.credential_name = credential_name

        if self.credential_name is not None:
            session = boto3.session.Session(
                profile_name=self.credential_name, region_name=self.aws_region
            )
        else:
            session = boto3.session.Session(region_name=self.aws_region)

        self.dynamo_db_table = session.resource(self.aws_service).Table(self.log_table)

    def dq_duplicate_count_log(
        self, entity, duplicate_count,
    ):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        glueEtl = self.job_name

        logger = Logger(self.job_name)
        logger.log("INFO", f"Inside method: {functionID}")

        try:

            self.dq_duplicate_log_insert(
                entity, duplicate_count,
            )
            self.dq_duplicate_log_update(
                entity, duplicate_count,
            )

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def dq_duplicate_log_insert(
        self, entity, duplicate_count,
    ):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        glueEtl = self.job_name
        ## create_date = self.create_date
        ## Default value means, there is no validation exception
        is_failed_validation = 0

        logger = Logger(self.job_name)
        logger.log("INFO", f"Inside method: {functionID}")

        try:

            ## Evaluate if duplciate_count > 0, if so, then set the failed validation indicator to 1.
            if duplicate_count > 0:
                is_failed_validation = 1

            response = self.dynamo_db_table.put_item(
                Item={
                    "entity": entity,
                    "create_date": self.create_date,
                    "duplicate_count": duplicate_count,
                    "is_failed_validation": is_failed_validation,
                    "modified_date": self.create_date,
                }
            )

            logger.log("INFO", f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def dq_duplicate_log_update(
        self, entity, duplicate_count,
    ):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        _modified_date = datetime.now()
        modified_date = _modified_date.strftime(self.date_format)
        ## Default value means, there is no validation exception
        is_failed_validation = 0

        logger = Logger(self.job_name)
        logger.log("INFO", f"Inside method: {functionID}")

        try:

            ## Evaluate if duplciate_count > 0, if so, then set the failed validation indicator to 1.
            if duplicate_count > 0:
                is_failed_validation = 1

            response = self.dynamo_db_table.update_item(
                Key={"entity": entity, "create_date": self.create_date},
                UpdateExpression="SET duplicate_count = :duplicate_count, is_failed_validation = :is_failed_validation, modified_date = :modified_date",
                ExpressionAttributeValues={
                    ":duplicate_count": duplicate_count,
                    ":is_failed_validation": is_failed_validation,
                    ":modified_date": modified_date,
                },
            )

            logger.log("INFO", f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
