#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import logging
import os
import time
import traceback
from os.path import exists

from commands import print_utils
from commands.cli_worker import CliWorker
from commands.colors import colors
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.aws_profile import Profile
from commands.kc_metadata_manager.property import Property


class InitWorker(CliWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.env = super().get_env()


    def verify_env(self):
        # self.logger.info("InitWorker verify_env")
        start_time = time.time()
        if self.args.env is not None:
            env = self.args.env
        elif 'env' in self.config and self.config['env'] != "":
            env = self.config['env']
            setattr(self.args, 'env', env)
        else:
            print(f"You don't have a current environment (verify_env). Run this command:\n{colors.OKBLUE}kc init set-env --env [your_env_name]{colors.ENDC}\n")
            return None

        if hasattr(self.args, 'x_acct_role_arn'):
            self.logger.info(f"InitWorker verify env has x_acct_role_arn {self.args.x_acct_role_arn}")

        print(f"Verifying {self.args.cloud} environment permission for `{env}` ...")
        try:
            profile = self.find_env(env)
            # self.logger.info(f"InitWorker verify_env profile {profile}")
            if profile is None:
                return None

            # make environment info available in args
            setattr(self.args, "env_info", profile)

            created_by = profile["created_by"] if "created_by" in profile else profile["updated_by"]
            print(f" - verify_env(): created_by: {created_by}", end=" ")

            # current user owns the environment
            verified = created_by == self.args.current_session_email
            if not verified and profile.get("shared", False):
                # environment is shared with "all" or current user
                shared_with = profile.get("shared_with", "")
                print(f"({shared_with})", end=" ")
                verified = self.args.current_session_email in shared_with or "all" in shared_with

            if verified:
                if not os.path.exists(f"./config/environments/{env}_config.json"):
                    self.create_missing_env_config(profile)

            duration = f"{round(time.time() - start_time, 2)}s"
            if not verified:
                print(f"{colors.FAIL}you don't have permission to use environment {env}{colors.ENDC} ({duration})")
                self.logger.warning(f"you don't have permission to use environment {env}")
            else:
                print(f"{colors.OKGREEN}ok{colors.ENDC} ({duration})")

            return profile if verified else None

        except Exception as e:
            self.logger.error(f"InitWorker failed to verify env: {env}")
            self.logger.error(e)
            traceback.print_exc()
            return None


    def init(self, profile=None):
        run_deploy_status = False
        if self.args.command == 'create-env':
            self.create_env()
            run_deploy_status = True

        elif self.args.command == 'reset-properties':
            Property(self.args).set_default_properties()

        elif self.args.command == 'load-data-type-mappings' and self.args.cloud == "aws":
            AwsInfra(self.args).load_data_type_mappings()

        elif self.args.command == 'set-property':
            Property(self.args).set_property(self.args.type, self.args.name, self.args.value)

        elif self.args.command == 'list-env':
            profiles = Profile(self.args).get_all_profiles()
            print_utils.print_grid_from_json(profiles, cols=['name','account','vpc','region','created_by','timestamp'])

        elif self.args.command == 'show-env':
            p_copy = copy.deepcopy(profile)
            for k in profile.keys():
                if "_wizard" in k:
                    del p_copy[k]
            self.logger.info(p_copy['name'])
            self.logger.info(json.dumps(p_copy, indent=2, default=str))

        elif self.args.command == 'set-env':
            self.set_env(profile, show_status=False)
            run_deploy_status = True

        elif self.args.command == 'add-ip-addr':
            Profile(self.args).add_ip_addr()

        if run_deploy_status and self.args.cloud == "aws":
            AwsInfra(self.args).show_status()
