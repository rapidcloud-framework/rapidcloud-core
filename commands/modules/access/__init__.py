__author__ = "Igor Royzis"

import glob

from commands.cli_worker.license_worker import LicenseWorker
from commands.kc_metadata_manager.aws_metadata import Metadata


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        if hasattr(self.args, "env_info"):
            print(f"module_metadata__init {self.args.env_info}")
        else:
            print("module_metadata__init: no env env")
        self.lic_worker = LicenseWorker(self.args)

    def create_role(self, metadata=None):
        role = {
            "name": self.args.name,
            "access_all": self.args.access_all,
            "access_description": self.args.access_description
        }
        if self.args.name not in ["RAPIDCLOUD_ADMIN", "RAPIDCLOUD_VIEWER"]:
            for tier in self.lic_worker.contact_lic_server("get_tiers"):
                if tier.get("enabled", False):
                    permission_name = f"access_{tier['feature']}"
                    if hasattr(self.args, permission_name):
                        role[permission_name] = getattr(self.args, permission_name)
            self.lic_worker.save_role(role)


    def assign_role(self, metadata=None):
        user_email = self.args.access_email
        user_role = self.args.access_role
        ux_context = self.args.access_ux_context
        self.lic_worker.assign_role(user_email, user_role, ux_context)
