__author__ = "iroyzis@kinect-consulting.com"

import json
import sys
import importlib
import os

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.print_utils import print_grid_from_json

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.boto3_session = super().get_boto3_session()


    def pause(self, metadata=None):
        self.logger.info("pausing workload resources:")
        self.pause_or_resume("pause")
            

    def resume(self, metadata=None):
        self.logger.info("resuming workload resources:")
        self.pause_or_resume("resume")


    def pause_or_resume(self, action):
        event = {
            "action": action,
            "resource_types": self.args.workload_resource_type
        }
        self.logger.info(json.dumps(event, indent=2))
        
        sys.path.append("./lambda")
        os.environ['PROFILE'] = self.env
        aws_workload = importlib.import_module('kc_common.aws_workload')
        aws_workload.pause_or_resume(event)


    def schedule(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra()
        schedule_name = metadata['name']

        self.logger.info("scheduling workload resources:")
        schedules = {
            "pause": self.args.workload_scheduled_pause,
            "resume": self.args.workload_scheduled_resume
        }
        for action, schedule in schedules.items():
            if schedule is not None:
                params = {
                    'schedule': schedule,
                    'target_type': 'lambda_function',
                    'target': "workload_event_handler",
                    'input': {
                        'action': action,
                        'schedule_name': schedule_name
                    }       
                }
                event_rule_name = f"{action}_workload_{schedule_name}"
                super().add_aws_resource('cloudwatch_event_rule', event_rule_name, params)


    def enable_pause(self, metadata=None):
        # workload event handler lambda function
        lambda_function_name = "workload_event_handler"
        layers = {
            "100": f"{self.env}_lambda_layer_kc_common"
        }
        params = super().get_lambda_function_params(layers=layers, default_layers=False)
        params['source_path'] = lambda_function_name
        params['memory_size'] = 128
        super().add_aws_resource('lambda_function', lambda_function_name, params, role_name="workload")


    def status(self, metadata=None):
        sys.path.append("./lambda")
        os.environ['PROFILE'] = self.env
        aws_workload = importlib.import_module('kc_common.aws_workload')
        status = aws_workload.status()
        print_grid_from_json(status, cols=["res_type","status","arn"])
        return status
