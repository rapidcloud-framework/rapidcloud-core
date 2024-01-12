__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import glob
import importlib
import json
import logging
import os
import sys
from collections import OrderedDict
from os.path import exists

from commands import print_utils
from commands.colors import colors
from commands.modules import cli_argument_utils

logger = logging.getLogger("module")

class Module(object):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        self.args = args
        self.imported_modules = {}
        self.cmd = ""

        with open('./config/version.json', 'r') as f1:
            self.version = json.load(f1)['version']

        if self.args.module != "module" and self.args.module_command != "create":
            with open(f'./config/environments/{self.args.env}_config.json', 'r') as f2:
                self.env_config = json.load(f2)


    def exec(self, metadata):
        if not self.args.module_command:
            setattr(self.args, "module_command", self.args.command)

        self.load_imported_modules()

        self.cmd = f"kc {self.args.module} {self.args.module_command} "
        logger.info(self.cmd)
        logger.info(f"\n\n{colors.OKGREEN}{self.config['help']}{colors.ENDC}")
        curr_values = {}

        # check if existing metadata already exists and set current values
        id_name = None
        if 'id' in self.config:
            logger.info(f"\n\nMain parameters:\n")
            id_name = self.config['id']
            prompt_info = self.config["args"][id_name]
            prompt_info['curr_value'] = ""
            id_value = cli_argument_utils.get_user_input(self.args, id_name, prompt_info)
            setattr(self.args, id_name, id_value)
            fq_id_name = f"{self.args.module}_{id_name}"
            setattr(self.args, fq_id_name, id_value)

            # Retrieve previously saved data (if any) from the 'metadata' db table corresponding to
            # these params in order to populate the default answer for the upcoming call to cli_argument_utils.get_user_input().
            result = metadata.get_modules(self.args.module, self.args.module_command, id_value)

            curr_values = {}
            if len(result) == 0:
                # creating new module
                curr_values = {
                    "id": id_value,
                    id_name: id_value,
                    fq_id_name: id_value
                }
            elif 'immutable' in self.config and self.config['immutable']:
                logger.warning(f"`{self.args.module}` module with name `{id_value}` already exists. Modules is immutable")
                return
            else:
                # updating existing module
                curr_values = result[0]

            if "params" in curr_values:
                # flatten params
                curr_values.update(curr_values["params"])
                curr_values.pop("params")

            self.cmd += f"--{id_name} \"{id_value}\" --{fq_id_name} \"{id_value}\" "

        # collect module arguments
        if "args" in self.config:
            for arg, info in self.config["args"].items():
                if not id_name or arg != id_name:
                    fq_arg = f"{self.args.module}_{arg}"
                    if arg in curr_values:
                        info['curr_value'] = curr_values[arg]
                    elif fq_arg in curr_values:
                        info['curr_value'] = curr_values[fq_arg]
                    else:
                        if "default" in info and "dynamic-config" in str(info['default']):
                            info['curr_value'] = self.env_config[info['default'].split("::")[-1]]
                            print(info['curr_value'])
                        else:
                            info['curr_value'] = info.get('default', '')
                    user_input = cli_argument_utils.get_user_input(self.args, arg, info)
                    value = user_input if user_input is not None else info.get('default', '')
                    curr_values[fq_arg] = value
                    setattr(self.args, fq_arg, value)
                    info[fq_arg] = value
                    self.cmd += f"--{fq_arg} \"{value}\" "

        # collect imported modules arguments
        for i_name, i_module in self.imported_modules.items():
            print(f"\n\n{colors.OKGREEN}Imported module `{i_name}`{colors.ENDC}\n")
            imported_module = i_name.split(".")[0]
            imported_cmd = i_name.split(".")[1]
            if "args" not in i_module[imported_cmd]:
                i_module[imported_cmd]["args"] = {}
            i_args = i_module[imported_cmd]["args"]
            i_enabled_values = {
                "name": f"Enable {imported_module.upper()}",
                "prompt": f"Enable {imported_module.upper()} (yes|no)",
                "required": True,
                "default": "no"
            }

            # collect imported module enabled flag
            value = self.collect_imported_arg(imported_module, "enabled", i_enabled_values, curr_values)
            print(f"imported module {imported_module} enabled: {value}\n")
            if value.lower() in ["yes", "true"]:
                self.imported_modules[i_name]['enabled'] = True
                for arg, info in i_args.items():
                    if "min_version" in info:
                        if "beta" in self.version or info['min_version'] > self.version:
                            continue
                    self.collect_imported_arg(imported_module, arg, info, curr_values)
            else:
                self.imported_modules[i_name]['enabled'] = False

        # Complete RapidCloud command
        print(f"\n\nCommmand:")
        print(f"\n{colors.OKBLUE}{self.cmd} --no-prompt{colors.ENDC}\n\n")

        # create/update metadata
        module_args = {}
        if 'args' in self.config:
            module_args = self.config['args']
        if 'fqn' in self.config:
            fqn = self.args.env + "_" + self.args.module
            for col in self.config['fqn'].split(','):
                if "'" not in col:
                    col_value = curr_values[f"{self.args.module}_{col}"]
                    if col_value:
                        fqn = fqn + "_" + col_value
                    else:
                        fqn = fqn + "_"
                else:
                    fqn = fqn + "_" + col.replace("'", "")
            curr_values['fqn'] = fqn
            logger.info(f"fqn: {fqn}")

        save_metadata = 'metadata_table' in self.config
        metadata_table = self.config['metadata_table'] if 'metadata_table' in self.config else None
        # logger.info(json.dumps(curr_values, indent=2))
        metadata_item = metadata.build_metadata_item(curr_values, metadata_table, args=module_args, save=save_metadata)

        # execute command logic
        if hasattr(metadata, self.args.module_command) and callable(getattr(metadata, self.args.module_command)):
            setattr(self.args, "composite_module", False)
            logger.info(f"executing command [{self.args.module}.{self.args.module_command}]")
            func = getattr(metadata, self.args.module_command.replace('-','_'))
            func(metadata=metadata_item)

            # this ensures metadata is not deleted when executing imported modules
            if self.imported_modules:
                setattr(self.args, "composite_module", True)

            # execute imported modules
            for i_name, i_module in self.imported_modules.items():
                if i_module['enabled']:
                    imported_module = i_name.split(".")[0]
                    imported_cmd = i_name.split(".")[1]
                    self.exec_imported_module(imported_module, imported_cmd, metadata_item)

        pass # Placeholder to allow a potential debugger breakpoint

    def get_module_json(self, module_name):
        dir_name = self.args.modules_dirs[self.args.cloud][module_name]
        file_name = f"{dir_name}/module.json"
        if exists(file_name):
            # logger.info(file_name)
            with open(file_name) as f:
                return json.load(f)[module_name]
        else:
            logger.error(f"{file_name} is not found")
        return None


    def load_imported_modules(self):
        module_json = self.get_module_json(self.args.module)
        if module_json:
            if self.args.module_command in module_json:
                self.config = module_json[self.args.module_command]
            else:
                self.config = {}
            if 'import_modules' in self.config:
                for imported in self.config['import_modules'].split(","):
                    imported_module_json = self.get_module_json(imported.split(".")[0])
                    if imported_module_json:
                        self.imported_modules[imported] = imported_module_json


    def collect_imported_arg(self, imported_module, arg, info, curr_values):
        info['curr_value'] = curr_values[arg] if arg in curr_values else info['default']
        value = cli_argument_utils.get_user_input(self.args, arg, info, imported_module=imported_module)
        fq_arg = f"{imported_module}_{arg}"
        curr_values[fq_arg] = value
        setattr(self.args, fq_arg, value)
        info[fq_arg] = value
        # print(f"--{fq_arg} \"{value}\" ")
        self.cmd += f"--{fq_arg} \"{value}\" "
        return value


    def exec_imported_module(self, imported_module, imported_cmd, metadata_item):
        module = get_module(self.args, imported_module)
        if module is not None:
            module_instance = module.ModuleMetadata(self.args)
            logger.info(f"executing command [{imported_module} {imported_cmd}]")
            func = getattr(module_instance, imported_cmd)
            metadata_item["composite_module"] = True
            func(metadata=metadata_item)


