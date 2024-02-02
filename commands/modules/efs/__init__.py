__author__ = "Abe Garcia"
__license__ = "MIT"
__email__ = "agarciaortiz"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

import json


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def load_params(self, module, command, args):
        # we will populate this dict and pass it to the command functions
        params = {}
        try:
            # we're pulling all valus from the args object into a dict
            args_dict = vars(args)

            # we then load the actual args from the module's json
            json_args = self.get_module_json("efs")[module][command]['args']

            # now we'll loop over them all
            for arg in json_args.keys():
                params[arg] = args_dict[f"{module}_{arg}"]
                if arg == 'tags' or arg == 'labels' or arg == 'selectors':
                    # convert string to dict here
                    arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                    try:
                        params[arg] = arg_json
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(f"init.py error: {e}")
        return params

    def create(self, metadata=None):
        super().delete_infra_metadata(name=self.args.fs_name)
        params = self.load_params('efs', 'create', self.args)
        resource_name = self.args.fs_name
        resource_type = "aws_efs_file_system"
        super().add_aws_resource(resource_type, resource_name, params)
