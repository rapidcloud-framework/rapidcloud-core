__author__ = "mlevy@kinect-consulting.com"
import json
# import pathlib
import pprint
# from ipaddress import ip_network

# import boto3
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
# import sys
# from ipaddress import ip_network

# default vars

# subnet_tiers = ['public', 'private', 'data', 'network']
# resources_to_build = ["vpc"]


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.boto3_session = super().get_boto3_session()

    def pp(self, v):
        print(pprint.pformat(v))

    def load_params(self, module, command, args):
        # we will populate this dict and pass it to the command functions
        params = {}

        # we're pulling all valus from the args object into a dict
        args_dict = vars(args)

        # we then load the actual args from the module's json
        json_args = self.get_module_json("net")[module][command]['args']

        # now we'll loop over them all
        for arg in json_args.keys():
            params[arg] = args_dict[f"{module}_{arg}"]
            if arg == 'tags':
                # convert string to dict here
                tags = json.loads(args_dict['net_tags'].replace("\\", ""))
                try:
                    params['tags'] = tags
                except Exception as e:
                    print(e)
        return params

    def create_vpc(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('net', 'create_vpc', self.args)
        resource_name = self.args.name
        resource_type = "aws_vpc"
        super().add_aws_resource(resource_type, resource_name, params)

    def create_subnet(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('net', 'create_subnet', self.args)
        resource_name = self.args.name
        resource_type = "aws_subnet"
        super().add_aws_resource(resource_type, resource_name, params)

    def create_igw(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('net', 'create_igw', self.args)
        resource_name = self.args.name
        resource_type = "aws_internet_gw"
        super().add_aws_resource(resource_type, resource_name, params)

    def create_natgw(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('net', 'create_natgw', self.args)
        resource_name = self.args.name
        resource_type = "aws_nat_gw"
        super().add_aws_resource(resource_type, resource_name, params)

    def create_route(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('net', 'create_route', self.args)
        resource_name = self.args.name
        resource_type = "aws_route"
        if params['transit_gateway_id'] == "" and params['vpc_peering_connection_id'] == "":
            raise Exception("You did not provide a peer or transit gateway, this route entry will not be created!")
        else:
            super().add_aws_resource(resource_type, resource_name, params)

    def create_endpoint(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('net', 'create_endpoint', self.args)
        resource_name = self.args.name
        resource_type = "aws_endpoint"
        super().add_aws_resource(resource_type, resource_name, params)