def get_module_json_dirs(skip_bundled=False):
    modules_jsons = []

    CUSTOM_MODULE_HOME_DIR = "./commands/modules"

    with open('./config/modules_config.json', 'r') as f:
        modules_config = json.load(f)
        CUSTOM_MODULES_PROJECT_DIR = modules_config["modules_parent_dir"]

    # multi-repo custom modules
    if os.path.exists(CUSTOM_MODULES_PROJECT_DIR):
        modules_jsons.append(f"{os.path.abspath(CUSTOM_MODULES_PROJECT_DIR)}/*/{CUSTOM_MODULE_HOME_DIR}/*/module.json")

    # for bundle also collect custom modules from local file system
    home_dir = getattr(sys, '_MEIPASS', os.getcwd())
    if '_MEI' in home_dir:
        modules_jsons.append(f'{CUSTOM_MODULE_HOME_DIR}/*/module.json')

    # bundled modules (or main repo in dev mode)
    if not skip_bundled or '_MEI' not in home_dir:
        modules_jsons.append(f'{home_dir}/{CUSTOM_MODULE_HOME_DIR}/*/module.json')

    return modules_jsons


# load modules info
def load_modules(skip_bundled=False):
    logger.debug("loading modules ...")
    modules_jsons = get_module_json_dirs(skip_bundled)
    print_utils.info("\nmodules_jsons=\n{}".format(json.dumps(modules_jsons, indent=2)))

    modules_by_cloud = {
        "aws": {},
        "azure": {},
        "gcp": {}
    }
    modules_dirs = copy.deepcopy(modules_by_cloud)
    add_args_list = []

    logger.debug(f"Initial/empty modules_dirs={modules_dirs}")
    for modules_dir in modules_jsons:
        # print_utils.info(f"\nmodules_dir: {modules_dir}")
        for file_name in glob.glob(modules_dir, recursive=True):
            # print(f"\tfile_name: {file_name}")
            file_name = file_name.replace("\\","/") # fixes windows issue
            module_name = file_name.split("/")[-2]
            # print(f"\trepo: {repo_name}")
            if module_name == "skeleton":
                continue
            add_args_list.append(f"module_{module_name}")
            with open(file_name) as f:
                filesize = os.path.getsize(file_name)
                if filesize > 0:
                    module_config = json.load(f)
                    for feature, commands in module_config.items():
                        # print_utils.info(f"\t\tmodule: {feature}")
                        for cmd, cmd_config in commands.items():
                            c = cmd_config.get("cloud", "aws")

                            for module_cloud in modules_by_cloud:
                                if c == module_cloud or c == "general":
                                    # print(f"\t\t\tcmd: {cmd}")
                                    if feature not in modules_by_cloud[module_cloud]:
                                        modules_by_cloud[module_cloud][feature] = {}
                                        modules_dirs[module_cloud][feature] = file_name.replace("/module.json","")

                                    if cmd in modules_by_cloud[module_cloud][feature]:
                                        # print(f"already got {feature}.{cmd}")
                                        continue # already got this module from custom modules

                                    cached_config = {
                                        "enabled": cmd_config.get("enabled", False),
                                        "template_enabled": cmd_config.get("template_enabled", False),
                                        "template_section": cmd_config.get("template_section", ""),
                                        f"create_{module_cloud}_infra": cmd_config.get(f"create_{module_cloud}_infra", False)
                                    }
                                    modules_by_cloud[module_cloud][feature][cmd] = cached_config
                                    # add fully qualified arg names
                                    if 'args' in cmd_config:
                                        for cmd_arg in cmd_config['args'].keys():
                                            add_args_list.append(f"{module_name}_{cmd_arg}")
                                    if 'import_modules' in cmd_config:
                                        for i_module in cmd_config['import_modules'].split(","):
                                            add_args_list.append(f"{i_module.split('.')[0]}_enabled")

    copy_dict = copy.deepcopy(modules_dirs)
    for cloud, modules in copy_dict.items():
        modules_dirs[cloud] = OrderedDict(sorted(modules.items()))

    # print_utils.info(json.dumps(modules, indent=2))
    # print_utils.info(json.dumps(add_args_list, indent=2))
    print_utils.info("\nMODULE DIRS:")
    print_utils.info(json.dumps(modules_dirs, indent=2))
    return modules_by_cloud, modules_dirs, add_args_list


# get module
def get_module(args, module_name):
    module = None
    try:
        module_dir = args.modules_dirs[args.cloud][module_name]
        if '_MEI' in module_dir:
            logger.info(f"loading native module [{module_name}]")
            module = importlib.import_module(f"commands.modules.{module_name}")
        else:
            file_path = f"{module_dir}/__init__.py"
            if os.path.exists(file_path):
                logger.info(f"loading custom module [{module_name}] from '{file_path}'")
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
            else:
                logger.error(f"module {module_name} in {file_path} is not found")
    except Exception as e:
        logger.error(f"module {module_name} is not loaded: {e}")
    return module


# execute module
def exec_module(args, module_name=None, command=None):
    if module_name is None:
        module_name = args.feature
    else:
        setattr(args, "module", module_name)

    if command is not None:
        setattr(args, "module_command", command)

    module = get_module(args, module_name)
    if module is not None:
        metadata_instance = module.ModuleMetadata(args)
        Module(args).exec(metadata_instance)


def pause(args):
    if args.pause:
        input(f"\n{colors.OKBLUE}Execution is paused. Click enter to continue, ctrl-c to exit{colors.ENDC}\n")
