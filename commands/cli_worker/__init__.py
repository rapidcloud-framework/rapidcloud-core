__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import socket
from datetime import datetime

from commands.colors import colors
from commands.general_utils import load_json_file


class CliWorker(object):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args
        self.config = load_json_file(f'config/{self.args.cloud}_profile.json', f'config/{self.args.cloud}_default_profile.json')
        pass  # Placeholder to allow a potential debugger breakpoint

    def get_config(self):
        return self.config


    def get_env(self):
        # self.logger.info(f"InitWorker get env")
        if hasattr(self.args, 'env'):
            return self.args.env
        elif 'env' in self.config:
            return self.config['env']

    def json_converter(self, obj):
        return str(obj)

    def create_missing_env_config(self, profile):
        self.logger.info(f"InitWorker create_missing_env_config")
        env_config_file = f"config/environments/{self.args.env}_config.json"
        self.logger.info(f"creating {env_config_file}")
        if profile:
            env_config = {}
            for e in ['client','workload','account','subscription','vpc','vnet','region','ssh_pub_key','vpn_only','aws_profile', 'x_acct_role_arn']:
                if e in profile:
                    env_config[e] = profile[e]
            env_config['env_suffix'] = profile['env']
            env_config['timestamp'] = str(datetime.now())
            self.logger.info(f"creating env config file: {env_config_file}")
            with open(env_config_file, 'w') as f:
                json.dump(env_config, f, indent=2)


    def show_kc_status(self, print_files=True):
        self.logger.info(f"InitWorker show_kc_status")
        config = self.get_json_file(f"config/{self.args.cloud}_profile.json", print_files)
        if 'env' in config:
            print("---------------------------------------------------------------")
            print(f"{colors.OKGREEN}Current active environment is [{config['env']}]:{colors.ENDC}")
            self.get_json_file(f"config/environments/{config['env']}_config.json", print_files)
            print(f"\nTo switch to another environment run:\n\n{colors.FAIL}kc init set-env --env <name_of_env>{colors.ENDC}\n")
            print(f"To start RapidCloud Console:\n\n{colors.FAIL}kc --console{colors.ENDC}\n")
            print(f"To show help:\n\n{colors.FAIL}kc help{colors.ENDC}\n")
            print(f"To show module specific help:\n\n{colors.FAIL}kc help <module>{colors.ENDC} (e.g. `kc help ec2`)\n")
        elif 'email' in config:
            print(f"\nYou don't have an active environment.\n\nTo create a new environment run:\n\n\t{colors.FAIL}kc init create-env{colors.ENDC}")
            print(f"To set active environment run:\n\n\t{colors.FAIL}kc init set-env --env <name_of_env>{colors.ENDC}\n")
        else:
            print(f"\nYour instance of RapidCloud is not activated yet")
            print(f"To activate RapidCloud run:\n\n\t{colors.FAIL}kc activate{colors.ENDC}\n\n")


    def get_user_input(self, prompt_info):
        if len(prompt_info) == 6:
            (arg, name, prompt, curr_value, required, force_naming) = prompt_info
        else:
            (arg, name, prompt, curr_value, required) = prompt_info
            force_naming = False

        # Console mode
        if self.args.mode == 'console' or self.args.no_prompt:
            if hasattr(self.args, arg):
                return getattr(self.args, arg)
            else:
                return ""

        # CLI mode
        value = input(f"{colors.OKBLUE}{prompt}{colors.ENDC} [{curr_value}]: ")
        if required:
            while value == '' and (curr_value == '' or curr_value == 'none'):
                value = input(f"{colors.WARNING}{name} is required:{colors.ENDC} ")
        if value == '':
            value = curr_value

        if force_naming:
            old_value = value
            value = value.replace('-','').replace(' ','').lower()
            if old_value != value:
                print(f"value provided changed to: {value}")
        return value


    def get_json_file(self, file, print_file=True):
        with open(file, 'r') as f:
            filesize = os.path.getsize(file)
            if filesize > 0:
                config = json.load(f)
                if print_file:
                    print("---------------------------------------------------------------")
                    print(f"{colors.OKBLUE}{file}{colors.ENDC}")
                    print("---------------------------------------------------------------")
                    print(f"{json.dumps(config, indent=2)}\n")
                return config


    def prompt(self, msg):
        if self.args.no_prompt or self.args.mode == 'console':
            return "yes"
        else:
            return input(f"{colors.OKBLUE}{msg} [curent env: {self.get_env()}] (yes|no):{colors.ENDC} ")


    def get_hostname(self):
        try:
            return socket.gethostname()
        except:
            try:
                return socket.getfqdn()
            except:
                return "localhost"


    def get_ipaddr(self):
        try:
            return socket.gethostbyname(self.get_hostname())
        except:
            return "localhost"
