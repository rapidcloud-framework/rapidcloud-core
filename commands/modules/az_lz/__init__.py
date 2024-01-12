__author__ = "Sridhar K"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "skammadanam@kinect-consulting.com"

import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra
from commands.modules import exec_module

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create_management_group(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        policy_def_ids = metadata["params"]["az_lz_policy_definition_id"]

        params = {
            "parent_id": metadata["params"]["az_lz_parent_id"],
            "policy_name": metadata["params"]["az_lz_policy_name"],
            "policy_definition_id": policy_def_ids
        }
        super().add_azure_resource("az_management_group", self.args.name, params)

    def create_policy_definition(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        
        parameters = ""
        metadata_json = ""
        policy_json = ""
        if metadata["params"]["az_lz_parameters_json"] != "":
            parameters = json.dumps(metadata["params"]["az_lz_parameters_json"],indent=None)
        if metadata["params"]["az_lz_metadata_json"] != "":
            metadata_json = json.dumps(metadata["params"]["az_lz_metadata_json"],indent=None)
        if metadata["params"]["az_lz_policy_json"] != "":
            policy_json = json.dumps(metadata["params"]["az_lz_policy_json"],indent=None)

        parameters_clean = parameters.replace('\\n','').replace('\\"',"\"")[1:-1]
        metadata_clean = metadata_json.replace('\\n','').replace('\\"',"\"")[1:-1]
        policy_clean = policy_json.replace('\\n','').replace('\\"',"\"")[1:-1]

        params = {
            "policy_mode": metadata["params"]["az_lz_policy_mode"],
            "metadata_json": metadata_clean,
            "parameters_json": parameters_clean,
            "policy_json": policy_clean
        }
        print(params)
        super().add_azure_resource("az_policy_definition", self.args.name, params)


    def create_policy_initiate_defintion(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        parameters = ""
        metadata_json = ""

        if metadata["params"]["az_lz_parameters_json"] != "":
            parameters = json.dumps(metadata["params"]["az_lz_parameters_json"],indent=None)
        if metadata["params"]["az_lz_metadata_json"] != "":
            metadata_json = json.dumps(metadata["params"]["az_lz_metadata_json"],indent=None)
        policy_id = metadata["params"]["az_lz_policy_definition_id"]

        parameters_clean = parameters.replace('\\n','').replace('\\"',"\"")[1:-1]
        metadata_clean = metadata_json.replace('\\n','').replace('\\"',"\"")[1:-1]

        params = {
            "parameters_json": parameters_clean,
            "metadata_json": metadata_clean,
            "policy_definition_id": policy_id
        }
        super().add_azure_resource("az_initiative_definition", self.args.name, params)

#####Pending to test
    def create_role_assignment_subscription(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        permissions_actions = metadata["params"]["az_lz_permissions_actions"]
        permissions_no_actions = metadata["params"]["az_lz_permissions_noactions"] 

        data_actions = ""
        data_no_actions = ""

        if metadata["params"].get("az_lz_data_actions") is not None:
            if metadata["params"].get("az_lz_data_actions") != "":
                data_actions = metadata["params"]["az_lz_data_actions"]
        if metadata["params"].get("az_lz_data_noactions") is not None:
            if metadata["params"].get("az_lz_data_noactions") != "":
                data_no_actions = metadata["params"]["az_lz_data_noactions"]


        assignable_scopes = metadata["params"]["az_lz_assignable_scopes"]
        principal = metadata["params"]["az_lz_principal"]

        params = {
            "permissions_actions": permissions_actions,
            "permissions_noactions": permissions_no_actions,
            "data_actions": data_actions,
            "data_noactions": data_no_actions,
            "assignable_scopes": assignable_scopes,
            "principal": principal
            }
        super().add_azure_resource("az_custom_role_subscription", self.args.name, params)

    def create_resource_group(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_lz_location"],
        }
        super().add_azure_resource("az_resource_group", self.args.name, params)

    def create_loganalytics(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_lz_location"],
            "rg_name": metadata["params"]["az_lz_rg_name"],
            "workspace_name": metadata["params"]["az_lz_workspace_name"],
        }
        super().add_azure_resource("az_log_analytics_solution", self.args.name, params)

    def create_key_vault(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "rg_name": metadata["params"]["az_lz_rg_name"],
            "sku_name": metadata["params"]["az_lz_sku_name"],
            "location": metadata["params"]["az_lz_location"]
        }
        super().add_azure_resource("az_key_vault", self.args.name, params)

    def create_key_vault_access_policy(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=f'{self.args.name}-ap')
        az_metadata = Metadata(self.args)
        extra_filters = {}
        env = self.args.env
        kv_name = self.args.name #this has to be refactored
        extra_filters.update({"profile":env})
        extra_filters.update({"command":'create_key_vault'})
        extra_filters.update({"name":f'{kv_name}'})
        kv_value = az_metadata.search_items('metadata',extra_filters)
        kv_rg_name = ''
        if len(kv_value) == 1:
            for kv in list(kv_value):
                kv_rg_name = kv["params"].get("az_lz_rg_name")
                print(kv_rg_name)
                break
        
        params = {
            "rg_name": kv_rg_name,
            "key_permissions_list": metadata["params"]["az_lz_key_permissions_list"],
            "secret_permissions_list": metadata["params"]["az_lz_secret_permissions_list"],
            "key_vault_name": self.args.name,
            "principal": metadata["params"]["az_lz_principal"]
        }
        super().add_azure_resource("az_key_vault_access_policy", f'{self.args.name}-ap', params)

    def ls(self, metadata=None):
        pass


    def create_log_analytics_workspace(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_lz_location"],
            "rg_name": metadata["params"]["az_lz_rg_name"],
            "sku": metadata["params"]["az_lz_sku"],
            "retention_in_days": metadata["params"]["az_lz_retention_in_days"],
        }
        super().add_azure_resource("az_log_analytics_workspace", self.args.name, params)