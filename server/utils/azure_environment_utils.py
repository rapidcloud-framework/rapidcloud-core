

from datetime import datetime
from fileinput import filename
import json
import logging
import os

logger = logging.getLogger("azure_metadata_utils")

class AzureConfigUtils:

    def get_all_azure_environments():
        filename = './config/all_azure_profiles.json'
        try:
            with open(filename, 'r') as f:
                envs = json.loads(f.read())
                return envs
        except Exception as e:
            logger.error(f"file {filename} does not exist")
            return None

    def get_azure_profile(env:str=None):
        dft_filename = f'./config/azure_profile.json'
        if not env is None:
            filename = f'./config/azure_profile_{env}.json'
            if not os.path.exists(filename):
                filename = dft_filename
        else:
            filename = dft_filename
        with open(filename, 'r') as f:
            env_dict = json.loads(f.read())
            return env_dict

    def get_azure_creds(env:str=None):
        creds = {}
        filename = f'./config/creds/{env}_creds.json'
        if env is None or not os.path.exists(filename):
            creds['client_id'] = os.environ['AZURE_CLIENT_ID']
            creds['client_secret'] = os.environ['AZURE_CLIENT_SECRET']
            creds['tenant_id'] = os.environ['AZURE_TENANT_ID']
            creds['subscription_id'] = os.environ['AZURE_SUBSCRIPTION_ID']
            return creds
        with open(filename, 'r') as f:
            creds = json.loads(f.read())
            return creds

    def get_azure_environment_config(env='default'):
        filename = f"./config/environments/{env}_config.json"
        try:
            with open(filename, 'r') as f:
                env_config= json.load(f)
                return env_config
        except Exception as e:
            logger.error(f"file {filename} does not exist")
            return None

    def save_environment(env, subscription):
        envs = AzureConfigUtils.get_all_azure_environments()
        envs[env] = subscription
        with open('./config/all_azure_profiles.json', 'w') as f:
            json.dump(envs, f, indent=2)

    def create_missing_env_config(env, profile):
        env_config_file = f"config/environments/{env}_config.json"
        logger.info(f"creating {env_config_file}")
        if profile:
            env_config = {}
            for e in ['client','workload','subscription','vnet','region','vpn_only']:
                if e in profile:
                    env_config[e] = profile[e]
            env_config['env_suffix'] = profile['env']
            env_config['timestamp'] = str(datetime.now())
            logger.info(f"creating env config file: {env_config_file}")
            with open(env_config_file, 'w+') as f:
                json.dump(env_config, f, indent=2)