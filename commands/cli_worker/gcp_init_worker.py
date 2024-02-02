#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
from datetime import datetime
from os.path import exists

from commands.general_utils import load_json_file
from commands.cli_worker.init_worker import InitWorker
from commands.colors import colors
from commands.kc_metadata_manager.gcp_profile import Profile
from commands.kc_metadata_manager.gcp_infra import GcpInfra
from commands.kc_metadata_manager.property import Property
from commands.kc_metadata_manager.profile_manager import get_profile_manager

from server.utils.gcp_metadata_utils import save_environment, get_gcp_environment_config, get_gcloud_cli_project_id, get_gcloud_cli_region, get_first_vpc_id, enable_gcp_service_apis

class GcpInitWorker(InitWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.env = super().get_env()
        self.args = args


    def create_env(self):
        if self.args.command == 'create-env':
            delattr(self.args, 'env') # in case `env` was passed in by mistake

        print("\nYou're creating or updating a RapidCloud environment for GCP\n")
        config = load_json_file(f'config/{self.args.cloud}_profile.json', f'config/{self.args.cloud}_default_profile.json')

        # arguments
        env_config = {}
        curr_client, curr_workload, curr_env_suffix, curr_shared, curr_project, curr_vpc, curr_ssh_pub_key, curr_region, curr_vpn_only, curr_ips_for_ssh = '', '', '', '', '', '', '', '', '', ''

        env_config = get_gcp_environment_config(self.env)

        # .......... 1st round of questionnair ................
        if not env_config is None:
            curr_client = env_config['client'] if 'client' in env_config else ''
            curr_workload = env_config['workload'] if 'workload' in env_config else ''
            curr_env_suffix = env_config['env_suffix'] if 'env_suffix' in env_config else ''
            curr_shared = env_config['shared'] if 'shared' in env_config else 'yes'
            curr_project = env_config['project'] if 'project' in env_config else get_gcloud_cli_project_id()
            curr_region = env_config['region'] if 'region' in env_config else get_gcloud_cli_region()

        prompts = {
            # [name, description, prompt, current value, required, force naming]
            'client': ['client','Company Name Abbreviation', 'Enter your company name abbreviation (letters and numbers only)', curr_client, True, True],
            'workload': ['workload','Workload', 'Enter your workload name (letters and numbers only)', curr_workload, True, True],
            'env_suffix': ['env_suffix','Environment', 'Enter environment (e.g dev|qa|prod)', curr_env_suffix, True, True],
            'shared': ['shared','Shared', 'Is this environment shared with other engineers? (yes|no)', curr_shared, True, True],
            'env_project_id': ['env_project_id','GCP Project ID', 'Enter the GCP Project ID for the environment', curr_project, True, False],
            'region': ['region','GCP Region', 'Enter GCP Region (e.g. us-east1)', curr_region, True, False],
        }

        for key, prompt in prompts.items():
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            env_config[key] = value

        enable_gcp_service_apis(["storage.googleapis.com",   ## https://bitbucket.org/kinect-consulting/rapidcloud-core/src/19e42b9439da54d2fd8e7cca563be6139a3dfac7/commands/kc_metadata_manager/gcp_infra.py#lines-99
                                 "compute.googleapis.com",   ## https://bitbucket.org/kinect-consulting/rapidcloud-core/src/b97d32244b50deee8543e4c8dffb5884074d9488/server/utils/gcp_metadata_utils.py#lines-88
                                 "firestore.googleapis.com", ## NoSQL tables for RC metadata
                                ])

        # .......... 2nd round of questionnair ................
        if not env_config is None:
            curr_vpc = env_config['vpc'] if 'vpc' in env_config else get_first_vpc_id()
            #curr_ssh_pub_key = env_config['ssh_pub_key'] if 'ssh_pub_key' in env_config else ''
            curr_vpn_only = env_config['vpn_only'] if 'vpn_only' in env_config else 'no'
            #curr_ips_for_ssh = env_config['ips_for_ssh'] if 'ips_for_ssh' in env_config else ''

        prompts = {
            'vpc': ['vpc','GCP VPC', 'Enter the existing GCP VPC Name', curr_vpc, True, False],
            # 'ssh_pub_key': ['ssh_pub_key','SSH Public Key', 'For EMR Only: Enter existing SSH Public Key if you require EMR nodes access', curr_ssh_pub_key, False, False],
            # 'ips_for_ssh': ['ips_for_ssh','List of IP Addresses', 'For EMR Only: IP Addresses to be allowed SSH Access to EMR Cluster', curr_ips_for_ssh, False, False],
            'vpn_only': ['vpn_only','VPN Only', 'Are you using VPN to connect to GCP? (yes|no)', curr_vpn_only, True, False],
        }

        for key, prompt in prompts.items():
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            env_config[key] = value

        env = f"{self.args.client}_{self.args.workload}_{self.args.env_suffix}".lower()
        self.logger.info(f"setting `args.env` {env}")
        setattr(self.args, 'env', env)

        # change environment context in "cli" mode
        if self.args.mode == 'cli':
            with open('config/gcp_profile.json', 'w') as f:
                config['default_region'] = self.args.region
                config['env'] = env
                json.dump(config, f, indent=2)

        with open(f"config/environments/{self.args.env}_config.json", 'w') as f:
            env_config['timestamp'] = str(datetime.now())
            json.dump(env_config, f, indent=2)

        profile_obj = Profile(self.args)
        profile = profile_obj.get_profile(env)
        if profile is None:
            GcpInfra(self.args).create_tf_state()
            Property(self.args).set_default_properties()

        # save profile and all the necessary gcp_infra items
        profile_obj.save_profile(profile)
        save_environment(env, get_profile_manager().get_env_project_id())

        if profile is None:
            print(f"\n{colors.OKGREEN}You've successfully created RapidCloud environment [{self.args.env}]!{colors.ENDC}")
        else:
            print(f"\n{colors.OKGREEN}You've successfully updated RapidCloud environment [{self.args.env}]!{colors.ENDC}")

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
            with open('config/gcp_profile.json') as f:
                gcp_profile_json = json.load(f)

            with open(env_config_file) as f:
                gcp_profile_json['env'] = self.args.env

            with open('config/gcp_profile.json', 'w') as f:
                json.dump(gcp_profile_json, f, indent=2)

        if show_status:
            self.show_kc_status()


    def find_env(self, env):
        profile_obj = Profile(self.args)
        profile = profile_obj.get_profile(env)

        if profile:
            print(f" - find_env(): {colors.OKGREEN}env_project_id='{get_profile_manager().get_env_project_id()}', region='{profile['region']}'{colors.ENDC}")
            return profile
        else:
            self.logger.error(f"Failed to find profile for env={env}, project_id={get_profile_manager().get_env_project_id()}")
            return None


    def list_env(self):
        Profile(self.args).list()


    # Override grandparent CliWorker.create_missing_env_config()
    # def create_missing_env_config(self, profile):
    #     pass
