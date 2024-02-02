__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata

class SourceTable(Metadata):

    TABLE_NAME = 'source_table'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)


    def json_converter(self, obj):
        return str(obj)


    def get_source_table(self, fqn):
        self.logger.info(f"fqn: {fqn}")
        source_table = super().get_item(self.TABLE_NAME, 'fqn', fqn)
        self.logger.info(json.dumps(source_table))
        return source_table


    def get_source_tables_for_database(self, db_name):
        self.logger.info(f"getting table info for [{super().get_env()}/{db_name}]")
        return super().get_dynamodb_resource().Table(self.TABLE_NAME).scan(        
            FilterExpression=Attr('database').eq(db_name) & Attr('profile').eq(super().get_env())
        )['Items']

