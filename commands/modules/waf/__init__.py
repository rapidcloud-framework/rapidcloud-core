__author__ = "jomartinez"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        #self.boto3_session = super().get_boto3_session()


    def create(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_waf_params()
        super().add_aws_resource("aws_waf", self.args.name, params)