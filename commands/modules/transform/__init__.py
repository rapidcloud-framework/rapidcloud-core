__author__ = "Igor Royzis"
__license__ = "MIT"


from datetime import datetime
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.target_database import TargetDatabase
from commands.modules import exec_module


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        # make sure datalake was created already, if not, create it
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        base_datasets = self.args.base_datasets.split(',') if self.args.base_datasets else []
        item={
            'fqn': f"{super().get_env()}_{self.args.transform_name}", 
            'profile': super().get_env(),
            'name': self.args.transform_name,
            'datalake': self.args.datalake,
            'enabled': 'False',
            'job_type': self.args.transform_job_type,
            'raw_catalog': f"{super().get_env()}_rawdb",
            'raw_bucket': f"{super().get_env()}_raw".replace('_','-'),
            'analysis_catalog': f"{super().get_env()}_analysisdb",
            'analysis_bucket': f"{super().get_env()}_analysis".replace('_','-'),
            'base_datasets': base_datasets,
            'create_quicksight_dataset': True if self.args.create_quicksight_dataset else False,
            'refresh_spice': True if self.args.transform_refresh_spice else False,
            'timestamp': str(datetime.now()),
        }
        super().put_item('transformation', item)

        # only need one main job and on-demand trigger
        job_name = 'transform_main'
        params = super().get_glue_job_params(job_name, self.args.job_type)
        super().add_aws_resource('glue_job', job_name, params)

        trigger_params = super().get_glue_trigger_params("ON_DEMAND", job_name)
        super().add_aws_resource('glue_trigger', job_name, trigger_params)

        # transformation job
        job_name = 'transform_' + self.args.name
        dbs = TargetDatabase(super().get_args()).get_all_target_databases()
        db_conn = None
        if dbs:
            db_conn = f"{super().get_env()}_{dbs[0]['name']}_{dbs[0]['resource_type']}" 
        params = super().get_glue_job_params(job_name, self.args.job_type, dataset=self.args.name, base_datasets=base_datasets, db_connection=db_conn)
        super().add_aws_resource('glue_job', job_name, params)

        # transformation trigger
        trigger_params = super().get_glue_trigger_params("CONDITIONAL", job_name, 'transform_main')
        super().add_aws_resource('glue_trigger', job_name, trigger_params)

        # get all transformations for crawler paths
        # transformations = self.get_all_transformations()

        # Glue crawler for transformations (analysisdb) 
        params = super().get_glue_crawler_params("analysis", "transformations", [])
        super().add_aws_resource('glue_crawler', 'transformations', params)

        # sns_topic
        super().add_aws_resource('sns_topic', 'transformations', params)