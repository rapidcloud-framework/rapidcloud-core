__author__ = "skammadanam"

import base64
import ipaddress
import json
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def load_params(self, module, command, args):
        # we will populate this dict and pass it to the command functions
        params = {}
        try:
            # we're pulling all valus from the args object into a dict
            args_dict = vars(args)

            # we then load the actual args from the module's json
            json_args = self.get_module_json("az_storage")[module][command]['args']

            # now we'll loop over them all
            for arg in json_args.keys():
                params[arg] = args_dict[f"{module}_{arg}"]
                if arg == 'tags' or arg == 'labels' or arg == 'selectors':
                    # convert string to dict here
                    arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                    try:
                        params[arg] = arg_json
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(f"init.py error: {e}")
        return params
    
    def create_storage_account(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_storage', 'create_storage_account', self.args)
        
        if params["ip_addresses"]:
            params["ip_addresses"] = params["ip_addresses"].split(",")

            try:
                for ip in params["ip_addresses"]:
                    ip_addr = ipaddress.ip_network(ip)
                    if "/" in ip and ip_addr.prefixlen > 30: 
                        raise Exception(f"{ip} prefix is greater than 30. /31 and /32 prefix lengths are not allowed.") 
            except ValueError:
                raise Exception(f"{params['ip_addresses']} is not a valid CIDR block.")
        
        params["subnet_ids"] = params["subnet_ids"].split(",")
        while("" in params["subnet_ids"]):
            params["subnet_ids"].remove("")
        
        super().add_azure_resource("az_storage_account", self.args.name, params)

    def create_blob_container(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_storage', 'create_blob_container', self.args)
        
        super().add_azure_resource("az_blob_container", self.args.name, params)

    def create_file_share(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_storage', 'create_file_share', self.args)
        
        super().add_azure_resource("az_file_share", self.args.name, params)

    def create_redis_cache(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_storage', 'create_redis_cache', self.args)

        params["family"] = "C"
        if (params["sku_name"] == "Premium"):
            params["family"] = "P"
        else:
            params["subnet_id"] = None
        
        params["managed_ids"] = params["managed_ids"].split(",")
        params["zones"] = params["zones"].split(",")
        
        super().add_azure_resource("az_redis_cache", self.args.name, params)

