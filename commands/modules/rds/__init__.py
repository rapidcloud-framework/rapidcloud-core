__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import json
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.target_database import TargetDatabase
from commands.modules import exec_module
from data_scripts.kc_publish_rds_ddl import RdsSqlDDL


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def get_resource_type(self, dbtype, engine):
        resource_type = None
        if dbtype == 'rds':
            if engine == 'mysql':
                resource_type = 'rds_mysql_instance'
            elif engine == 'postgres':
                resource_type = 'rds_postgresql_instance'                
        elif dbtype == 'aurora':
            if engine == 'mysql':
                resource_type = 'aurora_mysql_instance'
            elif engine == 'postgres':
                resource_type = 'aurora_postgresql_instance'
        return resource_type


    def create(self, metadata=None):
        # delete existing aws_infra items for this module - start clean
        AwsInfra(self.args).delete_aws_infra()

        # make sure datalake was created already, if not, create it
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        name = self.args.rds_name
        dbtype = self.args.rds_type
        engine = self.args.rds_engine
        multi_az = self.args.rds_multi_az in ('true', 'yes')
        database_name = self.args.rds_database_name
        resource_type = self.get_resource_type(dbtype, engine)

        params = super().get_db_params(dbtype, engine, resource_type, multi_az, name, database_name)
        item={
            'fqn': f"{self.env}_{dbtype}_{engine}_{name}", 
            'profile': self.env, 
            'name': name, 
            'type': dbtype,
            'engine': engine,
            'resource_type': resource_type,
            'multi_az': multi_az,
            'database_name': database_name,
            'timestamp': str(datetime.now())
        }
        super().put_item("target_database", item)

        super().save_password(super().get_env(), resource_type, self.args.rds_name)
        super().add_aws_resource(resource_type, name, params)

        # sns_topics (may or may not be used for specific use case)
        super().add_aws_resource('sns_topic', 'transformations', params)
        super().add_aws_resource('sns_topic', 'publishing', params)

        # lambda function (may or may not be used for specific use case)
        env_vars = {"PROFILE": self.env}
        params = super().get_lambda_function_params(env_vars)
        params['source_path'] = "default_lambda_template"
        params['immutable'] = True
        super().add_aws_resource("lambda_function", "run_publishing", params)

        # sns_topic_subscription
        params = super().get_sns_topic_subscription_params("transformations", "run_publishing")
        super().add_aws_resource('sns_topic_subscription', 'transformations', params)


    def add_table(self, metadata=None):
        env = super().get_env()
        name = self.args.name
        db_name = self.args.rds_db_name
        pk = self.args.rds_primary_key if self.args.rds_primary_key else None
        
        db = super().get_metadata_item("rds", "create", db_name)
        self.logger.info(json.dumps(db, indent=2))

        db_type = db['params']['rds_type']
        db_engine = db['params']['rds_engine']
        db_schema = db['params']['rds_database_name']
        target_db = f"{env}_{db_type}_{db_engine}_{db_name}"
        connection_string = f"{env}/{db_type}_{db_engine}_instance/{db_name}/connection_string"
        resource_type = self.get_resource_type(db_type, db_engine)

        fqn = f"{target_db}_{name}"
        item={
            'fqn': fqn, 
            'profile': env,
            'name': name,
            'dw': target_db,
            'connection_string': connection_string,
            'db_type': db_type,
            'db_engine': db_engine,
            'db_name': db_name,
            'primary_key': pk,
            'sort_key': None,
            'schema': db_schema,
            'enabled': 'False',
            'analysis_catalog': f"{env}_analysisdb",
            'analysis_bucket': f"{env}_analysis".replace('_','-'),
            'iam_role': 'tbd',
            'dist_key': 'tbd',              
            'timestamp': str(datetime.now()),
        }
        super().put_item("publishing", item)

        # Publishing Glue job infra
        job_name = f"publish_{db_type}_{db_engine}_{name}"
        db_connection = f"{super().get_env()}_{db_name}_{resource_type}"
        params = super().get_glue_job_params(job_name, "pythonshell", dataset=name, db_connection=db_connection)
        super().add_aws_resource('glue_job', job_name, params)

        # Publishing Glue Job Code Template
        template = f"data_scripts/job_templates/kc_publishing_job_{db_engine}_template.py"
        new_path = f"src/glue/publish/{super().get_env()}"
        new_file = f"{job_name}.py"
        super().create_from_template_file(template, new_path, new_file)
        local_script = f"{new_path}/{new_file}"
        AwsInfra(self.args).upload_glue_code(job_name, local_script)

        # if self.args.auto_trigger.lower() in ['true', 'yes']:
        #     trigger_name = f"transform_{db_type}_{db_engine}_{name}"
        #     trigger_params = super().get_glue_trigger_params("CONDITIONAL", job_name, trigger_name)
        #     super().add_aws_resource('glue_trigger', job_name, trigger_params)


    def generate_schema(self, metadata=None):
        # Generate schemas
        # do this after analysisdb has been crawled
        target_dbs = TargetDatabase(super().get_args()).get_all_target_databases()
        if len(target_dbs) > 0:
            step += 1
            if super().prompt(step, "Generate Target database schemas (if applicable)") == 'yes':                
                RdsSqlDDL().main(super().get_args())
