__author__ = "Abe Garcia"
__license__ = "MIT"
__email__ = "agarciaortiz"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
         # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_fsx_params()
        super().add_aws_resource("aws_fsx_windows_file_system", self.args.name, params)