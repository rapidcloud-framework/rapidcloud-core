__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import os
import socket
import sys
import requests

from commands import general_utils, print_utils
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.cli_worker.license_worker import LicenseWorker
from licensing.admin import admin

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def get_config(self):
        with open('config/aws_profile.json', 'r') as f:
            return json.load(f)


    def upgrade(self, metadata=None):
        accounts = self.contact_admin_server("upgrade")
        self().list_activations(self)


    def list_accounts(self, metadata=None):
        accounts = self.contact_admin_server("get_accounts")
        if accounts:
            # print(json.dumps(accounts, indent=2, default=str))
            for acc in accounts:
                acc['user_count'] = len(acc['activations']) if 'activations' in acc else 0
            print_utils.print_grid_from_json(accounts, cols = ['domain', 'tier', 'user_count', 'start','end','timestamp'], title="Accounts")


    def list_activations(self, metadata=None):
        accounts = self.contact_admin_server("get_accounts")
        print(accounts)


    def get_api_url(self, email, admin):
        api_prefix = "admin" if admin else "lic"
        app_mode = general_utils.get_app_mode()
        api_name = f"{api_prefix}_{app_mode}_url"
        return general_utils.API[api_name]


    def contact_admin_server(self, action, email=None):
        config = self.get_config()
        request = {
            "action": action,
            "command": self.args.command if self.args else None,
            "email": email if email else config.get('email'),
            "domain": self.args.domain if self.args.domain else None,
            "hostname": socket.gethostname(),
            "config": config
        }
        result = None
        try:
            self.logger.info(json.dumps(request, indent=2))
            if general_utils.in_local_mode():
                self.logger.info("local admin...")
                event = {
                    "httpMethod": "POST",
                    "body": json.dumps(request)
                }
                result = json.loads(admin.lambda_handler(event, None)['body'])
            else:
                url = f"{self.get_api_url(config.get('email'), admin=True)}/admin"
                print(url)
                result = requests.post(url, data = json.dumps(request, indent=2)).json()
        except:
            self.logger.warn(result)
        return result


    def confirm_activation(self, metadata=None):
        user_activation = self.contact_admin_server("confirm_activation", self.args.admin_email)
        self.logger.info(json.dumps(user_activation, indent=2, default=str))


    def create_subdomain(self, metadata=None):
        params = {
            "subdomain": self.args.admin_subdomain,
            "public_ip": self.args.admin_public_ip
        }
        LicenseWorker(self.args).create_subdomain(params)


    def get_tenant_details(self, metadata=None):
        params = {
            "domain": self.args.admin_domain
        }
        tenant_details = LicenseWorker(self.args).get_tenant_details(params)
        self.logger.info(json.dumps(tenant_details, indent=2, default=str))


    def get_cross_account_role_cf_template(self, metadata=None):
        params = {
            "domain": self.args.admin_domain,
            "email": "any@" + self.args.admin_domain,
            "account": self.args.admin_account
        }
        tenant_details = LicenseWorker(self.args).get_cross_account_role_cf_template(params)
        self.logger.info(json.dumps(tenant_details, indent=2, default=str))
