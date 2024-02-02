__author__ = "Igor Royzis"
__license__ = "MIT"


from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    #TODO Change create to a meaningfull command
    def create(self, metadata=None):
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_cloudfront_params()
        super().add_aws_resource('aws_cloudfront_distribution', self.args.name, params)