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

        # add source database info
        # SourceDatabase(self.args).save_source_database()
        
        # # add transformation 
        # Transformation(self.args).save_transformation()

        # # add target RDS
        # Datawarehouse(self.args).save_datawarehouse() 
