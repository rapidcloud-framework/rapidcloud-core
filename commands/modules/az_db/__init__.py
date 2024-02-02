__author__ = "jzelada"
__license__ = "MIT"

import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra
from commands.modules import exec_module

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create_sql_server(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        administrator_login = ""
        administrator_login_password = ""
        ad_admin = ""
        object_id = ""
        user_identity = ""
        tde_key = ""
        enabled_create = "false"
        start_ip_address = ""
        end_ip_address = ""

        if metadata["params"].get("az_db_start_ip_address") is not None:
            start_ip_address = metadata["params"]["az_db_start_ip_address"]
        if metadata["params"].get("az_db_end_ip_address") is not None:
            end_ip_address = metadata["params"]["az_db_end_ip_address"]
        if metadata["params"].get("az_db_administrator_login") is not None:
            administrator_login = metadata["params"]["az_db_administrator_login"]
        if metadata["params"].get("az_db_administrator_login_password") is not None:
            administrator_login_password = metadata["params"]["az_db_administrator_login_password"]
        if metadata["params"].get("az_db_ad_admin") is not None:
            ad_admin = metadata["params"]["az_db_ad_admin"]
        if metadata["params"].get("az_db_object_id") is not None:
            object_id = metadata["params"]["az_db_object_id"]
        if metadata["params"].get("az_db_user_identity") is not None:
            user_identity = metadata["params"]["az_db_user_identity"]
        if metadata["params"].get("az_db_tde_key") is not None:
            tde_key = metadata["params"]["az_db_tde_key"]
        if metadata["params"].get("az_db_tde_enabled_create") is not None:
            enabled_create = "true" if metadata["params"]["az_db_tde_enabled_create"].lower() in ["yes", "true"] else "false"

        params = {
            "location": metadata["params"]["az_db_location"],
            "resource_group": metadata["params"]["az_db_resource_group"],
            "dns_alias": metadata["params"]["az_db_dns_alias"],
            "subnet_id": metadata["params"]["az_db_subnet_id"],
            "start_ip_address": start_ip_address,
            "end_ip_address": end_ip_address,
            "administrator_login": administrator_login,
            "administrator_login_password": administrator_login_password,
            "ad_admin": ad_admin,
            "object_id": object_id,
            "user_identity": user_identity.replace("resourcegroups","resourceGroups"),
            "tde_key": tde_key,
            "tde_enabled_create": enabled_create
        }

        super().add_azure_resource("az_mssql_server", self.args.name, params)



    def create_sql_db(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        start_ip_address = ""
        end_ip_address = ""

        if metadata["params"].get("az_db_start_ip_address") is not None:
            start_ip_address = metadata["params"]["az_db_start_ip_address"]
        if metadata["params"].get("az_db_end_ip_address") is not None:
            end_ip_address = metadata["params"]["az_db_end_ip_address"]
        
        params = {
                "server_id": metadata["params"]["az_db_server_id"],
                "max_size_gb": metadata["params"]["az_db_max_size_gb"],
                "start_ip_address": start_ip_address,
                "end_ip_address": end_ip_address
            }
        super().add_azure_resource("az_sql_db", self.args.name, params)

    def create_cosmosdb_nosql(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        total_throughput_limit = -1
        enable_free_tier ="false"
        geo_location = ""
        enable_multiple_write_locations= "false"
        subnet_id = ""
        enable_serverless = "false"
        key_vault_key_id = ""
        backup_type = ""
        storage_redundancy = ""
        interval_in_minutes = 60
        retention_in_hours = 8
        allow_ips = ""
        identity_type= ""
        identity_ids = ""
        database_name = ""

        containers = []
        if metadata["params"]["az_db_containers"]:
            containers = metadata["params"]["az_db_containers"]


        if metadata["params"].get("az_db_total_throughput_limit") is not None:
            total_throughput_limit = metadata["params"]["az_db_total_throughput_limit"]
        if metadata["params"].get("az_db_enable_free_tier") is not None:
            enable_free_tier = metadata["params"]["az_db_enable_free_tier"]
        if metadata["params"].get("az_db_geo_location") is not None:
            geo_location = metadata["params"]["az_db_geo_location"]
        if metadata["params"].get("az_db_enable_multiple_write_locations") is not None:
            enable_multiple_write_locations = metadata["params"]["az_db_enable_multiple_write_locations"]
        if metadata["params"].get("az_db_subnet_id") is not None:
            subnet_id = metadata["params"]["az_db_subnet_id"]
        if metadata["params"].get("az_db_enable_serverless") is not None:
            enable_serverless = "true" if str(metadata["params"]["az_db_enable_serverless"]) in ["yes", "true"] else "false"
        if metadata["params"].get("az_db_key_vault_key_id") is not None:
            key_vault_key_id = metadata["params"]["az_db_key_vault_key_id"]
        if metadata["params"].get("az_db_backup_type") is not None:
            backup_type = metadata["params"]["az_db_backup_type"]
        if metadata["params"].get("az_db_storage_redundancy") is not None:
            storage_redundancy = metadata["params"]["az_db_storage_redundancy"]
        if metadata["params"].get("az_db_interval_in_minutes") is not None and metadata["params"].get("az_db_interval_in_minutes") != "":
            interval_in_minutes = metadata["params"]["az_db_interval_in_minutes"]
        if metadata["params"].get("az_db_retention_in_hours") is not None and metadata["params"].get("az_db_retention_in_hours") != "":
            retention_in_hours = metadata["params"]["az_db_retention_in_hours"]
        if metadata["params"].get("az_db_ip_range_filter") is not None:
            allow_ips = metadata["params"]["az_db_ip_range_filter"]
        if metadata["params"].get("az_db_identity_type") is not None:
            identity_type = metadata["params"]["az_db_identity_type"]
        if metadata["params"].get("az_db_identity_ids") is not None:
            identity_ids = metadata["params"]["az_db_identity_ids"]
        if metadata["params"].get("az_db_database_name") is not None:
            database_name = metadata["params"]["az_db_database_name"]
        
        if backup_type == "Continuous":
            enable_multiple_write_locations = "false"

        #Adding location to geolocation by default as requested
        if geo_location == "":
            geo_location = metadata["params"]["az_db_location"]
        
        if len(containers) == 0:
             
            params = {
                    "location": metadata["params"]["az_db_location"],
                    "resource_group": metadata["params"]["az_db_resource_group"],
                    "total_throughput_limit": total_throughput_limit,
                    "geo_location": geo_location,
                    "enable_multiple_write_locations": enable_multiple_write_locations,
                    "subnet_id": subnet_id,
                    "enable_free_tier": enable_free_tier,
                    "enable_serverless": enable_serverless,
                    "key_vault_key_id": key_vault_key_id,
                    "backup_type": backup_type,
                    "storage_redundancy": storage_redundancy,
                    "interval_in_minutes": interval_in_minutes,
                    "retention_in_hours": retention_in_hours,
                    "ip_range_filter": allow_ips,
                    "identity_type": identity_type,
                    "identity_ids": identity_ids.replace("resourcegroups","resourceGroups"),
                    "database_name" : database_name
                }
        else:
            params = {
                    "location": metadata["params"]["az_db_location"],
                    "resource_group": metadata["params"]["az_db_resource_group"],
                    "total_throughput_limit": total_throughput_limit,
                    "geo_location": geo_location,
                    "enable_multiple_write_locations": enable_multiple_write_locations,
                    "subnet_id": subnet_id,
                    "enable_free_tier": enable_free_tier,
                    "enable_serverless": enable_serverless,
                    "key_vault_key_id": key_vault_key_id,
                    "backup_type": backup_type,
                    "storage_redundancy": storage_redundancy,
                    "interval_in_minutes": interval_in_minutes,
                    "retention_in_hours": retention_in_hours,
                    "ip_range_filter": allow_ips,
                    "identity_type": identity_type,
                    "identity_ids": identity_ids.replace("resourcegroups","resourceGroups"),
                    "database_name" : database_name,
                    "containers": json.dumps(containers)
                }
        super().add_azure_resource("az_cosmosdb_nosql", self.args.name, params)