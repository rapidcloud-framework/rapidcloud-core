__author__ = "Abe Garcia"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "agarciaortiz@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_lb_params()
        super().add_aws_resource('aws_lb', self.args.name, params)

    def add_listener(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(metadata["module"], metadata["command"], self.args.name)

        metadata_params = metadata["params"]
        params = {
            "name": self.args.name,
            "load_balancer_name": metadata_params["lb_load_balancer_name"],
            "port": metadata_params["lb_port"],
            "protocol": metadata_params["lb_protocol"].upper(),
            "target_group_name": metadata_params["lb_target_group_name"],
            "alpn_policy": metadata_params["lb_alpn_policy"],
            "ssl_policy": metadata_params["lb_ssl_policy"],
            "certificate_arn": metadata_params["lb_certificate_arn"]
        }

        super().add_aws_resource('aws_lb_listener', self.args.name, params)

    def create_target_group(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(metadata["module"], metadata["command"], self.args.name)

        metadata_params = metadata["params"]
        preserve_client_ip = None
        if metadata_params["lb_preserve_client_ip"]:
            preserve_client_ip = "true" if metadata_params["lb_preserve_client_ip"].lower() in ["y", "yes", "true"] else "false"

        targets = ""
        target_type = metadata_params["lb_target_type"].lower()

        if target_type == "ip":
            targets = metadata_params["lb_ip_targets"].replace(" ","").split(",")
        if target_type == "instance":
            targets = metadata_params["lb_ec2_targets"].replace(" ","").split(",")

        params = {
            "name": self.args.name,
            "port": metadata_params["lb_port"],
            "protocol": metadata_params["lb_protocol"].upper(),
            "target_type": target_type,
            "vpc_id": metadata_params["lb_vpc_id"],
            "load_balancer_type": metadata_params["lb_load_balancer_type"].lower(),
            "load_balancing_algorithm_type": metadata_params["lb_load_balancing_algorithm_type"],
            "preserve_client_ip": preserve_client_ip,
            "ip_address_type": metadata_params["lb_ip_address_type"].lower() if metadata_params["lb_ip_address_type"] else None,
            "protocol_version": metadata_params["lb_protocol_version"].upper() if metadata_params["lb_protocol_version"] else None,
            "targets": targets
        }
        
        super().add_aws_resource('aws_lb_target_group', self.args.name, params)