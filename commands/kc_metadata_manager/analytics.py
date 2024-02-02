__author__ = "Igor Royzis"
__license__ = "MIT"


from datetime import datetime
import logging

from commands.kc_metadata_manager.aws_metadata import Metadata

class Analytics(Metadata):

    TABLE_NAME = 'analytics'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_analytics(self):
        item={
            'fqn': super().get_env() + '_' + super().get_args().name, 
            'profile': super().get_env(),
            'name': super().get_args().name,
            'runtime': super().get_args().runtime,
            'timestamp': str(datetime.now())
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata")

        super().add_aws_resource('kinesis_stream', 'main', {})

        job_name = f"streaming_{super().get_args().name}"
        if super().get_args().runtime == 'emr':
            # emr cluster
            params = super().get_emr_cluster_params()
            super().add_aws_resource("emr_cluster", "main", params)

            # s3 bucket for spark job code
            super().add_aws_resource("s3_bucket", "jobs", {})

            # spark streaming job template for analytics service - store in S3
            template = "modules/kc_streaming_emr_spark_job_template"
            new_job = f"src/emr/{job_name}"
            super().create_from_template(template, new_job)

            params = super().get_s3_object_params(f"{super().get_env()}-jobs".replace('_','-'), f"emr/{job_name}.py", f"{new_job}/main.py")
            super().add_aws_resource('s3_bucket_object', job_name, params)

        elif super().get_args().runtime == 'glue':
            # spark streaming glue job for analytics service
            params = super().get_glue_job_params(job_name, "gluestreaming")
            super().add_aws_resource('glue_job', job_name, params)

            template = "modules/kc_streaming_glue_job_template"
            new_job = f"src/glue/{job_name}"
            super().create_from_template(template, new_job)
        

