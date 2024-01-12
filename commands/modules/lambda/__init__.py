__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):        
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()

        name = self.args.name
        default_layers_order = {
            "awswrangler": "10",
            "kc_common": "100",
            "psycopg2": "300"
        }
        layers = {}
        for layer in self.args.lambda_include_layers.split(","):
            if layer != "":
                layers[default_layers_order[layer]] = f"{self.get_env()}_lambda_layer_{layer}"
        params = super().get_lambda_function_params(layers=layers, default_layers=False)

        if self.args.lambda_env_vars:
            env_vars = self.args.lambda_env_vars.replace("\\","")
            params['env_vars'].update(json.loads(env_vars))

        if self.args.lambda_memory_size:
            params['memory_size'] = self.args.lambda_memory_size

        if self.args.lambda_timeout:
            params['timeout'] = self.args.lambda_timeout

        if self.args.lambda_schedule:
            params['schedule'] = self.args.lambda_schedule

        params['source_path'] = "default_lambda_template"
        params['immutable'] = True

        super().add_aws_resource('lambda_function', name, params)

        # create CloudWatch Event rule
        if self.args.lambda_schedule:
            # 0 0/15 9-15 ? * MON,TUE,WED,THU,FRI *
            # 5 4 * * ? *
            params ={
                'schedule': self.args.lambda_schedule,
                'target_type': 'lambda_function',
                'target': name,
                'input': {
                    'task_type': self.args.phase
                },       
            }
            super().add_aws_resource('cloudwatch_event_rule', name, params)
