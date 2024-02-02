__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.publishing import Publishing
from commands.modules import exec_module
from data_scripts.kc_publish_redshift_ddl import RedshiftDDL

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()

        # make sure datalake was created already, if not, create it
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        item={
            'fqn': f"{super().get_env()}_{self.args.name}".replace('-','').replace('_',''),
            'name': self.args.name, 
            'profile': super().get_env(), 
            'type': "redshift", 
            'timestamp': str(datetime.datetime.now()),
        }
        super().put_item("datawarehouse", item)

        super().save_password(super().get_env(), 'redshift_cluster', self.args.name, '')
        params = super().get_redshift_params()
        super().add_aws_resource('redshift_cluster', self.args.name, params)


    def add_table(self, metadata=None):
        env = super().get_env()
        name = self.args.name
        db_name = self.args.redshift_db_name
        pk = self.args.redshift_primary_key
        sk = self.args.redshift_sort_key if self.args.redshift_sort_key else None
        dist_key = self.args.redshift_dist_key if self.args.redshift_dist_key else None
        dist_style = self.args.redshift_dist_style if self.args.redshift_dist_style else None
        target_db = f"{env}_{db_name}".replace('-','').replace('_','')
        connection_string = f"{env}/redshift_cluster/main/connection_string"

        fqn = f"{target_db}_{name}"
        item={
            'fqn': fqn, 
            'profile': env,
            'name': name,
            'dw': target_db,
            'connection_string': connection_string,
            'db_type': "redshift",
            'db_name': db_name,
            'schema': None,
            'primary_key': pk,
            'sort_key': sk,
            'enabled': False,
            'analysis_catalog': f"{env}_analysisdb",
            'analysis_bucket': f"{env}_analysis".replace('_','-'),
            'iam_role': 'tbd',
            'dist_key': dist_key,
            'dist_style': dist_style,       
            'timestamp': str(datetime.datetime.now()),
        }
        super().put_item("publishing", item)

        job_name = f"publish_redshift_{db_name}_{name}"
        db_connection = f"{super().get_env()}_{db_name}_redshift_cluster"
        params = super().get_glue_job_params(job_name, "pythonshell", dataset=name, db_connection=db_connection)
        super().add_aws_resource('glue_job', job_name, params)


    def generate_schema(self, metadata=None):
        # Generate schemas
        # do this after analysisdb has been crawled
        publishing = Publishing(super().get_args()).get_all_publishing()
        if len(publishing) > 0:
            step += 1
            if super().prompt(step, "Generate Redshift schemas (if applicable)") == 'yes':
                RedshiftDDL().main(super().get_args())
