#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
import json
import logging
import os
import sys
from datetime import datetime
from ipaddress import ip_address

import pyfiglet
import requests
from commands import general_utils, print_utils
from commands.cli_worker.aws_worker import AwsWorker
from commands.colors import colors


class LicenseWorker(AwsWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        self.cloud_config = {}
        self.cloud_context = general_utils.load_json_file("config/cloud_context.json")
        self.cloud = self.args.cloud if self.args.cloud is not None else self.cloud_context["cloud"]
        for cloud in self.cloud_context.get("supported_clouds", ["aws","azure","gcp"]):
            cloud_profile_file = f"config/{cloud}_profile.json"
            try:
                with open(cloud_profile_file, "r") as f:
                    self.cloud_config[cloud] = json.load(f)
            except Exception as e:
                self.logger.warn(f"file {cloud_profile_file} not found")
        self.config = self.cloud_config[self.cloud]

        pass  # Placeholder to allow a potential debugger breakpoint


    def get_api_url(self):
        app_mode = general_utils.get_app_mode(self.config.get('email'))
        api_name = f"lic_{app_mode}_url"
        return general_utils.API[api_name]


    def contact_lic_server(self, action, feature=None, params={}):
        print_utils.info((action, feature), "contact_lic_server")
        if not feature:
            feature = self.args.feature if hasattr(self.args, "feature") else None
        command = self.args.command
        tier = self.args.tier if self.args.tier is not None else "1"
        domain = self.args.domain
        if getattr(self.args, 'current_session_email') != None:
            email = getattr(self.args, "current_session_email")
        else:
            email = self.config.get('email')
        phone = self.config.get('phone')
        token = self.config.get('token')

        request = {
            "cloud": self.cloud,
            "action": action,
            "feature": feature,
            "command": command,
            "email": email,
            "domain": domain,
            "phone": phone,
            "token": token,
            "tier": tier,
            "hostname": super().get_hostname(),
            "config": self.config,
            "extra_params": params
        }
        result = None
        try:
            print_utils.info(json.dumps(request, indent=2), "REQUEST")
            if general_utils.in_local_mode():
                # run licensing locally
                from licensing import licensing
                self.logger.info("local licensing...")
                event = {
                    "httpMethod": "POST",
                    "body": json.dumps(request)
                }
                result = json.loads(licensing.lambda_handler(event, None)['body'])
            else:
                # contact license server
                url = f"{self.get_api_url()}/license/verify"
                # self.logger.info("remote licensing...")
                result = requests.post(url, data = json.dumps(request)).json()
            return result
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn(result)
            pass


    def verify_lic(self):
        verification = self.contact_lic_server("verify")
        print_utils.info(verification, "VERIFICATION")
        if self.args.feature == "console":
            return verification

        if verification.get("email") is None:
            verification['exit'] = True
            print(f"System Message: {colors.FAIL}{verification['msg']}{colors.ENDC}\n")
            return verification

        if verification:
            verification['exit'] = False

        if not verification.get('verified', False):
            # verification['msg'] = msg
            print()
            print(pyfiglet.figlet_format("Oops, sorry!"))
            if verification['msg'] is not None:
                print()
                print(f"System Message: {colors.FAIL}{verification['msg']}{colors.ENDC}")
            else:
                print()
                print(f"Something went wrong. Have you activated RapidCloud? If not, please activate via `kc activate` command.")
            print()

            if not verification['verified']:
                verification['exit'] = True
                print(f"{colors.FAIL}Your RapidCloud instance has not been properly activated{colors.ENDC}")
                print("")
                print(f"Run `{colors.OKBLUE}kc activate{colors.ENDC}` or contact RapidCloud support")
                print("")

            if not verification['activation_confirmed']:
                verification['exit'] = True
                print(f"{colors.FAIL}You have not confirmed your RapidCloud activation. Please check for a confirmation email and click `confirm` link. If you cannot find confirmation email, check your junk mail folder or run `kc activate` again.{colors.ENDC}")
                print("")

            if not verification['agreed_terms']:
                print("")
                print("")
                print(f"{colors.OKBLUE}Please review RapidCloud Terms at{colors.ENDC}: https://rapid-cloud.s3.amazonaws.com/docs/README.html#terms")
                print("")
                agreed = input(f"{colors.OKBLUE}I agree to RapidCloud terms (yes|no):{colors.ENDC} ")
                if agreed == "yes":
                    agreed = self.agree_terms()
                else:
                    verification['exit'] = True

            if not verification['authorized']:
                verification['exit'] = True
                self.logger.warning("Your subscription tier doesn't allow this command. Please upgrade or contact Kinect Consulting for support")

        return verification


    def agree_terms(self):
        return self.contact_lic_server("agree_terms")


    def activate(self):
        return self.contact_lic_server("activate")
    

    def save_role(self, role):
        return self.contact_lic_server("save_role", params={"role":role})


    def assign_role(self, email, role, ux_context):
        params = {
            "email": email,
            "role": role,
            "ux_context": ux_context
        }
        return self.contact_lic_server("assign_role", params=params)


    def confirm(self):
        params = {
            "email": self.args.email,
            "code": self.args.code
        }
        return self.contact_lic_server("confirm_activation", params=params)


    def subscribe(self):
        if self.args.command is None:
            return self.contact_lic_server("subscribe")
        elif self.args.command == "cancel":
            return self.contact_lic_server("cancel_subscription")


    def account_details(self):
        account_details = self.contact_lic_server("get_activation")
        print(f"\n{colors.OKGREEN}Subscription:{colors.ENDC}\n")
        # print(json.dumps(account_details, indent=2, default=str))
        if 'domain' in account_details:
            print(f"    Domain: {account_details['domain']}")
        if 'tier' in account_details:
            print(f"      Tier: {general_utils.TIERS[account_details['tier']]}")
        if 'status' in account_details:
            print(f"    Status: {account_details['status']}")
        if 'stripe' in account_details and 'current' in account_details['stripe']:
            start = int(account_details['stripe']['current']['period_start'])
            print(f"     Start: {datetime.fromtimestamp(start)}")
            end = int(account_details['stripe']['current']['period_end'])
            print(f"       End: {datetime.fromtimestamp(end)}")
            if 'auto-renew' in account_details['stripe']['current']:
                auto_renew = account_details['stripe']['current']['auto-renew']
                print(f"Auto-renew: {auto_renew}")
            invoice_url = account_details['stripe']['current']['hosted_invoice_url']
            print(f"Invoice: {invoice_url}")
        print("\n")
        activations = []
        if 'activations' not in account_details:
            account_details['activations'] = {
                account_details['email']: account_details
            }

        for email in sorted(account_details['activations'].keys()):
            activation = account_details['activations'][email]
            activation['email'] = email
            activation['access_email'] = email
            role = "RAPIDCLOUD_VIEWER"
            if 'role' in activation:
                role = activation['role']
            activation['role'] = role
            activation['access_role'] = role
            if 'agreed_terms' in account_details:
                activation['agreed_terms'] = account_details['agreed_terms'][email]['agreed'] if email in account_details['agreed_terms'] else 'No'
            activations.append(activation)
        print(f"{colors.OKGREEN}Activations:{colors.ENDC}")
        cols = ['email','role','status','hostname','agreed_terms','timestamp']
        print_utils.print_grid_from_json(activations, cols)
        return activations


    def get_presigned_url(self, tf_module_source):
        return self.contact_lic_server("get_presigned_url", params={
            "tf_module_source": tf_module_source
        })


    def create_subdomain(self, params):
        return self.contact_lic_server("create_subdomain", params=params)


    def set_account_permissions(self):
        return self.contact_lic_server("set_account_permissions", params={
            "account": self.args.account
        })

    def get_tenant_details(self, params):
        return self.contact_lic_server("get_tenant_details", params=params)

    def get_cross_account_role_cf_template(self, params):
        return self.contact_lic_server("get_cross_account_role_cf_template", params=params)
