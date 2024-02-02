__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
import logging
from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    logger = logging.getLogger("module.datalake")
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
            return

        profile = super().get_profile()
        response = super().get_dynamodb_resource().Table('datalake').put_item(
            Item={
                'fqn': f"{profile['client']}_{profile['env']}", 
                'client': profile['client'],
                'env': profile['env'],
                'athena_s3_bucket': f"{super().get_env()}-query-results-bucket".replace("_","-"), 
                'timestamp': str(datetime.datetime.now()),
            }
        )

        for bucket in ["ingestion", "raw", "analysis"]:
            super().add_aws_resource('s3_bucket', bucket, {})
            
            # create Lambda function for processing S3 events
            env_vars = {
                "PROFILE": super().get_env()
            }
            params = super().get_lambda_function_params(env_vars)
            lambda_name = "handle_s3_event_" + bucket
            super().add_aws_resource('lambda_function', lambda_name, params)

            params = super().get_s3_bucket_notification_params(bucket, lambda_name)
            super().add_aws_resource('s3_bucket_notification', bucket, params)

            super().add_aws_resource('glue_catalog_database', bucket + 'db', {})
        
            super().add_aws_resource('s3_bucket', 'query-results-bucket', {}, '-')
