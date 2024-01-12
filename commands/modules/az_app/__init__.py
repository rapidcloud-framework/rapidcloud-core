__author__ = "iroyzis@kinect-consulting.com"

import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create_app_env(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        subnet_id = ""
        internal_load_balancing_mode = ""
        allowed_user_ip_cidrs = ""
        pricing_tier = ""

        if metadata["params"]["az_app_subnet_id"] is not None:
            subnet_id = metadata["params"]["az_app_subnet_id"]
        if metadata["params"]["az_app_internal_load_balancing_mode"] is not None:
            internal_load_balancing_mode = metadata["params"]["az_app_internal_load_balancing_mode"]
        if metadata["params"].get("az_app_allowed_user_ip_cidrs") is not None:    
            allowed_user_ip_cidrs = metadata["params"]["az_app_allowed_user_ip_cidrs"]
        if metadata["params"].get("az_app_pricing_tier") is not None: 
            pricing_tier = metadata["params"]["az_app_pricing_tier"]

        params = {
                "name": self.args.name,
                "resource_group":  metadata["params"]["az_app_resource_group"],
                "subnet_id": subnet_id,
                "internal_load_balancing_mode": internal_load_balancing_mode,
                "allowed_user_ip_cidrs": allowed_user_ip_cidrs,
                "pricing_tier" : pricing_tier
            }
        super().add_azure_resource("az_app_env", self.args.name, params)


    def create_service_plan(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        service_env_id = ""

        if metadata["params"]["az_app_app_service_environment_id"] is not None:
            service_env_id = metadata["params"]["az_app_app_service_environment_id"]


        params = {
                "name": self.args.name,
                "resource_group":  metadata["params"]["az_app_resource_group"],
                "location": metadata["params"]["az_app_location"],
                "os_type": metadata["params"]["az_app_os_type"],
                "sku_name": metadata["params"]["az_app_sku_name"],
                "app_service_environment_id" : service_env_id

            }
        super().add_azure_resource("az_service_plan", self.args.name, params)

    def create_web_app(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)


        params = {
                "name": self.args.name,
                "resource_group":  metadata["params"]["az_app_resource_group"],
                "location": metadata["params"]["az_app_location"],
                "service_plan_id": metadata["params"]["az_app_service_plan_id"],

            }
        super().add_azure_resource("az_web_app", self.args.name, params)

    def create_logic_app(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)


        params = {
                "name": self.args.name,
                "resource_group":  metadata["params"]["az_app_resource_group"],
                "location": metadata["params"]["az_app_location"]

            }
        super().add_azure_resource("az_logic_app", self.args.name, params)

    def create_function_app(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        os_type = ""
        version = ""
        storage_access_type = ""
        managed_identity = ""
        public_access = "false"
        https_only = "false"
        subnet_id = ""

        if metadata["params"]["az_app_os_type"] is not None:
            os_type = metadata["params"]["az_app_os_type"]
        if metadata["params"]["az_app_version"] is not None:
            version = metadata["params"]["az_app_version"]
        if metadata["params"]["az_app_storage_access_type"] is not None:
            storage_access_type = metadata["params"]["az_app_storage_access_type"]
        if metadata["params"]["az_app_managed_identity"] is not None:
            managed_identity = metadata["params"]["az_app_managed_identity"]
        if metadata["params"]["az_app_public_access"] is not None:
            public_access = "true" if str(metadata["params"]["az_app_public_access"]).lower() in ["yes", "true"] else "false"
        if metadata["params"]["az_app_https_only"] is not None:
            https_only = "true" if str(metadata["params"]["az_app_https_only"]).lower() in ["yes", "true"] else "false"
        if metadata["params"]["az_app_subnet_id"] is not None:
            subnet_id = metadata["params"]["az_app_subnet_id"]
        
        params = {
                "name": self.args.name,
                "resource_group":  metadata["params"]["az_app_resource_group"],
                "location": metadata["params"]["az_app_location"],
                "service_plan_id": metadata["params"]["az_app_service_plan_id"],
                "storage_account_id": metadata["params"]["az_app_storage_account_id"],
                "storage_access_type": storage_access_type,
                "managed_identity": managed_identity.replace("resourcegroups","resourceGroups"),
                "public_access": public_access,
                "https_only": https_only,
                "subnet_id": subnet_id,
                "os_type": os_type,
                "version": version


            }
        super().add_azure_resource("az_function_app", self.args.name, params)