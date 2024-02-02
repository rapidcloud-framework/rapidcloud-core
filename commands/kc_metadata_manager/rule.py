__author__ = "Igor Royzis"
__license__ = "MIT"


import json
from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata

class Rule(Metadata):

    TABLE_NAME = 'rule'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def save_rule(self):
        fqn = f"{super().get_env()}_{self.args.dataset}_{self.args.attr}"
        item={
            'fqn': fqn, 
            'profile': super().get_env(), 
            'phase': "ingestion-to-raw", 
            'dataset': self.args.dataset, 
            'attr': self.args.attr, 
            'attr_type': self.args.attr_type if self.args.attr_type else '', 
            'action': self.args.action, 
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)


    def get_all_rules_by_dataset(self):
        response = super().get_dynamodb_resource().Table('rule').scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )
        self.logger.debug(json.dumps(response, indent=2))

        rules_by_dataset = {}
        for rule in response['Items']:
            rules_by_dataset[rule['dataset']] = rule            

        return rules_by_dataset
