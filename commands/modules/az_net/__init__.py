__author__ = "Igor Royzis"
__license__ = "MIT"



import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra
from commands.modules import exec_module


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def create_nsg(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        security_rules = []
        if metadata["params"]["az_net_security_rule"]:
            security_rules = metadata["params"]["az_net_security_rule"]

        if len(security_rules) == 0:
            params = {
                "name": self.args.name,
                "location": metadata["params"]["az_net_location"],
                "resource_group":  metadata["params"]["az_net_resource_group"]
            }
        else:
            params = {
                "name": self.args.name,
                "location": metadata["params"]["az_net_location"],
                "resource_group":  metadata["params"]["az_net_resource_group"],
                "security_rule": json.dumps(security_rules)
            }
        super().add_azure_resource("az_nsg", self.args.name, params)

    def create_vnet(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        dns_servers = []
        if metadata["params"]["az_net_dns_servers"] is not None:
            dns_servers = metadata["params"]["az_net_dns_servers"]

        if dns_servers:
            params = {
                "location": metadata["params"]["az_net_location"],
                "resource_group": metadata["params"]["az_net_resource_group"],
                "address_space": metadata["params"]["az_net_address_space"],
                "dns_servers": dns_servers
            }
        else:
            params = {
                "location": metadata["params"]["az_net_location"],
                "resource_group": metadata["params"]["az_net_resource_group"],
                "address_space": metadata["params"]["az_net_address_space"]
            }
        super().add_azure_resource("az_vnet", self.args.name, params)

    def create_firewall(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        subnet_id = ""
        public_address_id = ""
        if metadata["params"]["az_net_subnet_id"] is not None:
            subnet_id = metadata["params"]["az_net_subnet_id"]
        if metadata["params"]["az_net_public_address_id"] is not None:
            public_address_id = metadata["params"]["az_net_public_address_id"]

        if subnet_id != "" and public_address_id != "":
            params = {
                "location": metadata["params"]["az_net_location"],
                "resource_group": metadata["params"]["az_net_resource_group"],
                "subnet_id": subnet_id,
                "public_address_id": public_address_id,
                "sku_name": metadata["params"]["az_net_sku_name"],
                "sku_tier": metadata["params"]["az_net_sku_tier"]
            }
        else:
            params = {
                "location": metadata["params"]["az_net_location"],
                "resource_group": metadata["params"]["az_net_resource_group"],
                "sku_name": metadata["params"]["az_net_sku_name"],
                "sku_tier": metadata["params"]["az_net_sku_tier"]
            }

        super().add_azure_resource("az_firewall", self.args.name, params)

    def create_public_ip(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_net_location"],
            "resource_group_name": metadata["params"]["az_net_resource_group_name"],
            "sku_name": metadata["params"]["az_net_sku_name"]
        }
        super().add_azure_resource("az_public_ip", self.args.name, params)

    def create_ddos_plan(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_net_location"],
            "resource_group": metadata["params"]["az_net_resource_group"],
        }
        super().add_azure_resource("az_ddos_plan", self.args.name, params)

    def create_dns_zone(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "domain_name": metadata["params"]["az_net_domain_name"],
            "resource_group": metadata["params"]["az_net_resource_group"],
        }
        super().add_azure_resource("az_dns_zone", self.args.name, params)

    def create_private_dns_zone(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "domain_name": metadata["params"]["az_net_domain_name"],
            "resource_group": metadata["params"]["az_net_resource_group"],
        }
        super().add_azure_resource("az_private_dns", self.args.name, params)

    def create_route_table(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_net_location"],
            "resource_group": metadata["params"]["az_net_resource_group"],
        }
        super().add_azure_resource("az_route_table", self.args.name, params)

    def create_route(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "name": self.args.name,
            "resource_group": metadata["params"]["az_net_resource_group"],
            "route_table_name": metadata["params"]["az_net_route_table_name"],
            "address_prefix": metadata["params"]["az_net_address_prefix"],
            "next_hop_type": metadata["params"]["az_net_next_hop_type"]
        }
        super().add_azure_resource("az_route", self.args.name, params)

    def create_subnet(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        service_endpoints = ""
        if metadata["params"].get("az_net_service_endpoints") is not None:
            service_endpoints = metadata["params"]["az_net_service_endpoints"]
        params = {
            "resource_group": metadata["params"]["az_net_resource_group"],
            "address_prefix": metadata["params"]["az_net_address_prefix"],
            "vnet_name": metadata["params"]["az_net_vnet_name"],
            "service_endpoints": service_endpoints
        }
        super().add_azure_resource("az_subnet", self.args.name, params)

    def create_network_watcher(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        params = {
            "location": metadata["params"]["az_net_location"],
            "resource_group": metadata["params"]["az_net_resource_group"],
        }
        super().add_azure_resource("az_network_watcher", self.args.name, params)

    def create_vnet_peering(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        allow_fwd = "true" if str(metadata["params"]["az_net_allow_forwarded_traffic"]) in ["yes", "true"] else "false"
        allow_vnet_access = "true" if str(metadata["params"]["az_net_allow_virtual_network_access"]) in ["yes", "true"] else "false"
        params = {
            "resource_group": metadata["params"]["az_net_resource_group"],
            "virtual_network_name": metadata["params"]["az_net_virtual_network_name"],
            "remote_virtual_network_id": metadata["params"]["az_net_remote_virtual_network_id"],
            "allow_forwarded_traffic": allow_fwd,
            "allow_virtual_network_access": allow_vnet_access
        }
        super().add_azure_resource("az_vnet_peering", self.args.name, params)

    def create_net_flow_log(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)

        enable = "true" if str(metadata["params"]["az_net_enabled"]) in ["yes", "true"] else "false"
        params = {
            "resource_group": metadata["params"]["az_net_resource_group"],
            "location": metadata["params"]["az_net_location"],
            "network_watcher_name": metadata["params"]["az_net_network_watcher_name"],
            "network_security_group_id": metadata["params"]["az_net_network_security_group_id"],
            "storage_account_id": metadata["params"]["az_net_storage_account_id"],
            "enabled": enable,
            "retention_days": metadata["params"]["az_net_retention_days"],
            "workspace_id": metadata["params"]["az_net_workspace_id"],
        }
        super().add_azure_resource("az_net_flow_log", self.args.name, params)
