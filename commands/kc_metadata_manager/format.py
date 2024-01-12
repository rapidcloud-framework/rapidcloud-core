__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata

class Format(Metadata):

    TABLE_NAME = 'format'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def save_format(self):
        fqn = f"{super().get_env()}_{self.args.dataset}_{self.args.attr}"
        item={
            'fqn': fqn, 
            'profile': super().get_env(), 
            'phase': self.args.pipeline_phase, 
            'pipeline_phase': self.args.pipeline_phase, 
            'dataset': self.args.dataset, 
            'attr': self.args.attr, 
            'attr_type': self.args.attr_type, 
            'from_format': self.args.from_format if self.args.from_format else '',
            'to_format': self.args.to_format if self.args.to_format else '',
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
        self.logger.info(json.dumps(item, indent=2, default=str))


    def get_all_formats_by_dataset(self):
        response = super().get_dynamodb_resource().Table('format').scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )
        self.logger.debug(json.dumps(response, indent=2))

        formats_by_dataset = {}
        for f in response['Items']:
            formats_by_dataset[rule['dataset']] = f            

        return formats_by_dataset
