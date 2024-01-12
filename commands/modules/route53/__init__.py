__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"


import boto3
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):
    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.boto3_session = super().get_boto3_session()

    def load_params(self, module, command, args):
        # we will populate this dict and pass it to the command functions
        params = {}

        # we're pulling all valus from the args object into a dict
        args_dict = vars(args)

        # we then load the actual args from the module's json
        json_args = self.get_module_json("route53")[module][command]['args']

        # now we'll loop over them all
        for arg in json_args.keys():
            params[arg] = args_dict[f"{module}_{arg}"]
        return params

    def add_record(self, metadata=None):
         # Delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra(name=self.args.record_name)
        params = self.load_params('route53', 'add_record', self.args)
        resource_name = self.args.record_name
        resource_type = "aws_route53_record"
        super().add_aws_resource(resource_type, resource_name, params)
    
    def create_hosted_zone(self, metadata=None):
         # Delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = self.load_params('route53', 'create_hosted_zone', self.args)
        resource_name = self.args.name
        resource_type = "aws_route53_hosted_zone"
        super().add_aws_resource(resource_type, resource_name, params)