__author__ = "Igor Royzis"
__license__ = "MIT"


import json
from datetime import datetime
import logging
import os
import time
from progress.bar import Bar
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata

class DatasetUnstructured(Metadata):

    TABLE_NAME = 'dataset_unstructured'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def save_dataset_unstructured(self):
        if self.args.rules:
            rules = json.loads(self.args.rules.replace("\\",""))
        else:
            rules = []

        item={
            'fqn': f"{super().get_env()}_{self.args.name}", 
            'profile': super().get_env(), 
            'type': self.args.type,
            'category': self.args.category,
            'name': self.args.name,
            'size': self.args.size if self.args.size else 0,
            'count': self.args.count if self.args.count else 0,
            'rate_of_change': self.args.rate_of_change if self.args.rate_of_change else 0,
            'source_location': self.args.source_location,
            'type': self.args.type,
            'enable_transform': getattr(self.args, "enable_transform", "false") == "true",
            'enable_textract': getattr(self.args, "enable_textract", "false") == "true",
            'textract_fields': self.args.textract_fields,
            'rules': rules,
            'multiple_sections': getattr(self.args, "multiple_sections", "no"),
            'section_id_name': getattr(self.args, "section_id_name", ""),
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata")

        # create Lambda function for processing files via S3 event notification
        env_vars = {
            "PROFILE": super().get_env()
        }
        layers = {
            "1": f"{super().get_env()}_lambda_layer_kc_textract"
        }
        params = super().get_lambda_function_params(env_vars, layers)

        # overload params to trigger container lambda tf execution
        with open('./config/kc_config.json', 'r') as f:
            kc_config = json.load(f)
            textract_image_uri = kc_config.get('textract', {}).get('textract_image_uri')
        params['image_uri'] = textract_image_uri

        super().add_aws_resource('lambda_function', 'file_workflow', params)

        # ruels processor lambda
        if item["enable_textract"]:
            params = super().get_lambda_function_params(env_vars)
            params['immutable'] = "true"
            super().add_aws_resource('lambda_function', 'rules_processor', params)



    def get_dataset(self, name):
            fqn = super().get_env() + '_' + name
            response = super().get_dynamodb_resource().Table(self.TABLE_NAME).query(
                KeyConditionExpression=Key('fqn').eq(fqn)
            )
            return response

    # ------------------------------------------------------------------------------------
    # Upload multiple files to S3
    # ------------------------------------------------------------------------------------
    def send_files(self):
        fqn = super().get_env() + '_' + self.args.dataset_name
        dataset_unstructured = super().get_dynamodb_resource().Table(self.TABLE_NAME).get_item(Key={'fqn': fqn})['Item']

        # set timestamp verification flag if provided
        if self.args.timestamp_after is not None:
            self.logger.info(f"timestamp_after {self.args.timestamp_after}")
            timestamp_after = datetime.strptime(self.args.timestamp_after, '%Y-%m-%d %H:%M:%S').timestamp()
            check_timestamp = True
        else:
            check_timestamp = False

        self.logger.debug(json.dumps(dataset_unstructured, indent=2))
        self.logger.debug(self.args.location)

        # collect file names to send        
        files = [] # list of tuples (dirs, path, name)
        for root, dirs, file_names in os.walk(self.args.location):
            for name in file_names:
                path = os.path.join(root, name)

                # check for file timestamp if provided
                if check_timestamp:
                    # Last modification time since the epoch: 1558447897.0442736
                    file_timestamp = os.path.getmtime(path)
                    modified_on = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path)))
                    self.logger.debug(name + ': modified on ' + str(modified_on))

                    if file_timestamp > timestamp_after:
                        send_file = True
                    else:    
                        send_file = False
                else:
                    send_file = True        

                if send_file:
                    files.append((dirs, path, name))

        progress = Bar('Uploading files to S3', max=len(files))
        for file in files:
            self.send_file(dataset_unstructured, file)   
            progress.next()
        progress.finish()
     


    # ------------------------------------------------------------------------------------
    # Upload single file to S3
    # ------------------------------------------------------------------------------------
    def send_file(self, dataset_unstructured, file):
        (dirs, path, name) = file

        # key format: "files/{type}/{target_path}/{dir1}/{dir...}/{name}/{partition1}/{partition...}/{timestamp}/{name}"
        # example: "files/sharepoint_documents/accounting/dir1/dir2/document.docx/2020/5/26/20200526111904-document.docx"
        key = f"files/{dataset_unstructured['name']}"

        # append target path if provided
        if self.args.target_path is not None:
            key = f"{key}/{self.args.target_path}"         

        # append sub-directories if any
        relative_path = path.split(self.args.location,1)[1]
        if relative_path:
            key = f"{key}{relative_path}" 
        # self.logger.info("\n" + key)

        # construct partitions /YYYY/MM/DD
        dt = datetime.today()
        partition = f"{dt.year}/{dt.month}/{dt.day}"

        # construct final object name
        timestamp = time.strftime('%Y%m%d%H%M%S')
        key = f"{key}/{partition}/{timestamp}_{name}" 
        # self.logger.info(key + "\n\n")

        bucket = (super().get_env() + '-ingestion').replace('_','-')
        self.logger.debug(f" Uploading [{name}] to {bucket}/{key}")
        super().get_s3_client().upload_file(path, bucket, key)

        # tag the file
        response = super().get_s3_client().put_object_tagging(Bucket=bucket,Key=key,
            Tagging={
                'TagSet': [
                    {'Key': 'type','Value': dataset_unstructured['type']},
                    {'Key': 'category','Value': dataset_unstructured['category']},
                ]
            }
        )

        # update file metadata 
        fqn = f"{super().get_env()}_{dataset_unstructured['name']}_{name}"
        item={
            'fqn': fqn, 
            'type': dataset_unstructured['type'], 
            'category': dataset_unstructured['category'], 
            'dataset': dataset_unstructured['name'], 
            'source_path': path, 
            'bucket': bucket,
            'key': key,
            'profile': super().get_env(), 
            'timestamp': str(datetime.now()),
        }
        super().put_item('file', item)

