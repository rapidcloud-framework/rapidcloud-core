__author__ = "iroyzis@kinect-consulting.com"

import datetime
import json
import time
import botocore
from boto3.dynamodb.conditions import Key, Attr
import re

from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.boto3_session = super().get_boto3_session()
        self.dynamodb_resource = self.boto3_session.resource("dynamodb")


    def run(self, metadata=None):
        table = self.dynamodb_resource.Table("transform_log")
        report_name = self.args.name
        timestamp = str(datetime.datetime.now())
        for c in ['-',' ',':','.']:
            timestamp = timestamp.replace(c, "")
        report_instance_fqn = f"{self.env}_report_{report_name}_{timestamp}"

        # save report log
        item = {
            "fqn": report_instance_fqn,
            "profile": self.env,
            "job_type": "report",
            "report_name": report_name,
            "status": "STARTED",
            "update_timestamp": str(datetime.datetime.now())            
        }
        response = table.put_item(Item=item)
        self.logger.info(json.dumps(item, indent=2))
       
        try:
            config = botocore.config.Config(
                read_timeout=900,
                connect_timeout=900,
                retries={"max_attempts": 0}
            )
            self.lambda_client = self.boto3_session.client("lambda", config=config)
            response = self.lambda_client.invoke(
                # FunctionName=f"{self.env}_report-runner", # report_generation
                FunctionName=f"{self.env}_report_generation",
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    "report_name": self.args.name
                })
            )
            item['status'] = "COMPLETED"
            item['results'] = json.loads(response['Payload'].read())
            # s3://igor-textract-dev-analysis/reports/report-2023-06-29--16:03:45.csv
            # https://igor-textract-dev-analysis.s3.amazonaws.com/reports/report-2023-06-29--16%3A03%3A45.csv
            s3_loc = item['results']['s3']
            item['results']['_report_csv'] = s3_loc.replace('s3:','https:').replace('/reports/', '.s3.amazonaws.com/reports/')
        except Exception as e:
            item['status'] = "FAILED"
            item['message'] = str(e)

        # print(json.dumps(item, indent=2, default=str))
        item['update_timestamp'] = str(datetime.datetime.now())
        response = table.put_item(Item=item)
        self.logger.info(json.dumps(item, indent=2))

    def define_report(self, metadata=None):
        pass

    def set_document_report_mapping(self, metadata=None):
        pass