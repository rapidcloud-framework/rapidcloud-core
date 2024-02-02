#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import logging

from commands import print_utils
from commands.colors import colors
from commands.cli_worker.aws_worker import AwsWorker
from commands.kc_metadata_manager.aws_infra import AwsInfra 
from server import server


class MetadataWorker(AwsWorker):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def run(self):
        if self.args.command == 'show':
            self.show_metadata()
        
        elif self.args.command == 'remove':
            # take latest snapshot before removing
            self.export_metadata()
            self.remove_metadata()

        elif self.args.command == 'export': 
            self.export_metadata()

        elif self.args.command == 'import':
            self.import_metadata()


    def show_metadata(self):
        data = server.get_data(args=self.args)
        table_name = self.args.type if self.args.type else "metadata"
        if table_name == 'metadata':
            cols = ["feature","module","command","name","timestamp","cmd_id"]
        elif table_name == 'aws_infra':
            cols = ["phase","command","resource_name","resource_type","timestamp","cmd_id"]
        print_utils.print_grid_from_json(data, cols=cols)


    # remove all dynamodb data associated with current environment
    def remove_metadata(self):
        if super().prompt("Remove metadata. This doesn't destroy any AWS resources ") == 'yes':
            AwsInfra(self.args).delete_metadata()


    # take metadata snapshot at particular time
    def export_metadata(self):
        if super().prompt("Export metadata for current environment ") == 'yes':
            AwsInfra(self.args).export_metadata()


    # copy snapshot from particular time to another env
    def import_metadata(self):
        source_env = self.args.env
        target_env = self.args.target_env
        if super().prompt(f"Import last metadata snapshot from {source_env} to {target_env}") == 'yes':
            # switch to target env
            setattr(self.args, 'env', target_env)

            # import to target env
            AwsInfra(self.args).import_metadata(source_env, target_env)

            self.logger.info(f"\n\nRun {colors.OKGREEN}kc status{colors.ENDC} to see your imported environment details\n\n")

