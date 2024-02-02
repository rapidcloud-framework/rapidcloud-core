__author__ = "skammadanam"

import base64
import json
import ipaddress
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_infra import AzureInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # azure sdk
        # self.boto3_session = super().get_boto3_session()

        # use azure sdk as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def load_params(self, module, command, args):
        # we will populate this dict and pass it to the command functions
        params = {}
        try:
            # we're pulling all valus from the args object into a dict
            args_dict = vars(args)

            # we then load the actual args from the module's json
            json_args = self.get_module_json("az_frontdoor")[module][command]['args']

            # now we'll loop over them all
            for arg in json_args.keys():
                params[arg] = args_dict[f"{module}_{arg}"]
                if arg == 'tags':
                    # convert string to dict here
                    arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                    try:
                        params[arg] = arg_json
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(f"init.py error: {e}")
        return params
    
    def create_origingroup(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_frontdoor', 'create_origingroup', self.args)
        
        super().add_azure_resource("frontdoor_origingroup", self.args.name, params)

    def create_origin(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_frontdoor', 'create_origin', self.args)
        
        super().add_azure_resource("frontdoor_origin", self.args.name, params)

    def create_fd_profile(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_frontdoor', 'create_fd_profile', self.args)
        
        super().add_azure_resource("frontdoor_profile", self.args.name, params)

    def create_fd_endpoint(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_frontdoor', 'create_fd_endpoint', self.args)
        
        super().add_azure_resource("frontdoor_endpoint", self.args.name, params)
    
    def create_fd_domain(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_frontdoor', 'create_fd_domain', self.args)
        
        super().add_azure_resource("frontdoor_domain", self.args.name, params)

    def create_fd_route(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_frontdoor', 'create_fd_route', self.args)

        params['origins'] = params['origins'].split(",")
        params['domains'] = params['domains'].split(",")
        params['patterns_to_match'] = params['patterns_to_match'].split(",")
        params['supported_protocols'] = params['supported_protocols'].split(",")
        lst = params["supported_protocols"]
        if params["redirect_https"] == "true":
            lst.append("Http") if "Http" not in lst else lst
            lst.append("Https") if "Https" not in lst else lst
        
        params["supported_protocols"] = lst
        
        super().add_azure_resource("frontdoor_route", self.args.name, params)
