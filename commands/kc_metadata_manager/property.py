__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import datetime
from datetime import datetime
import logging
from commands.cli_worker.provider import Provider

class Property(object):

    TABLE_NAME = 'property'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__()
        self.args = args

    def set_default_properties(self):
        self.logger.info("saving default environment properties..")
        with open(f'config/{self.args.cloud}_default_properties.json') as f:
            props_by_type = json.load(f)  
            for type, props in props_by_type.items():
                for name, value in props.items():
                    self.logger.info(f"{type} -> {name} = {value}")
                    self.set_property(type, name, value)

    def set_property(self, type, name, value):
        item={
            'profile': self.args.env, 
            'id': self.args.env,
            'type': type,
            'name': name, 
            'default_value': value,
            'value': value,
            'timestamp': str(datetime.now()),
        }
        Provider(self.args).get_metadata_manager().put_item(self.TABLE_NAME, item)
