__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.modules import exec_module

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()

        # make sure datalake was created already, if not, create it
        if super().get_item("aws_infra", "fqn", f"{super().get_env()}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        # create Lambda function for processing files via S3 event notification
        # four lambda funcions to handle various file sizes
        memory_sizes = super().get_properties("lambda_memory_size_", True)
        super().print_json(memory_sizes)
        for memory_size in memory_sizes:
            params = super().get_lambda_function_params()
            params['source_path'] = "cdc"
            params['memory_size'] = memory_size
            super().add_aws_resource('lambda_function', f"cdc_{memory_size}", params)
