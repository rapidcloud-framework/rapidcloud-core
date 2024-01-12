
import logging

from commands.kc_metadata_manager.activation import AwsActivator, AzureActivator, CloudActivator, GcpActivator
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.aws_metadata import Metadata as AwsMetadata
from commands.kc_metadata_manager.azure_infra import AzureInfra
from commands.kc_metadata_manager.azure_metadata import Metadata as AzureMetadata
from commands.kc_metadata_manager.gcp_infra import GcpInfra
from commands.kc_metadata_manager.gcp_metadata import Metadata as GcpMetadata
from commands.kc_metadata_manager.cloud_metadata import CloudMetadata

class Provider(object):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args

    def get_activator(self) -> CloudActivator:
        # print("cloud", args.cloud)
        if self.args.cloud == "aws":
            return AwsActivator(self.args)
        elif self.args.cloud == "azure":
            return AzureActivator(self.args)
        elif self.args.cloud == "gcp":
            return GcpActivator(self.args)
        else:
            raise RuntimeError(f"Unexpected cloud provider: '{self.args.cloud}'")

    def get_metadata_manager(self) -> CloudMetadata:
        if self.args.cloud == "aws":
            return AwsMetadata(self.args)
        elif self.args.cloud == "azure":
            return AzureMetadata(self.args)
        elif self.args.cloud == "gcp":
            return GcpMetadata(self.args)
        else:
            raise RuntimeError(f"Unexpected cloud provider: '{self.args.cloud}'")

    def get_infra(self) -> CloudMetadata:
        if self.args.cloud == "aws":
            return AwsInfra(self.args)
        elif self.args.cloud == "azure":
            return AzureInfra(self.args)
        elif self.args.cloud == "gcp":
            return GcpInfra(self.args)
        else:
            raise RuntimeError(f"Unexpected cloud provider: '{self.args.cloud}'")