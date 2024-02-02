__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import sys
import time
from datetime import datetime

from commands.cli_worker import CliWorker, ec2_linux_activation
from commands.cli_worker.license_worker import LicenseWorker
from commands.colors import colors
from commands.general_utils import load_json_file
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.azure_infra import AzureInfra
from commands.kc_metadata_manager.gcp_infra import GcpInfra
from progress.spinner import Spinner
from server.utils.gcp_metadata_utils import get_gcloud_cli_configuration_name


class CloudActivator(object):
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args
        #super().__init__(args)

    def activate(self, cli_worker: CliWorker):
        config = load_json_file('config/activation.json')
        curr_email = config['email'] if 'email' in config else ''
        self.email = cli_worker.get_user_input(('email','Email', 'Enter your work email address', curr_email, True, False)).lower()

        print(f"\n\nkc activate --email {self.email}\n\n")
        with open('config/activation.json', 'w') as f:
            config["email"] = self.email
            config["timestamp"] = str(datetime.now())
            json.dump(config, f, indent=2)

        # TODO revisit this - need for backward compatibility for now
        for cloud in load_json_file('config/cloud_context.json').get("supported_clouds", ["aws","azure"]):
            cloud_profile_file = f'config/{cloud}_profile.json'
            cloud_config = load_json_file(cloud_profile_file)
            with open(cloud_profile_file, 'w') as f:
                cloud_config["email"] = self.email
                cloud_config["timestamp"] = str(datetime.now())
                json.dump(cloud_config, f, indent=2)

        # Activate
        lic_worker = LicenseWorker(self.args)
        activation = lic_worker.activate()
        print(f"\n{self.email} activation details:")
        if activation and "activations" in activation and self.email in activation["activations"]:
            print(json.dumps(activation["activations"][self.email], indent=2, default=str))
        else:
            print(activation)

        if self.args.mode == 'cli':
            self.activate_linux(lic_worker)

        return config
    

    def print_post_activation_instructions(self):
        if self.args.mode == "cli":
            print(f"\n{colors.OKGREEN}Activation email has been sent to {self.args.email}.{colors.ENDC}\nPlease open it and `Confirm your RapidCloud Activation` (check for spam folder just in case).\nIf you cannot find activation email, please contact us online at https://rapid-cloud.io/contact-us/ or by phone (305) 428-8255")

            print(f"\nYou can now create your RapidCloud environment by running following command:\n{colors.FAIL}kc init create-env{colors.ENDC}")

            print(f"\nOr switch to an existing RapidCloud environment by running following command:\n{colors.FAIL}kc init set-env --env [name_of_env]{colors.ENDC}")

            print(f"\nThen start RapidCloud Console Server:")
            if "linux" in sys.platform:
                print(f"{colors.FAIL}nohup ./kc --no-browser &>./logs/rapidcloud.log &{colors.ENDC}")
            else:
                print(f"{colors.FAIL}kc --no-browser{colors.ENDC}\n")

            print("\nRapidCloud documentation can be found here https://rapid-cloud.io\n")
        else:
            notes = f"""Activation email has been sent to {self.args.email}. Please open it and `Confirm your RapidCloud Activation` (check for spam folder just in case). If you cannot find activation email, please contact us online at https://rapid-cloud.io/contact-us/ or by phone (305) 428-8255"""
            setattr(self.args, "cmd_result_notes", notes)

    def bootstrap(self):
        raise RuntimeError("Subclass should override me.")

    def uninstall(self):
        print("Uninstall has not been implemented yet")
        pass

    def activate_linux(self, lic_worker: LicenseWorker):
        pass

    def update(self):
        pass

class AzureActivator(CloudActivator):
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args
        super().__init__(args)

    def bootstrap(self):
        print("Bootstrapping RapidCloud for your target Azure Account...")
        AzureInfra(self.args).create_metadata_tables()
        # status = ''
        # while status != 'ACTIVE':
        #     time.sleep(.1)
        #     status = super().get_dynamodb_client().describe_table(TableName=self.TABLE_NAME)['Table']['TableStatus']

    def update(self):
        spinner = Spinner('Updating RapidCloud Metadata tables')
        AzureInfra(self.args).create_metadata_tables()
        for i in range(1,10):
            time.sleep(.1)
            spinner.next()

class AwsActivator(CloudActivator):
    TABLE_NAME = 'kc_activation'
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args
        super().__init__(args)

    def bootstrap(self):
        print("Bootstrapping RapidCloud for your target AWS Account...")
        # create all required metadata tables
        awsinfra = AwsInfra(self.args)
        awsinfra.create_metadata_tables()
        status = ''
        while status != 'ACTIVE':
            time.sleep(.1)
            status = awsinfra.get_dynamodb_client().describe_table(TableName="profile")['Table']['TableStatus']

    def update(self):
        spinner = Spinner('Updating RapidCloud Metadata tables')
        AwsInfra(self.args).create_metadata_tables()
        for i in range(1,10):
            time.sleep(.1)
            spinner.next()

    def activate_linux(self, lic_worker: LicenseWorker):
        # For Amazon Linux Only (set up EIP, SSL cert, subdomain)
        platform = sys.platform
        print(f"\nYou're running on {platform}.")
        if "linux" in platform:
            ec2_linux_activation.activate_amazon_linux_ec2(self.email, lic_worker)

    def uninstall(self):
        if not self.aws_profile is None:
            print(f"\n\nATTENTION!\n\nUninstalling RapidCloud will backup all environments metadata, then delete all metadata tables in the account associated with {colors.FAIL}{self.aws_profile}{colors.ENDC} AWS profile. If you want to back up environment metadata, run {colors.FAIL}kc metadata export{colors.ENDC} for each environment to be backed up. Uninstall will not delete any AWS resources associated with the environments in the target AWS Account. If you uninstall RapidCloud, these AWS resources will no longer be managed by RapidCloud.\n")

            if super().prompt(f"Are you sure you want to uninstall RapidCloud?") == 'yes':
                print("\nUninstalling\n")
                #uninstall()
            else:
                print("\nUninstall cancelled\n")
        else:
            print("\nYour RapidCloud instance has not been activated. Uninstall is not applicabble.\n")

class GcpActivator(CloudActivator):
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args
        super().__init__(args)

    def bootstrap(self):
        pass # Nothing to do here because GCP Firestore doesn't need a 'table' (collection) to be created in advance before a 'record' (document) can be inserted into it.
        # print("Bootstrapping RapidCloud for your target GCP Project...")
        # GcpInfra(self.args).create_metadata_tables()
