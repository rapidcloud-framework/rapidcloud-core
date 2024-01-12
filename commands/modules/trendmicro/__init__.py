__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.modules.trendmicro.trend_application_worker import TrendApplicationSecurityWorker
from commands.modules.trendmicro.trend_filestorage_worker import TrendFilestorageSecurityWorker
from commands.modules.trendmicro.trend_workload_worker import TrendWorkloadSecurityWorker

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.env = self.env
        self.boto_session = self.get_boto3_session()


    def setup(self, metadata=None):
        api_key = self.args.trendmicro_api_key
        region = self.args.trendmicro_conformity_region

        super().delete_infra_metadata(name=region)

        if api_key != "trendmicro/api_key":            
            super().save_secret(self.env, 'trendmicro', 'api_key', api_key, use_env_prefix=False)
        
        super().add_infra_resource("conformity_provider", region, {"region": region, "api_key": api_key})

    
    def filestorage_create_stack(self, metadata=None):
        TrendFilestorageSecurityWorker(self).filestorage_create_stack(metadata)


    def filestorage_list_stacks(self, metadata=None, quiet=False):
        return TrendFilestorageSecurityWorker(self).filestorage_list_stacks()


    def filestorage_delete_stack(self, metadata=None):
        TrendFilestorageSecurityWorker(self).filestorage_delete_stack()
        

    def application_create_group(self, metadata=None):
        TrendApplicationSecurityWorker(self).application_create_group()


    def workload_create_group(self, metadata=None):
        TrendWorkloadSecurityWorker(self).workload_create_group()


    def workload_generate_deployment_script(self, metadata=None):
        TrendWorkloadSecurityWorker(self).workload_generate_deployment_script()


    def workload_group_sync(self, metadata=None):
        TrendWorkloadSecurityWorker(self).workload_group_sync()

    def workload_list_policies(self, metadata=None):
        return TrendWorkloadSecurityWorker(self).workload_list_policies()


    def conformity_enable(self, metadata=None):
        super().delete_infra_metadata(name=metadata["params"]["account_name"])
        
        params = {
            "account_name": self.args.trendmicro_account_name,
            "conformity_environment": self.args.trendmicro_conformity_environment,
            "conformity_tags": [] if not self.args.trendmicro_conformity_tags else self.args.trendmicro_conformity_tags.replace(" ","").split(",")
        }
        super().add_infra_resource("conformity", metadata["params"]["account_name"], params)

    def conformity_create_group(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)

        params = {
            "conformity_tags": [] if not self.args.trendmicro_conformity_tags else self.args.trendmicro_conformity_tags.replace(" ","").split(",")
        }

        super().add_infra_resource("conformity_group", self.args.name, params)