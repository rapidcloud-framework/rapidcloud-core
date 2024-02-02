__license__ = "MIT"

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

        self.dynamodb_client = session.resource(self.aws_service)
        self.dynamodb_resource = session.resource(self.aws_service)
        self.glue_client = session.client('glue')


    def scan(self,table,key_attr,key_value):
        return self.dynamodb_resource.Table(table).scan(FilterExpression=Attr(key_attr).eq(key_value))['Items']

    def query_property(self,table_name, profile,name):
        table =  self.dynamodb_resource.Table(table_name)
        response =  table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("name").eq(name))
        return response["Items"]
    
    def query(self,table, key_attr, key_value):
        return self.dynamodb_resource.Table(table).query(KeyConditionExpression=Key(key_attr).eq(key_value))['Items']

    def get_metadata(self,table_name,profile,dataset_name):
        table =  self.dynamodb_resource.Table(table_name)
        if dataset_name.lower() != 'all':
            response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("name").eq(dataset_name))
        else:
            response = table.scan(FilterExpression=Attr("profile").eq(profile))
        return response["Items"]

    def get_publishing(self,profile,db_engine,dataset_name):

            table =  self.dynamodb_resource.Table("publishing")

            ## if the data_set != 'all then add an extra filter clause for name (dataset), otherwise query metadata for just the profile and the size filters.
            if dataset_name.lower() != 'all':
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("db_engine").eq(db_engine) & Attr("name").eq(dataset_name))
            else:
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("db_engine").eq(db_engine))
            return response["Items"]

    def get_publishing_metadata(self,profile,dataset_name,db_engine=None):

            table =  self.dynamodb_resource.Table("publishing")

            ## if the data_set != 'all then add an extra filter clause for name (dataset), otherwise query metadata for just the profile and the size filters.
            if dataset_name.lower() != 'all' and db_engine is not None:
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("db_engine").eq(db_engine) & Attr("name").eq(dataset_name))
            elif  dataset_name.lower() == 'all' and db_engine is None:
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("db_engine").ne("redshift") & Attr("db_engine").ne("snowflake"))
            elif  dataset_name.lower() == 'all' and db_engine is not None:
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("db_engine").eq(db_engine))
            elif dataset_name.lower() != 'all' and db_engine is None:
                response = table.scan(FilterExpression=Attr("profile").eq(profile) & Attr("db_engine").ne("redshift") & Attr("db_engine").ne("snowflake") & Attr("name").eq(dataset_name))
            return response["Items"]
            
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

    def delete_metadata_table(self,table_name):

        dynamodb_delete_object = self.dynamodb_resource
        dynamodb_list_object = self.dynamodb_client

        ## Get Table List
        existing_tables = dynamodb_list_object.list_tables()['TableNames']
        ## Check to see if table exists, if so then we can delete the DynamoDB table
        if table_name  in existing_tables:            
            table = dynamodb_delete_object.Table(table_name)
            table.delete()
            ## Wait until the table is deleted.
            table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
            logger.info(f'Table deleted: {table_name}')

    def create_metadata_table(self,table_name):

        dynamodb_create_object = self.dynamodb_resource
        dynamodb_list_object = self.dynamodb_client

        ## Get Table List
        existing_tables = dynamodb_list_object.list_tables()['TableNames']
        ## Check to see if table exists, if so then we can delete the DynamoDB table
        if table_name  not in existing_tables:            
            table = dynamodb_create_object.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'fqn',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'cast_from',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'fqn',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'cast_from',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
            )

            ## Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            logger.info(f'Table created: {table_name}')

    def  insert_data_type_translation_stub_records(self,table_name,stub_record_pk,stub_record_sk,dateString):

        dynamodb = self.dynamodb_resource.Table(table_name)
        response = dynamodb.put_item(
        Item={
            "fqn": stub_record_pk,
            "cast_from": stub_record_sk,
            "engine_from":  "test",
            "engine_to": "test",
            "cast_to": "string",
            "create_timestamp": dateString
        }
        )
        logger.info(response)

    def  delete_data_type_translation_stub_records(self,table_name,stub_record_pk,stub_record_sk):

        dynamodb = self.dynamodb_resource.Table(table_name)
        response = dynamodb.delete_item(
            Key={"fqn": stub_record_pk,
            "cast_from": stub_record_sk}
        )

        logger.info(response)
        logger.info(f'Delete Stub Records from {table_name}')
    

    def get_glue_table_info(self, db_name, table_name):
        return self.glue_client.get_table(
            DatabaseName=db_name,
            Name=table_name
        )