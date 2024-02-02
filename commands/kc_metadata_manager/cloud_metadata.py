__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import logging
import os
from datetime import datetime

DO_NOT_SAVE_THESE_ARGS = ['password','feature','command','user','aws_profile','env','datalake','data_lake_fqn','output_folder_path','aws_region','cmd_id','password','api_key','api_secret','secret','modules_dirs','modules_by_cloud']


class CloudMetadata(object):

    logger = logging.getLogger(__name__)

    def __init__(self, args, cloud):
        self.cloud = cloud
        self.args = args
        self.load_cloud_config()
        self.resolve_env()
        self.load_env_config()

    def get_cross_account_roles(self):
        pass
        # self.logger.info(f"CloudMetadata executing get_tenant")
        # if self.args.cloud == "aws":
        #     try:
        #         saas_params = {
        #             "action": "get_tenant",
        #             "email": self.args.current_session_email
        #         }
        #         tenant = LicenseWorker(self.args).contact_lic_server("saas", params=saas_params)
        #         x_acct_roles = tenant.get('x-acct-roles', None)

        #         if x_acct_roles is not None:
        #             self.args.x_acct_role_arn = x_acct_roles[self.args.env]['role']
        #             self.args.region = x_acct_roles[self.args.env]['region']
        #     except Exception as e:
        #         pass

        #     self.args = args
        #     if hasattr(self.args, 'x_acct_role_arn'):
        #         self.logger.info(f"CliWorker has x_acct_role_arn {self.args.x_acct_role_arn}")
        #     elif hasattr(self.args, 'profile'):
        #         self.logger.info(f"CliWorker has profile {self.args.profile}")
        #     else:
        #         self.logger.info("CliWorker DOES NOT have x_acct_role_arn or profile")


        #     try:
        #         self.logger.info("-----------------------------------\n\n")
        #         self.logger.info(f"CliWorker find_env email {self.args.current_session_email}")
        #         self.logger.info(f"CliWorker find_env profile {self.args.profile}")
        #         self.logger.info(f"CliWorker find_env x_acct_role_arn {self.args.x_acct_role_arn}")
        #         self.logger.info("-----------------------------------\n\n")
        #     except Exception as e:
        #         pass

    def load_cloud_config(self):
        self.logger.debug(f"Getting config/{self.cloud}_profile.json")
        self.x_acct_role_arn = None
        self.aws_profile = None
        self.region_name = None

        with open(f'config/{self.cloud}_profile.json') as f:
            self.config = json.load(f)
            self.email = self.config['email']
            if self.cloud == "aws":

                if hasattr(self.args, "aws_profile") and self.args.aws_profile:
                    self.aws_profile = self.args.aws_profile
                    self.region_name = self.args.region
                else:
                    self.aws_profile = self.config.get('aws_profile')
                    self.region_name = self.config.get('default_region')

                self.logger.info(f"load_cloud_config trying to see if there's cross account roles")
                if hasattr(self.args, "x_acct_role_arn") and self.args.x_acct_role_arn:
                    self.logger.info(f"load_cloud_config has x_acct_role_arn")
                    self.x_acct_role_arn = self.args.x_acct_role_arn

            elif self.cloud == "gcp":
                self.region_name = self.config['default_region']
                self.logger.info(f"load_cloud_config: {self.region_name}")
            elif self.cloud == "azure":
                self.logger.info(json.dumps(self.config, indent=2))
                self.region_name = self.config.get('default_region')
                self.logger.info(f"load_cloud_config: {self.region_name}")
            else:
                raise RuntimeError("Unexpected cloud: '{self.cloud}'")


    def resolve_env(self):
        if all(k in self.args for k in ("client","workload","env_suffix","env","feature")) and self.args.client and self.args.workload and self.args.env_suffix:
            self.env = f"{self.args.client}_{self.args.workload}_{self.args.env_suffix}"
        elif hasattr(self.args, 'env') and self.args.env is not None:
            self.env = self.args.env
        elif 'env' in self.get_config():
            self.env = self.config['env']
        elif hasattr(self.args, 'feature') and self.args.feature == 'activate':
            self.env = 'kinect_theia_api'
        else:
            self.env = None
        self.logger.info(f"resolve_env: {self.env}")


    def load_env_config(self):
        with open("config/kc_config.json", 'r') as f:
            self.kc_config = json.load(f)

        config_file = f"config/environments/{self.get_env()}_config.json"
        if not os.path.exists(config_file):
            return

        with open(config_file, 'r') as f:
            self.env_config = json.load(f)
            self.region_name = self.env_config.get('region','?')

            if self.cloud == "aws":
                self.aws_profile = self.env_config.get('aws_profile','?')
                self.logger.info(f"load_env_config: {config_file} ({self.aws_profile}, {self.region_name})")
            elif self.cloud == "azure":
                self.azure_profile = self.env_config.get('azure_profile','?')
                self.logger.info(f"load_env_config: {config_file} ({self.azure_profile}, {self.region_name})")
            elif self.cloud == "gcp":
                self.logger.info(f"load_env_config: {config_file} ({self.region_name})")
            else:
                raise RuntimeError(f"Unexpected cloud provider: '{self.args.cloud}'")

        pass # Placeholder to allow a potential debugger breakpoint


    def get_metadata_fqn(self, module: str, command: str, name: str) -> str:
        env = self.get_env()
        assert env,     "self.get_env() cannot be null."
        assert module,  "Method param 'module' cannot be null."
        assert command, "Method param 'command' cannot be null." # Can this be None?
        assert name,    "Method param 'name' cannot be null."
        fqn = f"{env}_{module}_{command}_{name}"
        return fqn


    # Builds the object in memory. Subclass should extend this method to save the object to database.
    def build_metadata_item(self, metadata, name=None, args={}):
        self.logger.info("building metadata ...")

        module = self.args.module if self.args.module is not None else self.args.feature
        command = self.args.command if self.args.command else "none"
        name = self.args.name if self.args.name else metadata["id"] if "id" in metadata else "default"
        fqn = metadata['fqn'] if "fqn" in metadata else self.get_metadata_fqn(module, command, name)

        for arg in args.values():
            if 'type' in arg:
                arg_name = f"{module}_{arg['name']}"
                if arg['type'] == "secret":
                    secret_type = module
                    if 'secret_type' in arg:
                        secret_type = arg['secret_type']
                    secret_name = arg['name']
                    if 'secret_name' in arg:
                        secret_name = metadata[arg['secret_name']]
                    if 'ignore_env_prefix' in arg and arg['ignore_env_prefix']:
                        secret_name = f"{secret_type}/{secret_name}"
                    else:
                        secret_name = f"{self.get_env()}/{secret_type}/{secret_name}"
                    metadata[arg_name] = secret_name
                elif arg['type'] == "boolean":
                    metadata[arg_name] = str(metadata[arg_name]).lower() in ["true", "yes"]
                elif arg['type'] == "json":
                    metadata[arg_name] = json.loads(metadata[arg_name].replace("\\",""))

        item = {
            "fqn": fqn,
            "id": fqn,
            "module": module,
            "command": self.args.command,
            "name": name,
            "timestamp": str(datetime.now()),
            "params": metadata
        }

        _selected = []
        if self.args.dyn_args and 'args' in self.args.dyn_args:
            dyn_args = self.args.dyn_args['args']
            for arg, value in dyn_args.items():
                if arg not in metadata:
                    # set boolean values
                    if value is not None and value == "true":
                        item[arg] = True
                    elif value is not None and value == "false":
                        item[arg] = False
                    else:
                        item[arg] = value

                    # check "_selected"
                    if "_selected" in arg:
                        arg_ = arg.replace("_selected","")
                        if arg_ not in dyn_args or dyn_args[arg_] == "":
                            _selected.append((arg_, value))

        # set selected
        # self.logger.info(_selected)
        for arg in _selected:
            item[arg[0]] = arg[1]

        item["params"] = dict(sorted(item["params"].items(), key=lambda item: item[0]))

        if hasattr(self.args, 'cmd_id'):
            item['cmd_id'] = self.args.cmd_id

        item['profile'] = self.get_env()

        if 'module' not in item:
            item['module'] = self.args.module

        self.logger.info(json.dumps(item, indent=2, default=str))
        return item


    def build_infra_item(self, type, name, params={}, name_separator="_", custom=False, role_name=None, fqn=None):
        if not fqn:
            fqn = self.get_env() + '_' + type + '_' + name

        # only keep non-null arguments and those not in DO_NOT_SAVE_THESE_ARGS list
        command_args = {}
        for arg, value in vars(self.args).items():
            if value is not None and arg not in DO_NOT_SAVE_THESE_ARGS:
                command_args[arg] = value

        # full module name (if applicable)
        module_name = None
        if self.args.module:
            module_name = self.args.module
        elif self.args.phase:
            module_name = self.args.phase
        elif self.args.feature:
            module_name = self.args.feature
        command = self.args.command if self.args.command else "none"
        name_arg = self.args.name if self.args.name else "none"
        module = f"{module_name}_{command}_{name_arg}"

        # RapidCloud naming convention
        rc_resource_name = f"{self.get_env()}_{name.replace('_',name_separator)}_{type}"

        item={
            'fqn': fqn,
            'id': fqn,
            'profile': self.get_env(),
            'resource_type': type,
            'resource_name': name.replace('_',name_separator),
            'override_name': False,
            'custom': custom,
            'params': params,
            'status': 'active',
            'phase': module_name,
            'command': command,
            'module': module,
            'command_arguments': command_args,
            'timestamp': str(datetime.now()),
        }
        if hasattr(self.args, 'cmd_id'):
            item['cmd_id'] = self.args.cmd_id

        if role_name is None or role_name == "":
            role_name = self.get_role(item)
        if role_name is not None and role_name != "":
            item['params']['role_name'] = role_name

        return item


    def build_history_item(self):
        if self.args.feature not in ['activate'] and not hasattr(self.args, 'command_history_saved'):
            try:
                caller_arn = self.session.client('sts').get_caller_identity()['Arn']
                setattr(self.args, "caller_arn", caller_arn)
                self.args.user = caller_arn
                self.logger.debug(f"caller_arn: {caller_arn}")

                # only keep non-null arguments and those not in DO_NOT_SAVE_THESE_ARGS list
                command_args = {}
                for arg, value in vars(self.args).items():
                    if value is not None and arg not in DO_NOT_SAVE_THESE_ARGS:
                        command_args[arg] = value

                cmd_timestamp = datetime.now()
                cmd_id = str(cmd_timestamp).replace('-','').replace(':','').replace(' ','').replace('.','')
                item = {
                    'timestamp': str(cmd_timestamp),
                    'id': cmd_id,
                    'profile': self.get_env(),
                    'phase': self.args.feature,
                    'command': self.args.command,
                    'user': caller_arn,
                    'command_arguments': command_args,
                }
                self.logger.debug(json.dumps(item, indent=2, default=str))
                return item
            except Exception as e:
                self.logger.error(e)
        return None


    def json_converter(self, obj):
        return str(obj)

    def get_region(self):
        if not hasattr(self, "region_name") or self.region_name is None or (hasattr(self.args, "feature") and self.args.feature == "activate"):
            self.load_cloud_config()
        return self.region_name

    def get_kc_config(self):
        return self.kc_config

    def get_aws_profile(self):
        return self.aws_profile

    def get_env_config(self):
        return self.env_config

    def get_config(self):
        # TODO need to start using auth0 login info
        if not hasattr(self, "config") or self.config is None:
            self.load_cloud_config()
        return self.config

    def get_separator(self):
        return self.SEPARATOR

    def get_args(self):
        return self.args

    def get_env(self):
        if not hasattr(self, "env") or self.env is None:
            self.resolve_env()
        return self.env

    def get_mode(self):
        if type(self.args) == dict:
            return self.args.get("mode", "console")
        else:
            return self.args.mode

    def put_item(self, table: str, item: dict) -> None:
        pass

    def get_module_json(self, module_name):
        module_json_file = self.args.modules_dirs[self.args.cloud].get(module_name) + "/module.json"
        if os.path.exists(module_json_file):
            with open(module_json_file) as f:
                return json.load(f)

    def show_status(self):
        pass

    def exec_tf_action(self, action, subscription_tier, no_prompt):
        pass
