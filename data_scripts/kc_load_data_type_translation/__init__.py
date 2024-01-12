__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import os
import json
from datetime import datetime
import csv
import boto3
import argparse
from   progress.bar import Bar
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataTypeTranslation():

    def get_boto3_session(self,aws_region="us-east-1", profile=None):

            ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

            if profile is not None:
                session = boto3.session.Session(profile_name=profile, region_name=aws_region)
            else:
                session = boto3.session.Session()
                
            return session

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)
        
    def delete_metadata_table(self,session,aws_service,dynamo_table):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

            dynamodb_list_object = session.client(aws_service)
            dynamodb_delete_object = session.resource(aws_service)
            ## Get Table List
            existing_tables = dynamodb_list_object.list_tables()['TableNames']
            ## Check to see if table exists, if so then we can delete the DynamoDB table
            if dynamo_table  in existing_tables:            
                table = dynamodb_delete_object.Table(dynamo_table)
                table.delete()
                ## Wait until the table is deleted.
                table.meta.client.get_waiter('table_not_exists').wait(TableName=dynamo_table)
                logger.info(f'Table deleted: {dynamo_table}')

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)

    def create_metadata_table(self,session,aws_service,dynamo_table):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

            # Create the DynamoDB table.
            dynamodb_list_object = session.client(aws_service)
            dynamodb_create_object = session.resource(aws_service)
            ## Get Table List
            existing_tables = dynamodb_list_object.list_tables()['TableNames']
            ## Check to see if table exists, if so then we can delete the DynamoDB table
            if dynamo_table  not in existing_tables:            
                table = dynamodb_create_object.create_table(
                TableName=dynamo_table,
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
                table.meta.client.get_waiter('table_exists').wait(TableName=dynamo_table)
                logger.info(f'Table created: {dynamo_table}')

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)


    def  insert_stub_records(self,session,aws_service,dynamo_table,stub_record_pk,stub_record_sk,dateString):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

                dynamodb = session.resource(aws_service).Table(dynamo_table)
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

                logger.info(f'Inserted Stub Records into {dynamo_table}')

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)

    def  delete_stub_records(self,session,aws_service,dynamo_table,stub_record_pk,stub_record_sk):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

                dynamodb = session.resource(aws_service).Table(dynamo_table)
                response = dynamodb.delete_item(
                Key={"fqn": stub_record_pk,
                "cast_from": stub_record_sk}
            )

                logger.info(f'Delete Stub Records from {dynamo_table}')

        except Exception as e:                                
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)

    def convert_csv_to_json_list(self,file,dateString):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

            items = []
            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data = {}
                    data['fqn'] = row['fqn']
                    data['cast_from'] = row['cast_from']
                    data['engine_from'] = row['engine_from']            
                    data['engine_to'] = row['engine_to']
                    data['cast_to'] = row['cast_to']
                    data['create_timestamp']  = dateString
                    items.append(data)

                progress = Bar('Converting CSV To Json', max=len(items))
                for item in items:
                    logger.debug(item)
                    progress.next()
                progress.finish()

            return items

        except Exception as e:                                
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)

    def batch_write(self,session,aws_service,items,dynamo_table):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

            dynamodb = session.resource(aws_service)
            db = dynamodb.Table(dynamo_table)
            with db.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)

                progress = Bar(f'Writting csv file to {dynamo_table}', max=len(items))
                for item in items:
                    logger.debug(item)
                    progress.next()
                progress.finish()

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)

    def main(self,args):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name
        script_id = os.path.basename(str(sys.argv[0]))
        script_id = script_id.split(".")[0].split("/")[-1]
        aws_service = "dynamodb"
        dynamo_table = "data_type_translation"
        stub_record_pk = "test_test"    
        stub_record_sk  = "varchar*"
        metadata_file_path = 'modules/kc_load_data_type_translation'
        file_name = "data_type_translation"
        csv_file_extension = '.csv'    
        now = datetime.now()  # current date and time
        dateString = now.strftime("%Y-%m-%d %H:%M:%S")

        try:

            if args.aws_profile:
                aws_profile = args.aws_profile.lower()
            if args.aws_region:
                aws_region  = args.aws_region

            session = self.get_boto3_session(aws_region,aws_profile)
            ## Delete DynamoDB metadata table if exists
            self.delete_metadata_table(session,aws_service,dynamo_table)
            ## Create DynamoDB metadata table if not exists
            self.create_metadata_table(session,aws_service,dynamo_table)
            ## Insert stub record into metadata table
            self.insert_stub_records(session,aws_service,dynamo_table,stub_record_pk,stub_record_sk,dateString)
            csv_file = f"{metadata_file_path}/{file_name}{csv_file_extension}"
            json_data   = self.convert_csv_to_json_list(csv_file,dateString)
            self.batch_write(session,aws_service,json_data,dynamo_table)
            ## Delete the Stub recordds
            self.delete_stub_records(session,aws_service,dynamo_table,stub_record_pk,stub_record_sk)

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_msg)
            raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws_profile", required=True, help="Please pass in the appropriate --aws_profile")
    parser.add_argument("--aws_region", required=True, help="Please pass in the appropriate --aws_region")
    args = parser.parse_args()
    DataTypeTranslation().main(args)
