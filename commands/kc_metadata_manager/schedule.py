__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr
from commands.kc_metadata_manager.aws_metadata import Metadata

class Schedule(Metadata):

    TABLE_NAME = 'schedule'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def save_schedule(self):
        type = self.args.type
        source_database = self.args.source_database
        if self.args.enabled and self.args.enabled.lower() in ['yes', 'true', 'y']:
            enabled = True
        else:
            enabled = False
        task = f"{super().get_env()}_{source_database}_{type}"
        item={
            'task': task, 
            'profile': super().get_env(),
            'source_database': source_database,
            'type': type,
            'schedule': self.args.schedule,
            'enabled': enabled,
            'timestamp': str(datetime.now()),
        }

        if type == 'full':
            target = f'{source_database}_run_small_tables_dms_task'
        elif type == 'inserts' or type == 'updates':
            target = f'{source_database}_run_timestamp_based_dms_task'

        # create CloudWatch Event Rule
        params ={
            'schedule': self.args.schedule,
            'target_type': 'lambda_function',
            'target': target,
            'input': {'task_type': type},       
        }
        rule_name = f"{source_database}_{type}"
        super().add_aws_resource('cloudwatch_event_rule', rule_name, params)

        item['cloudwatch_event_rule'] = params
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata", rule_name)


    def get_all_schedules(self):
        return super().get_dynamodb_resource().Table('schedule').scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )['Items']
