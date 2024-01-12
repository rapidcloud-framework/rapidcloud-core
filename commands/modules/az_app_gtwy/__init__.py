__author__ = "skammadanam@kinect-consulting.com"

import base64
import json
import ipaddress
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
            json_args = self.get_module_json("az_app_gtwy")[module][command]['args']

            # now we'll loop over them all
            for arg in json_args.keys():
                params[arg] = args_dict[f"{module}_{arg}"]
                if arg == 'tags' or arg == 'selectors':
                    # convert string to dict here
                    arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                    try:
                        params[arg] = arg_json
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(f"init.py error: {e}")
        return params
    
    def create_app_gtwy(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_app_gtwy', 'create_app_gtwy', self.args)

        params["zones"] = params["zones"].split(",")
        params["identity_ids"] = params["identity_ids"].split(",")
        params["backend_ips"] = params["backend_ips"].split(",")
        params["backend_fqdns"] = params["backend_fqdns"].split(",")
        
        super().add_azure_resource("azapp_gateway", self.args.name, params)

    def create_waf_policy(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_app_gtwy', 'create_waf_policy', self.args)
        
        super().add_azure_resource("waf_policy", self.args.name, params)