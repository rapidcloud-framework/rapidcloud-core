__author__ = "agarciaortiz"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
import json

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        self.boto3_session = super().get_boto3_session()

        # use boto3 clients or resources as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def create(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)

        if not self.args.org_aws_service_access_principals:
            service_access_principals = []
        else:
            service_access_principals = self.args.org_aws_service_access_principals.replace(" ","").split(",")
        
        if not self.args.org_enabled_policy_types:
            enabled_policy_types = []
        elif self.args.org_enabled_policy_types.lower() == "all":
            enabled_policy_types = ["SERVICE_CONTROL_POLICY", "TAG_POLICY", "BACKUP_POLICY", "AISERVICES_OPT_OUT_POLICY"]
        else:
            enabled_policy_types = self.args.org_enabled_policy_types.replace(" ","").split(",")

        params = {
            "aws_service_access_principals": service_access_principals,
            "enabled_policy_types": enabled_policy_types
        }

        resource_type = "aws_organizations_organization"

        resource_name = self.args.name

        super().add_aws_resource(resource_type, resource_name, params)

    def create_ou(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        scps = [] if not self.args.org_scps else self.args.org_scps.replace(" ","").split(",")
        params = {
            "parent_name": self.args.org_parent_name,
            "parent_type": self.args.org_parent_type,
            "scps": scps
        }
        super().add_aws_resource("aws_organizations_organizational_unit", self.args.name, params)

    def create_account(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        scps = [] if not self.args.org_scps else self.args.org_scps.replace(" ","").split(",")
        params = {
            "parent_name": self.args.org_parent_name,
            "email": self.args.org_email,
            "scps": scps
        }
        super().add_aws_resource("aws_organizations_account", self.args.name, params)

    def create_scp(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra(name=self.args.name)
        params = {
            "policy_text": self.args.org_policy_text.strip(),
            "description": self.args.org_description
        }
        super().add_aws_resource("aws_organizations_policy", self.args.name, params)