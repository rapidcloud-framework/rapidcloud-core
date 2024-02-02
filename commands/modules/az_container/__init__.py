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
            json_args = self.get_module_json("az_container")[module][command]['args']

            # now we'll loop over them all
            for arg in json_args.keys():
                params[arg] = args_dict[f"{module}_{arg}"]
                if arg == 'tags' or arg == 'node_labels' or arg == 'selectors':
                    # convert string to dict here
                    arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                    try:
                        params[arg] = arg_json
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(f"init.py error: {e}")
        return params
    
    def create_aks(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_container', 'create_aks', self.args)
        if (params["private_cluster_enabled"] == "false"):
            params["authorized_ip_ranges"] = params["authorized_ip_ranges"].split(",")

            for ip in params["authorized_ip_ranges"]:
                try:
                    ip_addr = ipaddress.ip_network(ip) 
                except ValueError:
                    raise Exception(f"{ip} is not a valid CIDR block.")
                    
        params["node_pool_zones"] = params["node_pool_zones"].split(",")
        group_ids = []
        if params["rbac_aad_admin_group_object_ids"]:
            group_ids = params["rbac_aad_admin_group_object_ids"].split(",")
        params["rbac_aad_admin_group_object_ids"] = group_ids
        
        super().add_azure_resource("aks_cluster", self.args.name, params)


    def create_node_pool(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_container', 'create_node_pool', self.args)        

        if params["os_type"].lower() == "windows" and len(self.args.name) > 6:
            raise Exception("Windows agent pool name can not be longer than 6 characters")
        
        params["zones"] = params["zones"].split(",")
        if params["node_taints"]:
            params["node_taints"] = params["node_taints"].split(",")
        
        super().add_azure_resource("aks_node_pool", self.args.name, params)

    def create_app_environment(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_container', 'create_app_environment', self.args)

        if not params["infrastructure_subnet_id"]:
            params["internal_load_balancer_enabled"] = False

        super().add_azure_resource("container_app_env", self.args.name, params)

    def create_app_environment_cert(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_container', 'create_app_environment_cert', self.args)
        #blob = params["certificate_blob_base64"].encode("ascii")
        #base64_bytes = base64.b64encode(blob)
        #base64_str = base64_bytes.decode("ascii")
        #params["certificate_blob_base64"] = base64_str
        super().add_azure_resource("container_app_cert", self.args.name, params)

    def create_app(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_container', 'create_app', self.args)
        if params["container_args"]:
            params["container_args"] = params["container_args"].split(",")
        #params["identity_ids"] = params["identity_ids"].split(",") if params["identity_ids"] else None

        super().add_azure_resource("container_app", self.args.name, params)

    def create_registry(self, metadata=None):
        AzureInfra(self.args).delete_infra_metadata(name=self.args.name)
        params = self.load_params('az_container', 'create_registry', self.args)
        
        if params["identity_type"]:
            params["identity_type"] = params["identity_type"].replace(',', ', ')
        params["identity_ids"] = params["identity_ids"].split(",") if params["identity_ids"] else []
        params["geolocations"] = params["geolocations"].split(",") if params["geolocations"] else []

        if params["encryption_client_id"] is not None:
            print(f"encryption_client_id: {params['encryption_client_id']}")
            ids = params["encryption_client_id"].split(";")
            print(f"len: {len(ids)}")
            params["encryption_client_id"] = ids[1]
            if ids[0] not in params["identity_ids"]:
                params["identity_ids"].append(ids[0])

        if params["location"] in params["geolocations"]:
            params["geolocations"].remove(params["location"])

        super().add_azure_resource("container_registry", self.args.name, params)