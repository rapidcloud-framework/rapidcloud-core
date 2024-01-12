__author__ = "Igor Royzis"
__copyright__ = "Copyright 2021, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import datetime
import logging
import os
import shutil
from boto3.dynamodb.conditions import Key, Attr
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra 

class Stream(Metadata):

    TABLE_NAME = 'stream'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)


    def save_stream(self):
        env = super().get_env()
        name = self.args.name   
        stream_type = self.args.type
        consumer = self.args.consumer  
        consumer_name = f"{name}_{stream_type}_stream_consumer"
        event_source_arn = self.args.event_source_arn  
        fqn = f"{env}_{name}_{stream_type}" 

        item={
            'fqn': fqn, 
            'profile': env, 
            'name': name,
            'type': stream_type,
            'event_source_arn': event_source_arn,
            'consumer': consumer,
            'consumer_name': consumer_name,
            'enabled': True, 
            'timestamp': str(datetime.datetime.now())
        }
        self.logger.info(json.dumps(item, indent=2))
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata")
                
        if consumer == 'lambda_function':
        
            # generate lambda source form template
            src_dir_name = f"./src/lambda/{super().get_profile()['client']}/{super().get_profile()['workload']}/{consumer_name}"
            src_file_name = f"{src_dir_name}/main.py"
            if not os.path.exists(src_file_name):
                os.makedirs(src_dir_name)
                shutil.copyfile(f"./lambda/kinesis_consumer_lambda_template/main.py", src_file_name)
            
            # add lambda 
            env_vars = {
                "PROFILE": super().get_env()
            }
            layers = {
                "10": f"{super().get_env()}_lambda_layer_awswrangler"
            }
            params = super().get_lambda_function_params(env_vars, layers)
            if self.args.env_vars:
                params['env_vars'].update(json.loads(self.args.env_vars))
            params['source_path'] = "kinesis_consumer_lambda_template"
            params['memory_size'] = self.args.memory_size if self.args.memory_size else 128
            params['immutable'] = "true"
            super().add_aws_resource('lambda_function', consumer_name, params)

            # Add lambda event source
            params = super().get_lambda_event_source_params(consumer_name, event_source_arn)
            super().add_aws_resource('lambda_event_source_mapping', consumer_name, params)

        elif consumer == 'glue_streaming':
            
            params = super().get_glue_job_params(consumer_name, "gluestreaming", name)
            super().add_aws_resource('glue_job', consumer_name, params)
            template = "modules/kc_streaming_glue_job_template"
            new_job = f"src/glue/{consumer_name}"
            super().create_from_template(template, new_job)
            local_script = f"{new_job}/main.py"
            AwsInfra(self.args).upload_glue_code(consumer_name, local_script)

        else:
            self.logger.error(f"{consumer} consumer type is not supported")
            return
        

    def get_all_streams(self):
        return super().get_dynamodb_resource().Table(self.TABLE_NAME).scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )['Items']
