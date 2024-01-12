__author__ = "iroyzis@kinect-consulting.com"

import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def create_bastion_host(self, metadata=None):

        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        subnet_id = ""
        public_address_id = ""
        copy_paste_enabled = "false"
        file_copy_enabled = "false"
        print("VALUES")
        print(str(metadata["params"]["az_mgmt_copy_paste_enabled"]))
        print("VALUES")
        print(str(metadata["params"]["az_mgmt_file_copy_enabled"]))
        sku = metadata["params"]["az_mgmt_sku_name"]
        if metadata["params"]["az_mgmt_subnet_id"] is not None:
            subnet_id = metadata["params"]["az_mgmt_subnet_id"]
        if metadata["params"]["az_mgmt_public_address_id"] is not None:
            public_address_id = metadata["params"]["az_mgmt_public_address_id"]
        if metadata["params"].get("az_mgmt_copy_paste_enabled") is not None:    
            copy_paste_enabled = "true" if str(metadata["params"]["az_mgmt_copy_paste_enabled"]).lower() in ["yes", "true"] else "false"
        if metadata["params"].get("az_mgmt_file_copy_enabled") is not None and sku == "Standard":
            file_copy_enabled = "true" if str(metadata["params"]["az_mgmt_file_copy_enabled"]).lower() in ["yes", "true"] else "false"

        params = {
                "name": self.args.name,
                "location": metadata["params"]["az_mgmt_location"],
                "resource_group":  metadata["params"]["az_mgmt_resource_group"],
                "sku_name": sku,
                "copy_paste_enabled": copy_paste_enabled,
                "file_copy_enabled": file_copy_enabled,
                "subnet_id": subnet_id,
                "public_address_id": public_address_id
            }
        super().add_azure_resource("az_bastion_host", self.args.name, params)

