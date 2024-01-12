__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import json
import os
import sys
import datetime
import time
import fnmatch
import urllib.parse
import  boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
import botocore
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

class QuicksightIntegration:

    def __init__(self, transform, dtypes, region):
        self.transform = transform
        self.dtypes = {}
        self.region = region

        for col, dt in dtypes.items():
            if 'int' in dt:
                dt = 'INTEGER'
            elif dt == 'timestamp':
                dt = 'DATETIME'
            else:
                dt = 'STRING'
            self.dtypes[col] = dt

        self.quicksight_client = boto3.client('quicksight')
        
        self.account_id = boto3.client('sts').get_caller_identity().get('Account')
        logger.info(f"account_id: {self.account_id}")

        self.username = boto3.client('iam').get_user()["User"]["UserName"]
        logger.info(f"username: {self.username}")

        self.quicksight_user_arn = f"arn:aws:quicksight:{self.region}:{self.account_id}:user/default/{self.username}"
        logger.info(f"quicksight_user_arn: {self.quicksight_user_arn}")

        self.quicksight_dataset_id = f"{transform['profile']}_{transform['name']}".replace('_','-') 
        logger.info(f"quicksight_dataset_id: {self.quicksight_dataset_id}")


    def json_converter(self, obj):
        return str(obj)


    def get_quicksight_data_source(self):
        data_source = None
        try:
            data_source = self.quicksight_client.describe_data_source(
                AwsAccountId=self.account_id,
                DataSourceId=self.quicksight_dataset_id,
            )
            logger.info(json.dumps(data_source, indent=2, default=self.json_converter))
        except Exception as e:
            logger.info(e.args)
        return data_source


    def create_quicksight_data_source(self):
        logger.info(f"creating quicksight data source {self.quicksight_dataset_id} ...")
        data_source = None
        try:
            data_source = self.quicksight_client.create_data_source(
                AwsAccountId=self.account_id,
                DataSourceId=self.quicksight_dataset_id,
                Name=self.quicksight_dataset_id,
                Type='ATHENA',
                DataSourceParameters={
                    'AthenaParameters': {
                        'WorkGroup': 'primary'
                    }
                },
                SslProperties={
                    'DisableSsl': False
                },
                Permissions=[
                    {
                        'Principal': self.quicksight_user_arn,
                        "Actions": [
                            "quicksight:UpdateDataSourcePermissions",
                            "quicksight:DescribeDataSource",
                            "quicksight:DescribeDataSourcePermissions",
                            "quicksight:PassDataSource",
                            "quicksight:UpdateDataSource",
                            "quicksight:DeleteDataSource"
                        ]                    
                    },
                ],                
                Tags=[
                    {
                        'Key': 'env',
                        'Value': transform['profile']
                    },
                    {
                        'Key': 'transform',
                        'Value': transform['fqn']
                    }
                ]
            )
            logger.info(json.dumps(data_source, indent=2, default=self.json_converter))

        except Exception as e:
            logger.info(e.args)

        return data_source


    def get_quicksight_dataset(self):
        dataset = None
        try:
            dataset = self.quicksight_client.describe_data_set(
                AwsAccountId=self.account_id,
                DataSetId=self.quicksight_dataset_id,
            )
            logger.info(json.dumps(dataset, indent=2, default=self.json_converter))
        except Exception as e:
            logger.info(e.args)
        return dataset


    def create_quicksight_dataset_if_not_exists(self):
        if self.get_quicksight_dataset() is not None:
            return

        data_source = self.get_quicksight_data_source()
        if data_source is None:
            data_source = self.create_quicksight_data_source()

        try:        
            glue_db = f"{transform['analysis_catalog']}"
            glue_table = f"{transform['name']}"
            logger.info(f"creating quicksight dataset for {glue_db}.{glue_table}")

            input_columns = []
            projected_columns = []
            logger.info(f"self.dtypes: {self.dtypes}")
            for col, dt in self.dtypes.items():
                input_columns.append({
                    "Name": col,
                    "Type": dt
                })
                projected_columns.append(col)
            logger.info(f"input_columns: {input_columns}")
            logger.info(f"projected_columns: {projected_columns}")
            
            import_mode = 'SPICE' if transform.get('refresh_spice') else 'DIRECT_QUERY'
            dataset = self.quicksight_client.create_data_set(
                AwsAccountId=self.account_id,
                DataSetId=self.quicksight_dataset_id,
                Name=self.quicksight_dataset_id,
                PhysicalTableMap={
                    self.quicksight_dataset_id: {
                        'RelationalTable': {
                            'DataSourceArn': data_source['Arn'],
                            'Schema': glue_db,
                            'Name': glue_table,
                            'InputColumns': input_columns
                        }
                    }
                },
                LogicalTableMap={
                    self.quicksight_dataset_id: {
                        'Alias': self.quicksight_dataset_id,
                        'DataTransforms': [
                            {
                                "ProjectOperation": {
                                    "ProjectedColumns": projected_columns
                                }
                            }
                        ],
                        'Source': {
                            'PhysicalTableId': self.quicksight_dataset_id
                        }
                    }
                },
                ImportMode=import_mode,
                Permissions=[
                    {
                        'Principal': self.quicksight_user_arn,
                        "Actions": [
                            "quicksight:UpdateDataSetPermissions",
                            "quicksight:DescribeDataSet",
                            "quicksight:DescribeDataSetPermissions",
                            "quicksight:PassDataSet",
                            "quicksight:DescribeIngestion",
                            "quicksight:ListIngestions",
                            "quicksight:UpdateDataSet",
                            "quicksight:DeleteDataSet",
                            "quicksight:CreateIngestion",
                            "quicksight:CancelIngestion"
                        ]                    
                    },
                ],                
                Tags=[
                    {
                        'Key': 'env',
                        'Value': transform['profile']
                    },
                    {
                        'Key': 'transform',
                        'Value': transform['fqn']
                    }
                ]
            )

            logger.info(json.dumps(dataset, indent=2, default=self.json_converter))

        except Exception as e:
            logger.warn("FAILURE: create_quicksight_dataset_if_not_exists()")
            for arg in e.args:
                logger.info(arg)


    def refresh_spice(self):
        try:
            logger.info("refreshing SPICE")
            response = quicksight_client.create_ingestion(
                DataSetId=self.quicksight_dataset_id,
                IngestionId=f"{transform['name']}_{str(int(round(time.time() * 1000)))}",
                AwsAccountId=self.account_id
            )
            self.logger.info(json.dumps(response, indent=2, default=self.json_converter))    
        except Exception as e:
            logger.info(e)        

if __name__ == "__main__":
    print(sys.argv[1])
    transform = boto3.resource('dynamodb').Table('transformation').query(
            KeyConditionExpression=Key('fqn').eq(sys.argv[1])
        )['Items'][0]
    print(json.dumps(transform, indent=2))

    dtypes = {
        'id': 'string',
        'first_name': 'string',
        'last_name': 'string',
        'ssn': 'string',
        'dob': 'string',
        'address': 'string',
        'city': 'string',
        'state': 'string',
        'timestamp': 'timestamp'
    }
    qsi = QuicksightIntegration(transform, dtypes, "us-east-1")
    dataset = qsi.create_quicksight_dataset_if_not_exists()

