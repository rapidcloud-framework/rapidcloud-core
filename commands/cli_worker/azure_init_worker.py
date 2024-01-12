#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import json
import logging
import os
from os.path import exists
from commands import general_utils
from commands.cli_worker.init_worker import InitWorker
from commands.colors import colors
from commands.kc_metadata_manager.activation import AzureActivator
from commands.kc_metadata_manager.azure_infra import AzureInfra
from commands.kc_metadata_manager.azure_metadata import Metadata
from commands.kc_metadata_manager.azure_profile import Profile
from commands.kc_metadata_manager.property import Property
from server.utils.azure_environment_utils import AzureConfigUtils

class AzureInitWorker(InitWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.env = super().get_env()
        self.args = args


    def create_env(self):
        if self.args.command == 'create-env':
            delattr(self.args, 'env') # in case `env` was passed in by mistake

        print("\nYou're creating or updating a RapidCloud environment for Azure\n")

        cloud_config = AzureConfigUtils.get_azure_profile(self.env)
        env_config = AzureConfigUtils.get_azure_environment_config(cloud_config.get('env'))
        if env_config is None:
            env_config = {}

        prompts = {
            # [name, description, prompt, current value, required, force naming]
            'client': [
                'client','Company Name Abbreviation', 'Enter your company name abbreviation (letters and numbers only)', env_config.get('client',''), True, True],
            'workload': [
                'workload','Workload', 'Enter your workload name (letters and numbers only)', env_config.get('workload',''), True, True],
            'env_suffix': [
                'env_suffix','Environment', 'Enter environment (e.g dev|qa|prod)', env_config.get('env_suffix',''), True, True],
            'shared': [
                'shared','Shared', 'Is this environment shared with other engineers? (yes|no)', env_config.get('shared',''), True, True],
            'subscription': [
                'subscription','Azure Subscription ID', 'Enter your Azure Subscription ID', env_config.get('subscription',''), True, False],
            'vnet': [
                'vnet','Azure VNET', 'Enter Azure VNET ID', env_config.get('vnet',''), True, False],
            'region': [
                'region','Azure Region', 'Enter Azure Region (e.g. eastus)', env_config.get('region','useast'), True, False],
            'vpn_only': [
                'vpn_only','VPN Only', 'Are you using VPN to connect to Azure? (yes|no)', env_config.get('vpn_only',''), True, False],
        }

        cmd = "kc init create-env --cloud azure"
        for key, prompt in prompts.items():
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            env_config[key] = value
            if value != '':
                cmd += f" --{key} {value}"
        cmd += " --no-prompt"
        print(f"\n\n{cmd}\n\n")

        os.environ['AZURE_SUBSCRIPTION_ID'] = env_config["subscription"]
        env = f"{self.args.client}_{self.args.workload}_{self.args.env_suffix}".lower()
        self.logger.info(f"setting `args.env` {env}")
        setattr(self.args, 'env', env)

        # change environment context in "cli" mode
        if self.args.mode == 'cli':
            with open('config/azure_profile.json', 'w') as f:
                cloud_config['subscription'] = self.args.subscription
                cloud_config['default_region'] = self.args.region
                cloud_config['env'] = env
                json.dump(cloud_config, f, indent=2)

        env_file_dir = "config/environments/"
        if not os.path.exists(env_file_dir):
            os.makedirs(env_file_dir)
        with open(f"{env_file_dir}/{self.args.env}_config.json", 'w') as f:
            env_config['timestamp'] = str(datetime.now())
            json.dump(env_config, f, indent=2)

        creds_dir = "config/creds/"
        creds = {}
        if not os.path.exists(creds_dir):
            os.makedirs(creds_dir)
        with open(f"{creds_dir}/{self.args.env}_creds.json", 'w') as f:
            creds['client_id'] = os.environ['AZURE_CLIENT_ID']
            creds['client_secret'] = os.environ['AZURE_CLIENT_SECRET']
            creds['tenant_id'] = os.environ['AZURE_TENANT_ID']
            creds['subscription_id'] = os.environ['AZURE_SUBSCRIPTION_ID']
            creds['timestamp'] = str(datetime.now())
            json.dump(creds, f, indent=2)

        # check if target account already has RapidCloud environments, if not, generate cosmosdb metadata collection
        azure_metadata = Metadata(self.args)
        container_exists = azure_metadata.get_container("profile")
        if not container_exists:
            AzureActivator(self.args).bootstrap()

        profile_obj = Profile(self.args)
        profile = profile_obj.get_profile(env)
        new_profile = profile is None
        if profile is None:
            AzureInfra(self.args).create_tf_state()
            Property(self.args).set_default_properties()

        # save profile and all the necessary aws_infra items
        profile_obj.save_profile(profile)
        AzureConfigUtils.save_environment(env, self.args.subscription)

        if new_profile:
            print(f"\n{colors.OKGREEN}You've successfully created RapidCloud environment [{self.args.env}]!{colors.ENDC}")
        else:
            print(f"\n{colors.OKGREEN}You've successfully updated RapidCloud environment [{self.args.env}]!{colors.ENDC}")

        print(f"\nThe default credentials for the environment are saved in {creds_dir}/{self.args.env}_creds.json. Please update if required.\n\n")
        print(f"\nTo show environment details run:\n{colors.FAIL}kc init show-env\n")

        print(f"\nTo see current state of your environment run:\n{colors.FAIL}kc status{colors.ENDC}\n")


    def set_env(self, profile=None, show_status=True):
        if profile is None:
            profile = self.find_env(self.args.env)
            if profile is None:
                return

        self.logger.info(f"{self.args.env}: {profile['region']}")
        env_config_file = f"config/environments/{self.args.env}_config.json"
        if not exists(env_config_file):
            super().create_missing_env_config(profile)

        if exists(env_config_file) and self.args.mode == 'cli':
            with open('config/azure_profile.json') as f:
                azure_profile_json = json.load(f)

            with open(env_config_file) as f:
                azure_profile_json['env'] = self.args.env
                env_config = json.load(f)
                # if 'aws_profile' in env_config:
                #     azure_profile_json['aws_profile'] = env_config['aws_profile']

            with open('config/azure_profile.json', 'w') as f:
                json.dump(azure_profile_json, f, indent=2)

        if show_status:
            self.show_kc_status()


    def find_env(self, env):
        metadata = Metadata(self.args)
        self.logger.info(f"finding environment: {env}")
        profile = metadata.get_item_by_key('profile', env)
        if not profile is None:
            #profile = profile['Item']
            print(f" - {colors.OKGREEN}{profile['region']}{colors.ENDC}")
            return profile

        return None

    def create_missing_env_config(self, profile):
        AzureConfigUtils.create_missing_env_config(self.args.env, profile)