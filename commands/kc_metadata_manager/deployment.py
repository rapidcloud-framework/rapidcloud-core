__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import copy
import botocore

from commands.kc_metadata_manager.aws_infra import AwsInfra 
from commands.kc_metadata_manager.dataset_semi_structured import DatasetSemistructured
from commands.kc_metadata_manager.dataset import Dataset 
from commands.kc_metadata_manager.transformation import Transformation 
from commands.kc_metadata_manager.rule import Rule 
from commands.kc_metadata_manager.schedule import Schedule 
from data_scripts.kc_ingest_ctas import IngestCtas
from data_scripts.kc_transform_job import TransformationJob


class Deployment(AwsInfra):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.env = super().get_env()

    # ------------------------------------------------------------------------------------
    # Start - Update DMS tasks, Generate catalogs, Glue jobs, Enable event rules, etc 
    # Note: do this after terraform apply
    # ------------------------------------------------------------------------------------
    def start_pipeline(self):
        step = 0

        datasets = Dataset(self.args).get_all_dms_datasets()
        if len(datasets) > 0:
            step += 1 
            if super().prompt(step, "Update table mappings for DMS Tasks") == 'yes':
                self.add_datasets_to_dms(datasets)

        # disable for now
        # datasets = Dataset(self.args).get_all_datasets()
        # if len(datasets) > 0:
        #     step += 1 
        #     if super().prompt(step, "Update ingestion Glue catalogs") == 'yes':
        #         setattr(self.args, 'datasets', 'all')
        #         IngestDDL().main(self.args)

        transformations = Transformation(self.args).get_all_transformations()
        if len(transformations) > 0:
            step += 1 
            if super().prompt(step, "Generate transformation Glue job templates") == 'yes':
                self.generate_transform_jobs()

        schedules = Schedule(self.args).get_all_schedules()
        if len(schedules) > 0:
            step += 1 
            if super().prompt(step, "Activate DMS ingestion schedules") == 'yes':
                self.enable_cloudwatch_event_rules()

        step += 1 
        if super().prompt(step, "Deploy Glue jobs. This will replace existing Glue code") == 'yes':
            self.deploy_glue_transform_code()


    def generate_transform_jobs(self):
        config = super().get_json_file("config/aws_profile.json")
        setattr(self.args, 'aws_profile', config['aws_profile'])
        setattr(self.args, 'profile', self.env)
        setattr(self.args, 'env_prefix', super().get_profile()['env'])
        setattr(self.args, 'output_folder_path', f"./src/glue/transform/{self.env}")
        setattr(self.args, 'aws_region', self.profile['region'])
        setattr(self.args, 'datasets', 'all')
        TransformationJob().main(self.args)


    def deploy_glue_transform_code(self):
        transforms = Transformation(self.args).get_all_transformations()
        bucket = f"{self.env.replace('_','-')}-glue-scripts"

        # main transform job
        local_script = f"./data_scripts/job_templates/kc_transform_main_job_template.py"
        self.logger.debug(f"deploying Glue job script: s3://{bucket}/transform_main.py")
        print(f"\tdeploying transform_main.py")
        super().get_s3_client().upload_file(local_script, bucket, "transform_main.py")

        for t in transforms:
            job_name = f"transform_{t['name']}"
            local_script = f"./src/glue/transform/{super().get_profile()['client']}/{super().get_profile()['workload']}/{job_name}.py"
            s3_key = f"{job_name}.py"
            self.logger.debug(f"deploying Glue job script: s3://{bucket}/{s3_key}")
            print(f"\tdeploying {job_name}")
            super().get_s3_client().upload_file(local_script, bucket, s3_key)


    def test(self):
        # setattr(self.args, 'datasets', 'all')
        # IngestDDL().main(self.args)

        # self.generate_transform_jobs()

        self.deploy_glue_transform_code()

        pass


    #------------------------------------------------------------------------------------
    # Copy data from ingestiondb to rawdb via CTAS (only for RDBMS)
    #------------------------------------------------------------------------------------
    def post_ingestion(self):
        step = 0

        datasets = Dataset(self.args).get_all_datasets()
        if len(datasets) > 0:
            step += 1 
            if super().prompt(step, "Copy data from ingestiondb to rawdb via CTAS") == 'yes':
                setattr(self.args, 'datasets', 'all')
                IngestCtas().main(self.args)
        else:
            self.logger.info(f"No RDBMS data sources enabled for ingestion")

    #------------------------------------------------------------------------------------
    # Run crawlers for specific phase (ingestion, raw, analysis)
    #------------------------------------------------------------------------------------
    def run_crawlers(self):
        step = 0

        crawlers = super().get_resources("glue_crawler")
        if len(crawlers) > 0:
            bucket = f"{self.env.replace('_','-')}-{self.args.pipeline_phase}"
            self.logger.info(f"bucket: {bucket}")
            for crawler in crawlers:
                path = crawler['params']['s3_target']['path'][0]
                self.logger.info(f"path: {path}")
                crawler_name = f"{self.env}_{crawler['resource_name']}"
                self.logger.info(f"crawler: {crawler_name}")
                if bucket in path:
                    step += 1 
                    if super().prompt(step, f"Run Glue crawler [{crawler['resource_name']}] ") == 'yes':
                        self.logger.info(f"running {crawler_name}")
                        super().get_glue_client().start_crawler(Name=crawler_name)
        else:
            self.logger.info("No crawlers to run")


    # ------------------------------------------------------------------------------------
    # Change CSV tables to use org.apache.hadoop.hive.serde2.OpenCSVSerde if needed
    # ------------------------------------------------------------------------------------
    def post_crawlers(self):
        step = 0
        datasets = DatasetSemistructured(self.args).get_all_datasets()
        if len(datasets) > 0:
            step += 1 
            
            catalog_config = {}
            if self.args.config:
                config_file = self.args.config
                with open(config_file, 'r') as f:
                    filesize = os.path.getsize(config_file)
                    if filesize > 0:
                        catalog_config = json.load(f)  
            
            self.logger.info(json.dumps(catalog_config, indent=2))

            for dataset in datasets:
                if self.args.table_name in ('all', dataset['name']):
                    if dataset['format'] == 'csv' and dataset['use_quotes_around_strings']:
                        db = f"{dataset['profile']}_ingestiondb"
                        table = dataset['name'].lower()
                        try:
                            table_info = super().get_glue_client().get_table(
                                DatabaseName=db,
                                Name=f"{table}"
                            )['Table']
                            self.logger.info(dataset['name'])
                            
                            table_info['StorageDescriptor']['SerdeInfo']['SerializationLibrary'] = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
                            table_info['StorageDescriptor']['SerdeInfo']['Parameters']['separatorChar'] = f"{dataset['separator_char']}"
                            table_info['StorageDescriptor']['SerdeInfo']['Parameters']['quoteChar'] = "\""

                            for attr in ['DatabaseName','CreateTime','UpdateTime','CreatedBy','IsRegisteredWithLakeFormation','CatalogId']:
                                table_info.pop(attr)

                            # change data types as specified in catalog config json
                            if table in catalog_config:
                                for k,v in catalog_config[table].items():
                                    for glue_col in table_info['StorageDescriptor']['Columns']:
                                        if glue_col['Name'] == k:
                                            glue_col['Type'] = v
                            
                            # convert data types
                            if self.args.from_format and self.args.to_format:
                                for glue_col in table_info['StorageDescriptor']['Columns']:
                                    if glue_col['Type'] == self.args.from_format:
                                        glue_col['Type'] = self.args.to_format
                                        self.logger.info(f"{table}: {glue_col['Name']} -> {glue_col['Type']}")


                            response = super().get_glue_client().update_table(
                                DatabaseName=db,
                                TableInput=table_info
                            )
                            self.logger.info("After:")
                            self.logger.info(json.dumps(response, indent=2, default=super().json_converter))
                                            
                        except Exception as e:
                            self.logger.error(e.args)
                        

    # ------------------------------------------------------------------------------------
    # Run analysis crawlers. Do this after transformations wrote output to analysis bucket
    # ------------------------------------------------------------------------------------
    def post_transform(self):
        step = 0 
        crawlers = super().get_resources("glue_crawler")
        if len(crawlers) > 0:
            for crawler in crawlers:
                bucket = f"{self.env.replace('_','-')}-analysis"
                if bucket in crawler['params']['s3_target']['path'][0]:
                    step += 1 
                    if super().prompt(step, f"Run {crawler['resource_name']} Glue crawler") == 'yes':
                        super().get_glue_client().start_crawler(Name=f"{self.env}_{crawler['resource_name']}")

        # publishing = Publishing(self.args).get_all_publishing()
        # if len(publishing) > 0:
        #     for dataset in publishing:
        #         if dataset['db_engine'] == 'redshift':
        #             step += 1
        #             if super().prompt(step, "Generate publish Glue job templates for Redshift") == 'yes':
        #                 PublishRedshiftJob().main(self.args)


    # ------------------------------------------------------------------------------------
    # set up initial DMS tasks/mappings
    # ------------------------------------------------------------------------------------
    def add_datasets_to_dms(self, datasets):
        ALL_MAPPINGS = { 
            "rules": [
            ] 
        }

        SINGLE_TABLE_MAPPING = { 
            "rule-type": "selection", 
            "rule-id": "<RULE_ID>", 
            "rule-name": "<RULE_NAME>", 
            "object-locator": { 
                "schema-name": "<VAR_SCHEMA>", 
                "table-name": "<VAR_TABLE>" 
            }, 
            "rule-action": "include", 
            "load-order": "<VAR_LOAD_ORDER>", 
        }

        REMOVE_COLUMN_RULE = {
            "rule-type": "transformation",
            "rule-id": "<RULE_ID>", 
            "rule-name": "<RULE_NAME>", 
            "rule-target": "column",
            "object-locator": {
                "schema-name": "<VAR_SCHEMA>", 
                "table-name": "<VAR_TABLE>", 
                "column-name": "<VAR_COLUMN>"
            },
            "rule-action": "remove-column"
        }

        # add datasets to table mappings
        table_mappings = {}
        rules = {}
        i = 2  
        
        # get rules (e.g. omit)
        rules_by_dataset = Rule(self.args).get_all_rules_by_dataset()

        for dataset in datasets:
            dms_task_suffixes = [
                '-large-tables-initial',
                '-large-tables-full-and-cdc'
            ]

            for dms_task_suffix in dms_task_suffixes:
                dms_task_id = (self.env + '-' + dataset['source_database'] + dms_task_suffix).replace('_','-')

                # check if DMS task exists
                try:
                    response = super().get_dms_client().describe_replication_tasks(Filters = [{'Name': 'replication-task-id', 'Values': [dms_task_id]}])
                except botocore.exceptions.ClientError:
                    continue
                except botocore.errorfactory.ResourceNotFoundFault:
                    continue

                if len(response['ReplicationTasks']) > 0:
                    dms_task_arn = response['ReplicationTasks'][0].get('ReplicationTaskArn')
                else:
                    continue # this DMS taks doesn't exist. Try next one.

                # DMS task per source database (could be more than one)
                if dms_task_arn not in table_mappings:
                    table_mappings[dms_task_arn] = copy.deepcopy(ALL_MAPPINGS) 
                    rules = {} 

                if dataset['size'] != 'small':
                    print(f"\tadding {dataset['name']} ({dataset['size']}) to DMS task {dms_task_id}")
    
                    table_mapping = copy.deepcopy(SINGLE_TABLE_MAPPING)
                    table_mapping['rule-id'] = str(i)
                    table_mapping['rule-name'] = str(i)
                    table_mapping['object-locator']['schema-name'] = dataset['source_schema']
                    table_mapping['object-locator']['table-name'] = dataset['source_table']
                    table_mapping['load-order'] = i * 10
                    table_mappings[dms_task_arn]['rules'].append(table_mapping)

                    if dataset['name'] in rules_by_dataset:
                        rule = rules_by_dataset[dataset['name']]
                        if rule['action'] == 'omit':
                            column_rule = copy.deepcopy(REMOVE_COLUMN_RULE)
                            column_rule['rule-id'] = str(i + 500)
                            column_rule['rule-name'] = str(i + 500)
                            column_rule['object-locator']['schema-name'] = dataset['source_schema']
                            column_rule['object-locator']['table-name'] = dataset['source_table']
                            column_rule['object-locator']['column-name'] = rule['attr']
                            table_mappings[dms_task_arn]['rules'].append(column_rule)

                    i += 1

        # modify DMS task with new table mappings
        self.logger.debug(json.dumps(table_mappings, indent=2))
        for item in table_mappings.items():
            # self.logger.debug(json.dumps(item[1], indent=2))
            response = super().get_dms_client().modify_replication_task(
                ReplicationTaskArn = item[0],
                TableMappings = json.dumps(item[1], indent=2)
            )
            self.logger.debug(response)