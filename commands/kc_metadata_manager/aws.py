__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

from commands.kc_metadata_manager.aws_metadata import Metadata

class Aws(Metadata):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)


    def create_terraform_bucket(self, bucket, region):
        try:
            self.logger.info("Creating bucket " + bucket + " in " + region)
            response = super().get_s3_client().create_bucket(
                ACL='private',
                Bucket=bucket
            )
        except Exception as e:
            self.logger.warn("Bucket already exists")

        # enable versioning
        super().get_s3_resource().BucketVersioning(bucket).enable()

        # set default KMS encryption
        # TODO
