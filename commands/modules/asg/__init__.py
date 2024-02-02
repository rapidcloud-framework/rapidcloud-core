__author__ = "Abe Garcia"
__license__ = "MIT"
__email__ = "agarciaortiz"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)


    def create(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_asg_params()
        self.add_aws_resource("aws_autoscaling_group", self.args.name, params)