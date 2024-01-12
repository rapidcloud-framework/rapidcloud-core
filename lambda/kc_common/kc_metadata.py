__author__ = "Jeffrey Planes"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "jplanes@kinect-consulting.com"

import sys
import json
import boto3
import logging
import os
import datetime
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Metadata:

    def __init__( self, aws_region="us-east-1",aws_service="dynamodb",credential_name=None,):
        self.aws_region = aws_region
        self.aws_service = aws_service
        self.credential_name = credential_name

        if self.credential_name is not None:
            session = boto3.session.Session(
                profile_name=self.credential_name, region_name=self.aws_region
            )
        else:
            session = boto3.session.Session(region_name=self.aws_region)

        self.dynamodb_resource = session.resource(self.aws_service)

    def scan(self,table,key_attr,key_value):
        return self.dynamodb_resource.Table(table).scan(FilterExpression=Attr(key_attr).eq(key_value))['Items']

    def query(self,table, key_attr, key_value):
        return self.dynamodb_resource.Table(table).query(KeyConditionExpression=Key(key_attr).eq(key_value))['Items']

    def get_metadata(self,table_name,profile,dataset_name):

            table =  self.dynamodb_resource.Table(table_name)

            ## if the data_set != 'all then add an extra filter clause for name (dataset), otherwise query metadata for just the profile and the size filters.
            if dataset_name.lower() != 'all':
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("name").eq(dataset_name))
            else:
                response = table.scan(FilterExpression=Attr("profile").eq(profile))
            return response["Items"]

    ## Move this function into Igor's metadata module, so that we have code re-use
    def get_dataset_metadata(self,table_name,source_database,source_schema,dataset_name,profile):
    
            table =  self.dynamodb_resource.Table(table_name)
            response = table.scan(FilterExpression=Attr("source_database").eq(source_database) & Attr("source_schema").eq(source_schema) & Attr("name").eq(dataset_name) & Attr("profile").eq(profile))
            return response["Items"]

    def is_file_loaded(self,table_name,key_attr,key_value):
        item = self.query(table_name, key_attr, key_value)
        return True if item else False

    def update_publishing_ddl(self,fqn,redshift_schema_stage,redshift_ddl,redshift_table_property):
        
        ## Replace the schema name with a '{}'
        redshift_ddl = redshift_ddl.replace(redshift_schema_stage,'{}')
        dynamo_db_table = self.dynamodb_resource.Table('publishing')
        dynamo_db_table.update_item(
            Key={"fqn": fqn},
            UpdateExpression="SET  redshift_ddl = :redshift_ddl,redshift_table_property = :redshift_table_property",
            ExpressionAttributeValues={
                ":redshift_ddl":redshift_ddl,
                ":redshift_table_property": redshift_table_property,
            },
        )

