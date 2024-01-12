__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr
from commands.kc_metadata_manager.aws_metadata import Metadata

class Event(Metadata):

    TABLE_NAME = 'event'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def save_event(self):
        fqn = f"{super().get_env()}_{self.args.dataset_name}" 
        table_obj = super().get_dynamodb_resource().Table("dataset")
        dataset = table_obj.get_item(Key={'fqn': fqn})['Item']
        response = table_obj.update_item(Key={'fqn': fqn},
            UpdateExpression="set cdc_via = :p",
            ExpressionAttributeValues={':p': 'kinesis'}
        )
        dataset = table_obj.get_item(Key={'fqn': fqn})['Item']
                
        item={
            'fqn': fqn, 
            'profile': super().get_env(), 
            'name': self.args.dataset_name,
            'partitions': self.args.partitions if self.args.partitions else "datalake_year,datalake_month,datalake_day",
            'source_database': dataset['source_database'] if dataset else '',
            'source_schema': dataset['source_schema'] if dataset else '',
            'source_table': dataset['source_table'] if dataset else '',
            'enabled': True, 
            'timestamp': str(datetime.datetime.now())
        }
        self.logger.info(json.dumps(item, indent=2))
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata", self.args.dataset_name)
        
        # create kinesis firehose
        super().add_aws_resource('kinesis_firehose_s3_delivery_stream', 'main', super().get_kinesis_firehose_params())

        # create Lambda function for applying events to rawdb
        env_vars = {
            "PROFILE": super().get_env()
        }
        layers = {
            "10": f"{super().get_env()}_lambda_layer_awswrangler"
        }
        params = super().get_lambda_function_params(env_vars, layers)
        super().add_aws_resource('lambda_function', 'event_cdc', params)

        # Glue crawler for semi-structured data in raw
        events = self.get_all_events()
        params = super().get_glue_crawler_params("raw", "events", events)
        super().add_aws_resource('glue_crawler', 'raw-events', params)


    def get_all_events(self):
        return super().get_dynamodb_resource().Table(self.TABLE_NAME).scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )['Items']
