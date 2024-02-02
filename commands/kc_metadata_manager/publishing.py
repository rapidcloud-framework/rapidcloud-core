__author__ = "Igor Royzis"
__license__ = "MIT"


from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.target_database import TargetDatabase

class Publishing(Metadata):

    TABLE_NAME = 'publishing'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_publishing(self):
        env = super().get_env()
        db_type = super().get_args().type # redshift, rds, aurora
        db_name = super().get_args().name if super().get_args().name else db_type
        db_schema = super().get_args().schema
        db_engine = super().get_args().engine if super().get_args().engine else db_type
        name = super().get_args().table_name
        pk = super().get_args().primary_key if super().get_args().primary_key else 'n/a'
        sk = super().get_args().sort_keys if super().get_args().sort_keys else 'n/a'

        if db_type in ['redshift','snowflake']:
            target_db = f"{env}_{db_type}".replace('-','').replace('_','')
            connection_string = f"{env}/{db_type}_cluster/main/connection_string"
        else:
            target_db = f"{env}_{db_type}_{db_engine}_{db_name}"
            connection_string = f"{env}/{db_type}_{db_engine}_instance/{db_name}/connection_string"

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
            'sort_key': sk,
            'schema': db_schema,
            'enabled': 'False',
            'analysis_catalog': f"{env}_analysisdb",
            'analysis_bucket': f"{env}_analysis".replace('_','-'),
            'iam_role': 'tbd',
            'dist_key': 'tbd',              
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata", name)

        job_name = f"publish_{db_type}_{db_engine}_{name}"
        if db_type == 'redshift':
            db_connection = f"{super().get_env()}_main_redshift_cluster"
        else:
            db_fqn = f"{super().get_env()}_{db_type}_{db_engine}_{db_name}"
            db = TargetDatabase(super().get_args()).get_target_database(db_fqn)
            if db:
                db_connection = f"{super().get_env()}_{db_name}_{db['resource_type']}"

        params = super().get_glue_job_params(job_name, "pythonshell", dataset=name, db_connection=db_connection)
        super().add_aws_resource('glue_job', job_name, params)
        if db_type.lower() in ['rds', 'aurora']:
            template = f"data_scripts/job_templates/kc_publishing_job_{db_engine}_template.py"
            new_path = f"src/glue/publish/{super().get_env()}"
            new_file = f"{job_name}.py"
            super().create_from_template_file(template, new_path, new_file)
            local_script = f"{new_path}/{new_file}"
            AwsInfra(self.args).upload_glue_code(job_name, local_script)

        if super().get_args().auto_trigger.lower() in ['true', 'yes']:
            trigger_name = f"transform_{db_type}_{db_engine}_{name}"
            trigger_params = super().get_glue_trigger_params("CONDITIONAL", job_name, trigger_name)
            super().add_aws_resource('glue_trigger', job_name, trigger_params)


    def get_all_publishing(self):
        return super().get_dynamodb_resource().Table(self.TABLE_NAME).scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )['Items']
