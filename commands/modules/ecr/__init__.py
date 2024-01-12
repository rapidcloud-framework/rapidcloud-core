__author__ = "Abe Garcia"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "agarciaortiz@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_ecr_params()
        super().add_aws_resource('aws_ecr_repository', self.args.name, params)