__author__ = "jzelada@kinect-consulting.com"

import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create_lb(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        sku = ""
        sku_tier = ""
        if metadata["params"].get("az_lb_sku") is not None:
            sku = metadata["params"]["az_lb_sku"]
        if metadata["params"].get("az_lb_sku_tier") is not None:
            sku_tier = metadata["params"]["az_lb_sku_tier"]

        if sku != "" and sku_tier != "":
            params = {
                "location": metadata["params"]["az_lb_location"],
                "resource_group": metadata["params"]["az_lb_resource_group"],
                "public_address_id": metadata["params"]["az_lb_public_address_id"],
                "sku": sku,
                "sku_tier": sku_tier
            }
        else:
            params = {
                "location": metadata["params"]["az_lb_location"],
                "resource_group": metadata["params"]["az_lb_resource_group"],
                "public_address_id": metadata["params"]["az_lb_public_address_id"],
            }

        super().add_azure_resource("az_lb", self.args.name, params)


    def create_lb_rule(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        lb_name = metadata["params"]["az_lb_load_balancer"].split("/")[8]
        lb_rg = metadata["params"]["az_lb_load_balancer"].split("/")[4]
        params = {
                "load_balancer": lb_name,
                "resource_group": lb_rg,
                "protocol": metadata["params"]["az_lb_protocol"],
                "frontend_port": metadata["params"]["az_lb_frontend_port"],
                "backend_port": metadata["params"]["az_lb_backend_port"],
            }
        super().add_azure_resource("az_lb_rule", self.args.name, params)