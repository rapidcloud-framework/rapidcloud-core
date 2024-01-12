__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.target_database import TargetDatabase

class Transformation(Metadata):

    TABLE_NAME = 'transformation'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_transformation(self):
        base_datasets = []
        if super().get_args().base_datasets is not None:
            for dataset in super().get_args().base_datasets.split(','):
                # base_datasets.append(super().get_env() + '_' + dataset) 
                base_datasets.append(dataset) 

        item={
            'fqn': f"{super().get_env()}_{super().get_args().name}", 
            'profile': super().get_env(),
            'name': super().get_args().name,
            'datalake': super().get_args().datalake,
            'enabled': 'False',
            'job_type': super().get_args().job_type,
            'raw_catalog': f"{super().get_env()}_rawdb",
            'raw_bucket': f"{super().get_env()}_raw".replace('_','-'),
            'analysis_catalog': f"{super().get_env()}_analysisdb",
            'analysis_bucket': f"{super().get_env()}_analysis".replace('_','-'),
            'base_datasets': base_datasets,
            'create_quicksight_dataset': True if super().get_args().create_quicksight_dataset else False,
            'refresh_spice': True if super().get_args().refresh_spice else False,
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata")

        # only need one main job and on-demand trigger
        job_name = 'transform_main'
        params = super().get_glue_job_params(job_name, super().get_args().job_type)
        super().add_aws_resource('glue_job', job_name, params)

        trigger_params = super().get_glue_trigger_params("ON_DEMAND", job_name)
        super().add_aws_resource('glue_trigger', job_name, trigger_params)

        # transformation job
        job_name = 'transform_' + super().get_args().name
        db_conn = None
        # dbs = TargetDatabase(super().get_args()).get_all_target_databases()
        # if dbs:
        #     db_conn = f"{super().get_env()}_{dbs[0]['name']}_{dbs[0]['resource_type']}" 
        params = super().get_glue_job_params(job_name, super().get_args().job_type, dataset=super().get_args().name, base_datasets=base_datasets, db_connection=db_conn)
        super().add_aws_resource('glue_job', job_name, params)

        # transformation trigger
        trigger_params = super().get_glue_trigger_params("CONDITIONAL", job_name, 'transform_main')
        super().add_aws_resource('glue_trigger', job_name, trigger_params)

        # get all transformations for crawler paths
        transformations = self.get_all_transformations()

        # Glue crawler for transformations (analysisdb) 
        params = super().get_glue_crawler_params("analysis", "transformations", [])
        super().add_aws_resource('glue_crawler', 'transformations', params)

        # sns_topic
        super().add_aws_resource('sns_topic', 'transformations', params)




    def get_all_transformations(self):
        return super().get_dynamodb_resource().Table(self.TABLE_NAME).scan(        
            FilterExpression=Attr('profile').eq(super().get_env()) 
        )['Items']
