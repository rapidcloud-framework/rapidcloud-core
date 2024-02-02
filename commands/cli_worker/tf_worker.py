#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging
import os
import subprocess
from commands.cli_worker import CliWorker
from commands.cli_worker.provider import Provider

class TfWorker(CliWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def tf(self):

        if self.args.command == 'init':
            self.tf_action(self.args.command)

        elif self.args.command == 'plan':
            self.tf_action(self.args.command)

        elif self.args.command == 'apply':
            if super().prompt(f"Deploy {self.args.cloud} resources") == 'yes':
                self.tf_action(self.args.command)

        elif self.args.command == 'destroy':
            if super().prompt(f"Destroy {self.args.cloud} resources") == 'yes':
                self.tf_action(self.args.command)

        elif self.args.command == 'version':
            proc = subprocess.run("terraform -v", shell=True, check=True, env=os.environ.copy())
            print(proc)

    
    # ------------------------------------------------------------------------------------
    # Plan/Deploy/destroy Infrastructure via Terraform 
    #   --action [init|plan|apply|destroy]
    # ------------------------------------------------------------------------------------
    def tf_action(self, action):

        no_prompt = self.args.mode == "console" or hasattr(self.args, 'no_prompt')
        subscription_tier = self.args.verification["tier"] if "tier" in self.args.verification else "1"

        Provider(self.args).get_infra().exec_tf_action(action, subscription_tier, no_prompt=no_prompt)
