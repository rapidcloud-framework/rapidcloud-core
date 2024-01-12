__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
from datetime import datetime
import logging
import os
import shutil
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra


class DatasetSemistructured(Metadata):

    TABLE_NAME = 'dataset_semi_structured'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.env = super().get_env()

    def save_dataset_semi_structured(self):
        fqn = f"{self.env}_{self.args.name}"

        partitions = self.args.partitions if self.args.partitions else 'year,month,day,timestamp'

        if self.args.enabled and self.args.enabled.lower() in ['yes', 'true', 'y']:
            enable_dataset = True
        else:
            enable_dataset = False

        enrich_name = None
        if self.args.enable_enrich.lower() in ['yes', 'true', 'y']:
            enable_enrich = True
            enrich_name = self.args.enrich_name if hasattr(self.args, 'enrich_name') else 'enrich_semi_structured'
        else:
            enable_enrich = False

        if self.args.enable_transform.lower() in ['yes', 'true', 'y']:
            enable_transform = True
        else:
            enable_transform = False

        if self.args.normalize and self.args.normalize_config:
            with open(self.args.normalize_config) as f:
                normalize_config = json.load(f)
        else:
             normalize_config = " "

        item={
            'fqn': fqn,
            'profile': self.env,
            'category': self.args.category,
            'name': self.args.name,
            'enabled': enable_dataset,
            'pk': self.args.primary_key,
            'partitions': partitions,
            'source_location': self.args.source_location,
            'format': self.args.format,
            'normalize': True if self.args.normalize else False, # applies to xml only
            'normalize_config': normalize_config, # applies to xml only
            'separator_char': self.args.separator_char,
            'use_quotes_around_strings': self.args.use_quotes_around_strings,
            'use_first_row_as_cols': self.args.use_first_row_as_cols,
            'path_to_data': self.args.path_to_data.split(",") if self.args.path_to_data else "",
            'sheet_name': self.args.sheet_name,
            'cdc_type': self.args.cdc_type,
            'enable_enrich': enable_enrich,
            'enable_transform': enable_transform,
            'enrich_name': enrich_name,
            'notes': self.args.notes,
            'timestamp': str(datetime.now()),
        }
        self.logger.info(json.dumps(item, indent=2))
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata")

        # CDC lambdas for DMS and semi-structured
        # create Lambda function for processing files via S3 event notification
        env_vars = {
            "PROFILE": self.env
        }
        layers = {
            "10": f"{self.env}_lambda_layer_awswrangler"
        }

        # create 4 lambda funcions to handle various file sizes
        memory_sizes = super().get_properties("lambda_memory_size_", True)
        super().print_json(memory_sizes)
        for memory_size in memory_sizes:
            params = super().get_lambda_function_params(env_vars, layers)
            params['source_path'] = "cdc"
            params['memory_size'] = memory_size
            super().add_aws_resource('lambda_function', f"cdc_{memory_size}", params)

        # get all datasets for crawler paths
        datasets = self.get_all_datasets()

        # Glue CSV classifier
        classifier = "csv-with-headers-and-double-quotes"
        params = super().get_csv_classifier_params()
        super().add_aws_resource('glue_classifier', classifier, params)

        # Glue crawler for semi-structured data in ingestion 
        params = super().get_glue_crawler_params("ingestion", "semistructured", datasets, [classifier])
        super().add_aws_resource('glue_crawler', 'ingestion-semi-structured', params)

        # Glue crawler for semi-structured data in raw
        params = super().get_glue_crawler_params("raw", "semistructured", datasets)
        super().add_aws_resource('glue_crawler', 'raw-semi-structured', params)

        # Lambda layer for data enrichment 
        if enable_enrich:
            # generate lambda source from template (if doesn't exist yet)
            src_dir_name = f"./src/lambda/{super().get_profile()['client']}/{super().get_profile()['workload']}/{enrich_name}"
            src_file_name = f"{src_dir_name}/main.py"
            if os.path.exists(src_file_name):
                self.logger.info(f"{src_file_name} already exists")
            else:
                os.makedirs(src_dir_name)
                shutil.copyfile(f"./lambda/default_lambda_template/main.py", src_file_name)

                # add lambda 
                params = super().get_lambda_function_params(env_vars)
                if self.args.env_vars is not None:
                    params['env_vars'].update(json.loads(self.args.env_vars))
                params['source_path'] = "default_lambda_template"
                params['memory_size'] = 256
                params['immutable'] = "true"
                super().add_aws_resource('lambda_function', enrich_name, params)

        # create ingestion folder for this dataset
        AwsInfra(self.args).create_ingestion_folder(item)


    def get_dataset(self, name):
        try:
            fqn = f"{self.env}_{name}"
            self.logger.info(f"fqn: {fqn}")
            response = super().get_dynamodb_resource().Table(self.TABLE_NAME).query(
                KeyConditionExpression=Key('fqn').eq(fqn)
            )
            return response
        except Exception as e:
            return None

    def get_all_datasets(self):
        return super().get_dynamodb_resource().Table(self.TABLE_NAME).scan(
            FilterExpression=Attr('profile').eq(self.env)
        )['Items']

    def enable(self, dataset):
        response = super().get_dynamodb_resource().Table(self.TABLE_NAME).update_item(Key={'fqn': dataset['fqn']},
            UpdateExpression="set enabled = :p",
            ExpressionAttributeValues={':p': True}
        )

    def enable_and_trigger(self, dataset):
        bucket = f"{dataset['profile'].replace('_','-')}-ingestion"
        objects = super().get_s3_client().list_objects(
            Bucket=bucket,
            Prefix=f"semistructured/{dataset['name']}"
        )

        if 'Contents' in objects:
            self.enable(dataset)
            for obj in objects['Contents']:
                old_key = obj['Key']
                new_key = f"{old_key}_ENABLED"
                self.logger.info(f"key: {bucket}/{old_key}")
                super().get_s3_resource().Object(bucket, new_key).copy_from(CopySource=f"{bucket}/{old_key}")
                super().get_s3_resource().Object(bucket, old_key).delete()
