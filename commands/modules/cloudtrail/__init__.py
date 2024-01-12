__author__ = "roperez@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata
import traceback

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        self.boto3_session = super().get_boto3_session()

        # use boto3 clients or resources as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")



    def create_trail(self, metadata=None):
        super().delete_infra_metadata(name=metadata["params"]["trail_name"])

        params = {
            "trail_name": self.args.cloudtrail_trail_name,
            "s3_bucket_name": self.args.cloudtrail_s3_bucket_name,
            "kms_key_id": self.args.cloudtrail_kms_key_id,
            "include_global_service_events": "true" if self.args.cloudtrail_include_global_service_events.lower() in ["yes", "true"] else "false",
            "enable_log_file_validation": "true" if self.args.cloudtrail_enable_log_file_validation.lower() in ["yes", "true"] else "false",
            "is_organization_trail": "true" if self.args.cloudtrail_is_organization_trail.lower() in ["yes", "true"] else "false" ,
            "is_multi_region_trail": "true" if self.args.cloudtrail_is_multi_region_trail.lower() in ["yes", "true"] else "false"
        }

        super().add_infra_resource("aws_cloudtrail", metadata["params"]["trail_name"], params)
