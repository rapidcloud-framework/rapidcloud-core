__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.source_table import SourceTable

class SourceDatabase(Metadata):

    TABLE_NAME = 'source_database'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.env = super().get_env()
        self.args = args

    def get_source_database(self):
        return self.get_dynamodb_resource().Table('SourceDatabase').scan()

    def save_source_database(self):
        fqn = self.env + '_' + self.args.name
        password_secret_name = self.env + '/' + self.args.engine + '/' + self.args.name
        source_database_item={
            'fqn': fqn, 
            'profile': self.env, 
            'name': self.args.name, 
            'engine': self.args.engine,
            'server': self.args.server,
            'port': self.args.port,
            'db': self.args.db, # mssql, oracle
            'schema': self.args.schema, # all engines
            'db_user': self.args.db_user,
            'timestamp': str(datetime.now()),
            'size_gb': 0, # updated later
            'rate_of_change': self.args.rate_of_change, # GB/hr
            'use_dms': self.args.use_dms,
            'use_ctas': self.args.use_ctas,
            'password': password_secret_name
        }
        super().put_item(self.TABLE_NAME, source_database_item)
        super().build_metadata_item(source_database_item, "metadata")

        # save password in secrets manager
        password_secret_name = super().save_password(self.env, self.args.engine, self.args.name, self.args.password)

        # # glue connection
        # glue_conn_params = super().get_glue_conn_params(secret_name)
        # super().add_aws_resource('glue_connection', self.args.name + '_jdbc_conn', glue_conn_params)

        # DMS resources will only be created if "use_dms" argument is "yes"
        if self.args.use_dms in ['true', 'yes']:

            params = super().get_dms_replication_instance_params()
            super().add_aws_resource('dms_replication_instance', 'main', params)

            # create DMS source endpoint   
            params = super().get_dms_source_endpoint_params(password_secret_name)
            super().add_aws_resource('dms_source_endpoint', self.args.name + '-source', params)
            
            # create DMS target endpoint   
            params = super().get_dms_target_endpoint_params()
            super().add_aws_resource('dms_s3_target_endpoint', self.args.name + '-target', params)

            # create DMS tasks
            max_roc = super().get_property('dms_ongoing_replication_max_rate_of_change')
            roc = self.args.rate_of_change
            if not roc:
                roc = "1"
            source_ids = [] # for DMS event subscription

            self.logger.info(f"max_roc={max_roc}, rate_of_change={roc}")
            if int(roc) > int(max_roc): 

                # create DMS task for initial ingestion of large tables
                params = super().get_dms_task_params(max_roc, roc)
                large_task_name = self.args.name + '_large_tables_initial'
                super().add_aws_resource('dms_replication_task', large_task_name, params)
                source_ids.append(f"{self.env}-{large_task_name}")
                
                # create DMS task for daily ingestion of inserts 
                params = super().get_dms_task_params(max_roc, roc)
                inserts_task_name = self.args.name + '_timestamp_based_cdc_inserts'
                super().add_aws_resource('dms_replication_task', inserts_task_name, params)
                source_ids.append(f"{self.env}-{inserts_task_name}")
                
                # create DMS task for daily ingestion of updates 
                params = super().get_dms_task_params(max_roc, roc)
                updates_task_name = self.args.name + '_timestamp_based_cdc_updates'
                super().add_aws_resource('dms_replication_task', updates_task_name, params)
                source_ids.append(f"{self.env}-{updates_task_name}")       

                # create Lambda function for starting daily DMS timestamp based CDC
                env_vars = {
                    "DMS_TASK_ID_INSERTS": (self.env + '-' + inserts_task_name).replace("_", "-"),
                    "DMS_TASK_ID_UPDATES": (self.env + '-' + updates_task_name).replace("_", "-"),
                    "PROFILE": self.env
                }
                params = super().get_lambda_function_params(env_vars)
                params['source_path'] = "run_timestamp_based_dms_task"
                lambda_function_name = f"{self.args.name}_run_timestamp_based_dms_task"
                super().add_aws_resource('lambda_function', lambda_function_name, params)

            else:
                # create DMS task for initial ingestion of large tables and cdc 
                params = super().get_dms_task_params(max_roc, roc)
                large_task_name = self.args.name + '_large_tables_full_and_cdc'
                super().add_aws_resource('dms_replication_task', large_task_name, params)
                source_ids.append(f"{self.env}-{large_task_name}")   

            # daily small tables task    
            params = super().get_dms_task_params(max_roc, roc)
            params['migration_type'] = "full-load"
            small_task_name = self.args.name + '_small_tables_daily'
            super().add_aws_resource('dms_replication_task', small_task_name, params)
            source_ids.append(f"{self.env}-{small_task_name}")
            
            # create DMS event subscription
            params = super().get_dms_event_subscription_params()
            params['source_ids'] = []
            for source_id in source_ids:
                params['source_ids'].append(source_id.replace('_','-'))
            super().add_aws_resource('dms_event_subscription', self.args.name + '_dms_event', params)

            # create Lambda function for starting daily DMS small tables ingestion
            env_vars = {
                "DMS_TASK_ID": (self.env + '-' + small_task_name).replace('_','-'),
                "DATABASE": self.args.name,
                "PROFILE": self.env
            }
            params = super().get_lambda_function_params(env_vars)
            params['source_path'] = "run_small_tables_dms_task"
            lambda_function_name = f"{self.args.name}_run_small_tables_dms_task"
            super().add_aws_resource('lambda_function', lambda_function_name, params)
            
            # create daily Glue trigger
            params = super().get_glue_trigger_params("ON_DEMAND", 'main')
            super().add_aws_resource('glue_trigger', 'main', params)

            # create Lambda function for starting daily Glue trigger
            env_vars = {
                "PROFILE": self.env
            }
            params = super().get_lambda_function_params(env_vars)
            params['source_path'] = "start_glue_triggers"
            lambda_function_name = f"{self.args.name}_start_glue_triggers"
            super().add_aws_resource('lambda_function', lambda_function_name, params)

        
        # create Lambda function for processing files via S3 event notification
        
        # CTAS Lambda for initial DMS full load
        params = super().get_lambda_function_params()
        params['source_path'] = "ctas"
        super().add_aws_resource('lambda_function', "ctas", params)

        # create 4 lambda funcions to handle various file sizes
        memory_sizes = super().get_properties("lambda_memory_size_", True)
        # super().print_json(memory_sizes)
        for memory_size in memory_sizes:
            params = super().get_lambda_function_params()
            params['source_path'] = "cdc"
            params['memory_size'] = memory_size
            super().add_aws_resource('lambda_function', f"cdc_{memory_size}", params)
        
        return source_database_item


    def get_source_database(self, name):
        fqn = self.env + '_' + name
        response = super().get_dynamodb_resource().Table('source_database').query(
            KeyConditionExpression=Key('fqn').eq(fqn)
        )
        return response

