__author__ = "agarciaortiz@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        self.boto3_session = super().get_boto3_session()

        # use boto3 clients or resources as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def create_permission_set(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)

        aws_managed_policy_arns = []
        if self.args.sso_aws_managed_policy_arns:
            aws_managed_policy_arns = self.args.sso_aws_managed_policy_arns.replace(" ","").split(",")

        params = {
            "description": self.args.sso_description,
            "relay_state": self.args.sso_relay_state,
            "session_duration": self.args.sso_session_duration,
            "aws_managed_policy_arns": aws_managed_policy_arns,
            "inline_policy": self.args.sso_inline_policy.strip()
        }

        super().add_infra_resource("aws_ssoadmin_permission_set", self.args.name, params)

    def create_account_assignment(self, metadata=None):
        fqn = f"{self.env}_aws_ssoadmin_account_assignment_{self.args.sso_permission_set_name}_{self.args.sso_account_name}"
        super().delete_infra_metadata(name=self.args.name)

        #non rc managed principals
        principal_ids = []
        if self.args.sso_principal_ids:
            principal_ids = self.args.sso_principal_ids.replace(" ","").split(",")

        #rc managed group principals
        principal_groups = []
        if not principal_ids and (self.args.sso_principal_type.lower() == "group" and self.args.sso_principal_groups):
            principal_groups = self.args.sso_principal_groups.replace(" ","").split(",")

        #rc managed user principals
        principal_users = []
        if not principal_ids and (self.args.sso_principal_type.lower() == "user" and self.args.sso_principal_users):
            principal_users = self.args.sso_principal_users.replace(" ","").split(",")

        params = {
            "permission_set_name": self.args.sso_permission_set_name,
            "principal_type": self.args.sso_principal_type.lower(),
            "account_name": self.args.sso_account_name,
            "principal_ids": principal_ids,
            "principal_groups": principal_groups,
            "principal_users": principal_users
        }

        super().add_infra_resource("aws_ssoadmin_account_assignment", metadata["name"], params, fqn=fqn)

    def create_user(self, metadata=None):
        super().delete_infra_metadata(name=metadata["name"])
        params = {
            "user_name": self.args.sso_user_name,
            "display_name": self.args.sso_display_name,
            "first_name": self.args.sso_first_name,
            "last_name": self.args.sso_last_name,
            "email": self.args.sso_email
        }

        super().add_infra_resource("aws_identitystore_user", metadata["name"], params)

    def create_group(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)

        members = []
        if self.args.sso_members:
            members = self.args.sso_members.replace(" ","").split(",")

        params = {
            "description": self.args.sso_description,
            "members": members
        }

        super().add_infra_resource("aws_identitystore_group", self.args.name, params)
