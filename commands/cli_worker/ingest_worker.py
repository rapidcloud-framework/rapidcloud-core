#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging

from commands.colors import colors
from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.dataset import Dataset
from commands.kc_metadata_manager.deployment import Deployment 
from commands.kc_metadata_manager.schedule import Schedule 
from commands.kc_metadata_manager.format import Format 
from commands.kc_metadata_manager.source_database import SourceDatabase
from commands.kc_metadata_manager.source_database_mysql import SourceDatabaseMysql
from commands.kc_metadata_manager.source_database_oracle import SourceDatabaseOracle 
from commands.kc_metadata_manager.source_database_mssql import SourceDatabaseMssql 
from commands.kc_metadata_manager.source_database_postgres import SourceDatabasePostgres
from commands.kc_metadata_manager.source_table import SourceTable 
from commands.kc_metadata_manager.dataset_unstructured import DatasetUnstructured
from commands.kc_metadata_manager.dataset_semi_structured import DatasetSemistructured
from commands.kc_metadata_manager.event import Event 
from commands.kc_metadata_manager.stream import Stream
from commands.modules import exec_module

class IngestWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def register_source_database(self):
        print("\nYou're adding an existing relational database to your data ingestion pipeline\n")
        curr_name = ''
        name = super().get_user_input(('name','Database Name', 'Enter Database Name (no spaces)', curr_name, True))
        setattr(self.args, 'name', name)
        info = SourceDatabase(self.args).get_source_database(name)['Items']
        if info:
            info = info[0]
        else:
            info = {}

        curr_engine = info['engine'] if 'engine' in info else ''
        curr_server = info['server'] if 'server' in info else ''
        curr_port = info['port'] if 'port' in info else ''
        curr_user = info['db_user'] if 'db_use' in info else ''
        curr_password = '' # 'Q9CgBM7Zy17lBkfdRM9p1jR80='
        curr_db = info['db'] if 'db' in info else ''
        curr_schema = info['schema'] if 'schema' in info else 'dbo'
        curr_rate_of_change = info['rate_of_change'] if 'rate_of_change' in info else ''
        curr_use_dms = info['use_dms'] if 'use_dms' in info else ''
        # curr_use_ctas = info['use_ctas'] if 'use_ctas' in info else ''

        prompts = {
            'engine': ['engine','Database Engine', 'What database engine is it? (oracle|mysql|postgres)', curr_engine, True], # |mssql
            'server': ['server','Database Server Address', 'Database Server Address (dns or ip address)', curr_server, True],
            'port': ['port','Database Server Port', 'Database Server Port', curr_port, True],
            'db_user': ['db_user','Database User', 'Database User', curr_user, True],
            'password': ['password','Password', 'Password (will be encrypted and never transmitted or stored in plain text)', curr_password, True],
            'db': ['db','Database Name', 'Database Name', curr_db, True],
            'schema': ['schema','Schema Name', 'Schema Name', curr_schema, False],
            'rate_of_change': ['rate_of_change','Rate of Change', 'Rate of Change (GB/hr)', curr_rate_of_change, True],
            'use_dms': ['use_dms','Use DMS', 'Use DMS (yes|no)', curr_use_dms, True],
            # 'use_ctas': ['use_ctas','Use CTAS for initial load', 'Use CTAS (yes|no)', curr_use_ctas, True],
        }

        for key, prompt in prompts.items():
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            info[key] = value

        source_database_item = SourceDatabase(self.args).save_source_database()
        if not self.args.skip_tables:
            print(f"Collecting {self.args.engine} database metadata")
            print(json.dumps(source_database_item, indent=2, default=str))
            if self.args.engine == 'mysql':
                SourceDatabaseMysql(self.args, source_database_item).save_tables()  
            elif self.args.engine == 'oracle':
                SourceDatabaseOracle(self.args, source_database_item).save_tables()  
            elif self.args.engine == 'mssql':
                SourceDatabaseMssql(self.args, source_database_item).save_tables()  
            elif self.args.engine == 'postgres':
                SourceDatabasePostgres(self.args, source_database_item).save_tables()  
            else:
                self.logger.error("Incorrect database engine. Must be one of: [oracle|mssql|mysql|postgres]")  

        print(f"\n{colors.OKGREEN}You've successfully added `{name}` to [{super().get_env()}] environment!{colors.ENDC}\n")

            
    def register_unstructured(self):
        print("\nYou're adding unstructured data source (documents, media and other binary sources) to your data ingestion pipeline\n")
        # kc ingest register-unstructured --name sharepoint_documents --type document --category financials  --size 1200 --count 800 --rate-of-change 5 --source-location /Users/igor/Workspace/kinect/kinect-frameworks/kc-big-data/documents

        curr_name = ''
        name = super().get_user_input(('name','Dataset Name', 'Enter Dataset Name with no spaces (e.g. sharepoint_documents)', curr_name, True))
        setattr(self.args, 'name', name)
        info = DatasetUnstructured(self.args).get_dataset(name)['Items']
        if info:
            info = info[0]
            self.logger.info(info)
        else:
            info = {}

        curr_type = info['type'] if 'type' in info else ''
        curr_category = info['category'] if 'category' in info else ''
        curr_size = info['size'] if 'size' in info else ''
        curr_count = info['count'] if 'count' in info else ''
        curr_rate_of_change = info['rate_of_change'] if 'rate_of_change' in info else ''
        curr_source_location = info['source_location'] if 'source_location' in info else ''
        curr_enable_transform = info['enable_transform'] if 'enable_transform' in info else ''

        prompts = {
            'type': ['type', 'Type', 'Data Type (e.g document, media)', curr_type, True],
            'category': ['category', 'Category', 'Data Category (e.g. financials, legal, products)', curr_category, True],
            'size': ['size', 'Size', 'Approximate Total Size (GB)', curr_size, True],
            'count': ['count', 'Count', 'Total number of files (if known)', curr_count, False],
            'rate_of_change': ['rate_of_change','Rate of Change', 'Rate of Change (GB/hr if known)', curr_rate_of_change, False],
            'source_location': ['source_location', 'Source Location', 'Location in the filesystem (if applicable)', curr_source_location, False],
            'enable_transform': ['enable_transform','Enable Transformation', 'Do you want to enable transformation for this dataset? [yes|no]', curr_enable_transform, True]
        }

        for key, prompt in prompts.items():
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            info[key] = value

        DatasetUnstructured(self.args).save_dataset_unstructured()
        print(f"\n{colors.OKGREEN}You've successfully added `{name}` to [{super().get_env()}] environment!{colors.ENDC}\n")


    def register_semi_structured(self):
        print("\nYou're adding semi-structured data source to your data ingestion pipeline\n")

        curr_name = ''
        name = super().get_user_input(('name','Dataset Name', 'Enter Dataset Name with no spaces', curr_name, True))
        setattr(self.args, 'name', name)
        info = DatasetSemistructured(self.args).get_dataset(name)['Items']
        if info:
            info = info[0]
            self.logger.info(info)
        else:
            info = {}

        curr_format = info['format'] if 'format' in info else ''
        curr_category = info['category'] if 'category' in info else ''
        curr_cdc_type = info['cdc_type'] if 'cdc_type' in info else ''
        curr_separator_char = info['separator_char'] if 'separator_char' in info else ''
        curr_use_quotes_around_strings = info['use_quotes_around_strings'] if 'use_quotes_around_strings' in info else ''
        curr_source_location = info['source_location'] if 'source_location' in info else ''
        curr_enable_transform = info['enable_transform'] if 'enable_transform' in info else ''
        curr_enable_enrich = info['enable_enrich'] if 'enable_enrich' in info else ''
        curr_enrich_name = info['enrich_name'] if 'enrich_name' in info else ''
        curr_partitions = info['partitions'] if 'partitions' in info and info['partitions'].strip() else 'year,month,day,timestamp'

        prompts = {
            'format': ['format', 'Format', 'Data format (csv|json)', curr_format, True],
            'category': ['category', 'Category', 'Data Category (e.g. financials, legal, products)', curr_category, True],
            'cdc_type': ['cdc_type', 'CDC Type', 'CDC Type (delta, cumulative, cumulative_year, cumulative_month, cumulative_day)', curr_cdc_type, True],
            'separator_char': ['separator_char', 'Separator Character', 'Separator Character (for CSV only)', curr_separator_char, False],
            'use_quotes_around_strings': ['use_quotes_around_strings', 'Use Quotes around strings', 'Use Quotes around strings [yes|no]', curr_use_quotes_around_strings, False],
            'source_location': ['source_location', 'Source Location', 'Location in the filesystem (if applicable)', curr_source_location, False],
            'enable_transform': ['enable_transform', 'Enable Transformation', 'Do you want to enable transformation for this dataset? [yes|no]', curr_enable_transform, True],
            'enable_enrich': ['enable_enrich', 'Enable Data Enrichment', 'Do you want to enable data enrichment for this dataset? [yes|no]', curr_enable_enrich, True],
            'enrich_name': ['enrich_name', 'Enrich Lambda Name', 'Enrich Lambda Name', curr_enrich_name, False],
            'partitions': ['partitions', 'Partitions', 'Partitions (comma separated)', curr_partitions, False],
        }

        cmd = "kc ingest register-semi-structured "
        for key, prompt in prompts.items():
            # self.logger.info(key + ": " + str(prompt))
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            info[key] = value
            cmd += f"--{key} \"{value}\" "

        print(cmd)
        DatasetSemistructured(self.args).save_dataset_semi_structured()
        print(f"\n{colors.OKGREEN}You've successfully added `{name}` to [{super().get_env()}] environment!{colors.ENDC}\n")


    def enable_semi_structured(self):
        if super().prompt("Enable all disabled semi-structured datasets") == 'yes':
            dataset_semi_structured = DatasetSemistructured(self.args)
            datasets = dataset_semi_structured.get_all_datasets()
            for dataset in datasets:
                # print(f"{dataset['name']}: {dataset.get('enabled')}")
                if dataset.get('enabled') is not None and not dataset['enabled']:
                    print(f"Enabling/processing {dataset['name']}")
                    dataset_semi_structured.enable_and_trigger(dataset)
                else:
                    dataset_semi_structured.enable(dataset)


    def ingest(self):
        # make sure datalake was created already, if not, create it
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        if self.args.command == 'register-source-database':
            self.register_source_database()    
            
        elif self.args.command == 'show-table':
            SourceTable(self.args).get_source_table(self.args.table_name)

        elif self.args.command == 'schedule':

            print("\nAdding DMS task schedule...\n")
            Schedule(self.args).save_schedule()    
            print(f"\n{colors.OKGREEN}You've successfully added DMS task schedule!{colors.ENDC}\n")

        elif self.args.command == 'add-dataset':

            print("\nAdding database tables to the ingestion pipeline...\n")
            if self.args.include_tables and self.args.include_tables == 'all':
                count = Dataset(self.args).save_all_datasets()   
            elif self.args.include_tables and self.args.include_tables != 'all':
                count = Dataset(self.args).save_datasets()   
            elif self.args.source_table:
                count = Dataset(self.args).save_dataset()    
            print(f"\n{colors.OKGREEN}You've successfully added {count} tables to [{super().get_env()}] ingestion pipeline!{colors.ENDC}\n")

        elif self.args.command == 'register-unstructured':
            self.register_unstructured()

        elif self.args.command == 'register-semi-structured':
            self.register_semi_structured()

        elif self.args.command == 'enable-semi-structured':
            self.enable_semi_structured()

        elif self.args.command == 'add-unstructured-partitions':
            DatasetUnstructured(self.args).save_partitions()

        elif self.args.command == 'add-dataset-partitions':
            Dataset(self.args).save_partitions()

        elif self.args.command == 'register-stream':
            Stream(self.args).save_stream()

        elif self.args.command == 'add-event':

            print("\nAdding real-time event to the ingestion pipeline...\n")
            Event(self.args).save_event()
            print(f"\n{colors.OKGREEN}You've successfully added real-time event to the ingestion pipeline!{colors.ENDC}\n")

        elif self.args.command == 'send-events':
            Event(self.args).send_events()

        elif self.args.command == 'send-files':
            DatasetUnstructured(self.args).send_files()

        elif self.args.command == 'add-format':
            Format(self.args).save_format()

        # elif self.args.command == 'post-crawlers':
        #     if super().prompt("\nChange ingestiondb Glue table data types") == 'yes':
        #         Deployment(self.args).post_crawlers()

        # elif self.args.command == 'post-ingestion':
        #     Deployment(self.args).post_ingestion()

        elif self.args.command == 'start':
            if super().prompt("\nActivate data ingestion pipeline") == 'yes':
                Deployment(self.args).start_pipeline()



