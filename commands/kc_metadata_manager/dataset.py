__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import datetime
from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.source_table import SourceTable
from commands.kc_metadata_manager.source_table import SourceTable

class Dataset(Metadata):

    TABLE_NAME = 'dataset'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def get_size(self, source_table_info):
        size = self.args.size
        if size is None:
            sizes = {
                "dataset_size_small_max_gb": super().get_property("dataset_size_small_max_gb"),
                "dataset_size_medium_max_gb": super().get_property("dataset_size_medium_max_gb"),
                "dataset_size_large_max_gb": super().get_property("dataset_size_large_max_gb"),
            } 

            if source_table_info['data_length'] != 'n/a':
                size_gb = source_table_info['data_length'] / 1024 / 1024 / 1024
                if size_gb < sizes["dataset_size_small_max_gb"]:
                    size = "small"
                elif size_gb < sizes["dataset_size_medium_max_gb"]:
                    size = "medium"
                elif size_gb < sizes["dataset_size_large_max_gb"]:
                    size = "large"
                else:
                    size = "xlarge"
            else:
                size = "n/a"                
        return size


    # def get_cdc_via(self, source_table_info):
    #     if size is None:
    #         max = super().get_property("dataset_size_small_max_gb")
    #     return 'DMS' if self.args.size != ('small') else 'n/a'


    def save_dataset_item(self, name, source_table_info):
        name = name.lower()
        env = super().get_env()
        source_database = source_table_info['database']
        source_schema = source_table_info['table_schema']
        source_table = self.args.source_table if self.args.source_table else name
        source_table_fqn = f"{env}_{source_database}_{source_schema}_{source_table}".lower()
        partitions = self.args.partitions if self.args.partitions else 'n/a'

        prefix = None
        if self.args.prefix is not None:
            prefix = self.args.prefix
            name = prefix + name

        size = self.get_size(source_table_info)
        ingested_via = 'DMS' if size != ('xlarge') else 'extracts'
        cdc_via = 'DMS' if size != ('small') else 'reload'

        pk = super().get_dynamodb_resource().Table('source_table').get_item(Key={'fqn': source_table_fqn})['Item']['pk']
        fqn = f"{env}_{name}"
        ingestion_db = f"{env}_ingestiondb"
        ingestion_location = (f"s3://{env.replace('_','-').lower()}-ingestion/databases/{source_database}/{source_schema}/{name}")
        raw_db = f"{env}_rawdb"
        raw_location = (f"s3://{env.replace('_','-').lower()}-raw/databases/{self.args.source_database}/{self.args.source_schema}/{name}")
        insert_timestamp = self.args.insert_timestamp
        update_timestamp = self.args.update_timestamp

        item = {
            'fqn': fqn, 
            'profile': super().get_env(),
            'name': name,
            'prefix': prefix,
            'datalake': self.args.datalake,
            'source_database': source_database,
            'source_schema': source_schema,
            'source_table': source_table,
            'size': size,
            'pk': pk,
            'partitioned_by': partitions,
            'ingested_via': ingested_via,
            'format': 'parquet',
            'compression': 'NONE',
            'cdc_via': cdc_via,
            'cdc_type': 'delta',
            'ingestion_catalog': ingestion_db,
            'ingestion_location': ingestion_location,
            'raw_catalog': raw_db,
            'raw_location': raw_location,
            'ingested': 'False',
            'organized': 'False',
            'insert_timestamp': insert_timestamp,
            'update_timestamp': update_timestamp,
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata", name)

        # Glue crawler for datasets in raw
        datasets = self.get_all_datasets()
        # kinect-theia-2-raw/databases/theia_oracle/admin/test_oracle_orders/
        # f"s3://{bucket}/databases/{source_database}/{source_schema.lower()}/{name}"
        folder = f"databases/{source_database}/{source_schema}".lower()
        params = super().get_glue_crawler_params("raw", folder, datasets)
        super().add_aws_resource('glue_crawler', 'raw-dataset', params)


    def save_all_datasets(self):
        source_tables = SourceTable(self.args).get_source_tables_for_database(self.args.source_database)
        i = 0
        for source_table in source_tables:
            i += 1
            self.logger.info(f"{i}: {source_table['table_name']}")
            self.save_dataset_item(source_table['table_name'], source_table)
        return len(source_tables)


    def save_datasets(self):
        datasets = self.args.include_tables.replace(' ', '').split(',')
        self.logger.info(datasets)
        for dataset in datasets:
            fqn = f"{super().get_env()}_{self.args.source_database}_{self.args.source_schema}_{dataset}".lower()
            self.logger.info(fqn)
            source_table = SourceTable(self.args).get_source_table(fqn)
            self.save_dataset_item(dataset, source_table)
        return len(datasets)


    def save_dataset(self):
        self.logger.info(self.args.name)
        fqn = f"{super().get_env()}_{self.args.source_database}_{self.args.source_schema}_{self.args.name}"
        source_table = SourceTable(self.args).get_source_table(fqn)
        self.save_dataset_item(self.args.name, source_table)
        return 1


    def get_dataset(self,dataset_name):
        response = super().get_dynamodb_resource().Table('dataset').query(
            KeyConditionExpression=Key('fqn').eq('dataset_name')
        )
        return response


    def get_all_datasets(self):
        response = super().get_dynamodb_resource().Table('dataset').scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )
        return response['Items']


    def get_all_dms_datasets(self):
        response = super().get_dynamodb_resource().Table('dataset').scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) & Attr('ingested_via').eq('DMS') 
        )
        return response['Items']


    def save_partitions(self):
        fqn = super().get_env() + '_' + self.args.dataset_name
        response = super().get_dynamodb_resource().Table('dataset').update_item(Key={'fqn': fqn},
            UpdateExpression="set partitioned_by = :p",
            ExpressionAttributeValues={':p': self.args.partitions},
            ReturnValues="UPDATED_NEW"
        )
        self.logger.debug(json.dumps(response, indent=2))
