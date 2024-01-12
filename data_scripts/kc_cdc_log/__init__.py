__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import os
import sys
import boto3
from   datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CdcLog:
    def __init__(
        self,
        job_name,
        aws_region="us-east-1",
        log_table="cdc_log",
        aws_service="dynamodb",
        date_format="%Y-%m-%d %H:%M:%S",
        credential_name=None,
    ):
        self.job_name = job_name
        self.aws_region = aws_region
        self.log_table = log_table
        self.aws_service = aws_service
        _cdc_timestamp = datetime.now()
        self.date_format = date_format
        self.cdc_timestamp = _cdc_timestamp.strftime(self.date_format)
        self.credential_name = credential_name

        if self.credential_name is not None:
            session = boto3.session.Session(
                profile_name=self.credential_name, region_name=self.aws_region
            )
        else:
            session = boto3.session.Session(region_name=self.aws_region)

        self.dynamo_db_table = session.resource(self.aws_service).Table(self.log_table)

    def cdc_log(self, fqn,cdc_s3_bucket, cdc_s3_key, cdc_s3_file,source_database,source_schema,dataset_name,cdc_action='n/a'):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        glueEtl = self.job_name

        logger.info(f"Inside method: {functionID}")

        try:

            self.cdc_log_insert(fqn,cdc_s3_bucket, cdc_s3_key, cdc_s3_file,source_database,source_schema,dataset_name,cdc_action)
            self.cdc_log_update(fqn,cdc_s3_bucket, cdc_s3_key, cdc_s3_file,source_database,source_schema,dataset_name,cdc_action)

        except Exception as e:
            msg = e.args
            execption_message = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.error(execption_message)
            raise Exception(execption_message)

    def cdc_log_insert(self,fqn,cdc_s3_bucket, cdc_s3_key, cdc_s3_file,source_database,source_schema,dataset_name,cdc_action='n/a'):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        
        logger.info(f"Inside method: {functionID}")

        try:
            env = cdc_s3_bucket[0:cdc_s3_bucket.rindex("-")].replace("-","_")
            response = self.dynamo_db_table.put_item(
                Item={
                    "fqn": fqn,
                    "profile": env,
                    "cdc_s3_bucket": cdc_s3_bucket,
                    "cdc_s3_key": cdc_s3_key,
                    "cdc_s3_file": cdc_s3_file,
                    "source_database": source_database,
                    "source_schema": source_schema,
                    "dataset_name": dataset_name,
                    "cdc_action": cdc_action,
                    "job_name": self.job_name,
                    "cdc_timestamp": self.cdc_timestamp,
                }
            )

            logger.info(f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            execption_message = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.error(execption_message)
            raise Exception(execption_message)

    def cdc_log_update(self,fqn,cdc_s3_bucket, cdc_s3_key, cdc_s3_file,source_database,source_schema,dataset_name,cdc_action='n/a'):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {functionID}")

        try:

            response = self.dynamo_db_table.update_item(
                Key={"fqn": fqn},
                UpdateExpression="SET cdc_s3_bucket = :cdc_s3_bucket, cdc_s3_key = :cdc_s3_key, cdc_s3_file = :cdc_s3_file, source_database = :source_database, source_schema = :source_schema, dataset_name = :dataset_name, cdc_action = :cdc_action, job_name = :job_name, cdc_timestamp = :cdc_timestamp",
                ExpressionAttributeValues={
                    ":cdc_s3_bucket": cdc_s3_bucket,
                    ":cdc_s3_key": cdc_s3_key,
                    ":cdc_s3_file": cdc_s3_file,
                    ":source_database": source_database,
                    ":source_schema": source_schema,
                    ":dataset_name": dataset_name,
                    ":cdc_action": cdc_action,
                    ":job_name": self.job_name,
                    ":cdc_timestamp": self.cdc_timestamp,
                },
            )

            logger.info(f"Boto3 DynamoDB Response: {response}")

        except Exception as e:
            msg = e.args
            execption_message = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            logger.error(execption_message)
            raise Exception(execption_message)
