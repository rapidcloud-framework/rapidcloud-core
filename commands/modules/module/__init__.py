__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
from datetime import datetime
import json
import shutil
import os
import sys
from zipfile import ZipFile
from os.path import exists

from commands import general_utils, print_utils
from commands.colors import colors
from commands.modules import load_modules
from commands.kc_metadata_manager.cloud_metadata import CloudMetadata
from commands.kc_metadata_manager.aws_metadata import Metadata as AwsMetadata
from commands.kc_metadata_manager.azure_metadata import Metadata as AzureMetadata
from commands.kc_metadata_manager.gcp_metadata import Metadata as GcpMetadata


CUSTOM_MODULE_HOME_DIR = "./commands/modules"
with open('./config/modules_config.json', 'r') as f:
    modules_config = json.load(f)
    CUSTOM_MODULES_PROJECT_DIR = modules_config["modules_parent_dir"]

MODULE_PLACEHOLDER = "MODULE_NAME_PLACEHOLDER"
COMMAND_PLACEHOLDER = "COMMAND_NAME_PLACEHOLDER"
AUTHOR_PLACEHOLDER = "AUTHOR_PLACEHOLDER"

IMPORTED_MODULE_TOGGLE = {
    "type": "Theia::Control::Select",
    "id": "_enabled",
    "label": "",
    "help": "",
    "default": "no",
    "options": [
        {
            "type": "Theia::Option",
            "label": "No",
            "value": {
                "type": "Theia::DataOption",
                "value": "no",
                "disableControls": [
                ]
            }
        },
        {
            "type": "Theia::Option",
            "label": "Yes",
            "value": {
                "type": "Theia::DataOption",
                "value": "yes",
                "enableControls": [
                ]
            }
        }
    ]
}


class ModuleMetadata(CloudMetadata):

    def __init__(self, args):
        self.args = args
        cloud_context_file = "config/cloud_context.json"
        with open(cloud_context_file) as f:
            self.cloud_context = json.load(f)
        super().__init__(args, self.cloud_context["cloud"])

    def get_modules(self, module=None, command=None, name=None):
        cloud_provider = self.cloud_context["cloud"]
        if cloud_provider == "aws":
            return AwsMetadata(self.args).get_modules(module, command, name)
        elif cloud_provider == "azure":
            return AzureMetadata(self.args).get_modules(module, command, name)
        elif cloud_provider == "gcp":
            return GcpMetadata(self.args).get_modules(module, command, name)
        else:
            raise RuntimeError(f"Unexpected cloud provider: '{cloud_provider}'")

    def build_metadata_item(self, metadata, metadata_table, name=None, args={}, save=True):
        cloud_provider = self.cloud_context["cloud"]
        if cloud_provider == "aws":
            return AwsMetadata(self.args).build_metadata_item(metadata, metadata_table, name, args, save)
        elif cloud_provider == "azure":
            return AzureMetadata(self.args).build_metadata_item(metadata, metadata_table, name, args, save)
        elif cloud_provider == "gcp":
            return GcpMetadata(self.args).build_metadata_item(metadata, metadata_table, name, args, save)
        else:
            raise RuntimeError(f"Unexpected cloud provider: '{cloud_provider}'")

    def module_exists(self, module_name):
        dirs = [
            f"{CUSTOM_MODULES_PROJECT_DIR}/{module_name}",
            f"{CUSTOM_MODULE_HOME_DIR}/{module_name}"
        ]
        home_dir = getattr(sys, '_MEIPASS', os.getcwd())
        if '_MEI' in home_dir:
            dirs.append(f'{home_dir}/{CUSTOM_MODULE_HOME_DIR}/{module_name}')

        for module_dir in dirs:
            if os.path.isdir(module_dir):
                print(module_dir)
                return True
        return False


    def create(self, metadata=None):
        if self.module_exists(self.args.name):
            print(f"\n{colors.FAIL}Module `{self.args.name}` already exists{colors.ENDC}\n")
            return

        is_custom_module = general_utils.get_app_mode() == "live"

        # scaffolding dir
        skeleton_module_dir = f"{CUSTOM_MODULE_HOME_DIR}/skeleton"

        # create module files
        module_repo_dir = self.args.module_repo_dir
        try:
            shutil.copytree(f"{skeleton_module_dir}/repo", module_repo_dir)
            self.logger.info(f"created `{self.args.name}` module skeleton in {module_repo_dir}")
        except Exception as e:
            self.logger.warning(f"{module_repo_dir} already exists")

        new_module_dir = f"{module_repo_dir}/commands/modules/{self.args.name}"
        try:
            self.logger.info(f" creating {new_module_dir}")
            os.makedirs(new_module_dir)
            os.mkdir(f"{new_module_dir}/console")
        except Exception as e:
            self.logger.error(e)

        # README.md
        shutil.copy2(f"{skeleton_module_dir}/README.md", f"{new_module_dir}/README.md")

        # module.json
        with open(f"{skeleton_module_dir}/module.json", "r") as f:
            module_json = f.read()
            module_json = module_json.replace(MODULE_PLACEHOLDER, self.args.name)
            module_json = module_json.replace(COMMAND_PLACEHOLDER, self.args.module_action)
            module_json = json.loads(module_json)
            module_json[self.args.name][self.args.module_action]["cloud"] = self.args.module_cloud
            with open(f"{new_module_dir}/module.json", 'w') as module_json_file:
                json.dump(module_json, module_json_file, indent=2)

        # template_module_{}.json
        with open(f"{skeleton_module_dir}/template_module_.json", "r") as f:
            template_json = f.read()
            template_json = template_json.replace(MODULE_PLACEHOLDER, self.args.name)
            template_json = template_json.replace(COMMAND_PLACEHOLDER, self.args.module_action)
            template_name = f"template_{self.args.name}_{self.args.module_action}.json"
            with open(f"{new_module_dir}/console/{template_name}", 'w') as template_json_file:
                template_json_file.write(template_json)

        # template_module_{}.md
        skeleton_md_file = f"{skeleton_module_dir}/template_module_.md"
        if os.path.isfile(skeleton_md_file):
            md_name = f"template_{self.args.name}_{self.args.module_action}.md"
            shutil.copy2(skeleton_md_file, f"{new_module_dir}/console/{md_name}")

        # __init__.py
        cloud_skeleton_init_py = f"{self.args.module_cloud}__init__.py"
        with open(f"{skeleton_module_dir}/{cloud_skeleton_init_py}", "r") as f:
            init_py = f.read()
            author = f"__author__ = \"{super().get_config()['email']}\""
            init_py = init_py.replace(AUTHOR_PLACEHOLDER, author)
            init_py = init_py.replace(COMMAND_PLACEHOLDER, self.args.module_action)
            with open(f"{new_module_dir}/__init__.py", 'w') as init_py_file:
                init_py_file.write(init_py)

        # mark as custom
        if is_custom_module:
            with open(f"{new_module_dir}/.custom", 'w') as custom_flag:
                custom_flag.write("yes")

        # instructions
        self.print_instructions(self.args.name, self.args.module_action)


    def print_instructions(self, custom_module_name, custom_command):
        print(f"""
        {colors.OKBLUE}You have successfully created a new custom RapidCloud Module{colors.ENDC}

        You can invoke this command via RapidCLoud CLI as:
        `{colors.OKGREEN}kc {custom_module_name} {custom_command}{colors.ENDC}`

        Add/modify module functionality here: {colors.OKBLUE}{CUSTOM_MODULE_HOME_DIR}/{custom_module_name}{colors.ENDC}
            Module configuration: {colors.OKBLUE}{CUSTOM_MODULE_HOME_DIR}/{custom_module_name}/module.json{colors.ENDC}
            Module Python Script: {colors.OKBLUE}{CUSTOM_MODULE_HOME_DIR}/{custom_module_name}/__init__.py{colors.ENDC}
            Module Console Templates: {colors.OKBLUE}{CUSTOM_MODULE_HOME_DIR}/{custom_module_name}/console{colors.ENDC}

        RapidCloud includes a comprehensive set of Terraform automation features,
        but you can always add your own custom Terraform scripts here: {colors.OKBLUE}./terraform/modules{colors.ENDC}

        See Complete Custom Modules Documentation here:
        {colors.OKBLUE}https://rapid-cloud.s3.amazonaws.com/docs/RapidCloud-Custom-Modules.html{colors.ENDC}

        """)


    def add_command(self, metadata=None):
        if "mode" in metadata and metadata["mode"] == "console":
            module_name = metadata["module_name"]
            command_name = metadata["module_action"]
        else:
            module_name = self.args.module_module_name
            command_name = self.args.module_command_name

        skeleton_module_dir = f"{CUSTOM_MODULE_HOME_DIR}/skeleton"
        module_dir = self.args.modules_dirs[self.args.module_cloud][module_name]
        # module_dir = f"{CUSTOM_MODULE_HOME_DIR}/{module_name}"

        # module.json
        module_json_file = f"{module_dir}/module.json"
        with open(module_json_file, "r") as f:
            module_json = json.load(f)

            # check if command already exists
            command_exists = False
            if command_name in module_json[module_name]:
                print(f"\n{colors.FAIL}Command `kc {module_name} {command_name}` already exists{colors.ENDC}\n")
                command_exists = True
                # update command
                module_json[module_name][command_name].update({
                    "cloud": self.args.module_cloud,
                    "enabled": metadata.get("enabled", False),
                    "help": metadata.get("help", ""),
                    "template_section": metadata.get("template_section", ""),
                    "template_enabled": metadata.get("template_enabled", False),
                })
                if "id_arg" in metadata:
                    module_json[module_name][command_name]["id"] = metadata["id_arg"]
                if "args" in metadata:
                    args = json.loads(metadata["args"].replace("\n"," "))
                    module_json[module_name][command_name]["args"] = args
            else:
                # create command
                module_json[module_name][command_name] = {
                    "cloud": self.args.module_cloud,
                    "enabled": False,
                    "help": "",
                    "template_section": "",
                    "template_enabled": False,
                }

            module_json[module_name][command_name]["timestamp"] = str(datetime.now())
            module_json[module_name][command_name]["cmd_id"] = metadata["cmd_id"]

            with open(module_json_file, 'w') as f:
                json.dump(module_json, f, indent=2)

        # exit if command already exists
        if command_exists:
            return

        # add template_module_{}.json
        with open(f"{skeleton_module_dir}/template_module_.json", "r") as f:
            template_json = f.read().replace(MODULE_PLACEHOLDER, module_name).replace(COMMAND_PLACEHOLDER, command_name)
            template_name = f"template_{module_name}_{command_name}.json"
            with open(f"{module_dir}/console/{template_name}", 'w') as template_json_file:
                template_json_file.write(template_json)

        # add template_module_{}.md
        skeleton_md_file = f"{skeleton_module_dir}/template_module_.md"
        if os.path.isfile(skeleton_md_file):
            md_name = f"template_{module_name}_{command_name}.md"
            shutil.copy2(skeleton_md_file, f"{module_dir}/console/{md_name}")

        # add command to __init__.py
        with open(f"{module_dir}/__init__.py", "r") as f:
            init_py = f.read()
            init_py += f"\n\n    def {command_name}(self, metadata=None):\n        pass"
            with open(f"{module_dir}/__init__.py", 'w') as init_py_file:
                init_py_file.write(init_py)


    def show(self, metadata=None):
        all_modules = self.get_modules(module=self.args.module_filter, name=self.args.name)
        if len(all_modules) > 0:
            print_utils.print_grid_from_json(all_modules, cols = ['module', 'command', 'name', 'timestamp','cmd_id','fqn'], title="Modules")
        else:
            print(f"\n{colors.WARNING}No modules found for this environment{colors.ENDC}\n")
        return all_modules


    def activate_deactivate(self, action=None):
        if action is None:
            return

        module_name = self.args.module_name
        module_dir = self.args.modules_dirs[self.args.cloud][module_name]
        module_file = f"{module_dir}/module.json"
        with open(module_file, "r") as f:
            module_json = json.load(f)
            commands = self.args.module_commands.split(",")
            if commands[0] == "ALL":
                commands = []
                for cmd in module_json[module_name].keys():
                    commands.append(cmd)

            print(f"\n{action} module {module_name}:")
            for cmd, cmd_details in module_json[module_name].items():
                if cmd in commands:
                    cmd_details['enabled'] = action == "activate"
                    cmd_details['template_enabled'] = action == "activate"
                    print(f"\t{colors.OKBLUE}kc {module_name} {cmd}{colors.ENDC}")

        with open(module_file, "w") as f:
            json.dump(module_json, f, indent=2)

        return module_json, module_name, commands


    def get_template_file(self, module_name, command, check_bundle=False):
        print(f"\t\tgetting template [{module_name}] [{command}]")
        module_template_dir = f"{self.args.modules_dirs[self.args.cloud][module_name]}/console"
        file_name = f"{module_template_dir}/template_{module_name}.json"
        if not exists(file_name):
            file_name = f"{module_template_dir}/template_{module_name}_{command}.json"
        if exists(file_name):
            with open(file_name) as f:
                return json.load(f), file_name
        else:
            return None, None


    def get_imported_template_controls(self, i_feature, i_command):
        i_module_template, f = self.get_template_file(i_feature, i_command, check_bundle=True)
        if i_module_template is not None:
            if len(i_module_template['steps']) > 1:
                form_step = i_module_template['steps'][1]
            else:
                form_step = i_module_template['steps'][0]
            # print(f"getting imported template controls [{i_feature}.{i_command}] ...")
            return form_step['controls']
        else:
            print(f"imported template not found for [{i_feature}.{i_command}]")
        return []


    def append_imported_controls(self, cmd_template_json, controls):
        for i_module, controls in controls.items():
            print(f"appending imported template controls for [{i_module}] ...")
            # Imported Module Constrols Toggle
            module_toggle = copy.deepcopy(IMPORTED_MODULE_TOGGLE)
            module_toggle['id'] = f"{i_module}_enabled"
            module_toggle['label'] = f"Enable {i_module.upper()} module"
            cmd_template_json['steps'][1]['controls'].append(module_toggle)
            for control in controls:
                if control['id'] == 'name':
                    control['id'] = f'{i_module}_name'
                cmd_template_json['steps'][1]['controls'].append(control)
                module_toggle['options'][0]['value']['disableControls'].append(control['id'])
                module_toggle['options'][1]['value']['enableControls'].append(control['id'])
        return cmd_template_json


    def activate(self, metadata=None):
        module_json, module_name, commands = self.activate_deactivate("activate")
        cloud = self.cloud_context["cloud"]

        print("\nactivating console templates:")
        # collect actions to activate
        templates_to_activate = {}
        for cmd in commands:
            print(f"\t{colors.OKBLUE}{module_name} {cmd}{colors.ENDC}:")
            cmd_template_json, f = self.get_template_file(module_name, cmd)
            if cmd_template_json is None:
                continue

            template_section = module_json[module_name][cmd]['template_section']
            if template_section not in templates_to_activate:
                templates_to_activate[template_section] = {}

            # collect imported modules form controls
            if 'import_modules' in module_json[module_name][cmd]:
                controls = {}
                for i_module in module_json[module_name][cmd]["import_modules"].split(","):
                    i_feature = i_module.split(".")[0]
                    i_command = i_module.split(".")[1]
                    controls[i_feature] = self.get_imported_template_controls(i_feature, i_command)
                cmd_template_json = self.append_imported_controls(cmd_template_json, controls)

            # create section dir if not there yet
            section_dir = f"./server/console/template/{template_section}"
            if not os.path.exists(section_dir):
                os.makedirs(section_dir)

            # info file
            info_md_file = f"{self.args.modules_dirs[self.args.cloud][module_name]}/console/template_{module_name}_{cmd}.md"
            if os.path.isfile(info_md_file):
                print(f"\t\t{info_md_file}")
                with open(info_md_file, 'r') as f:
                    cmd_template_json['info'] = "\n".join(f.readlines())

            # save final command template
            file_name = f"{section_dir}/template_{module_name}_{cmd}.json"
            with open(file_name, "w") as target_file:
                print(f"\t\tsaving template for [{module_name}] [{cmd}]")
                print(f"\t\t{file_name}")
                json.dump(cmd_template_json, target_file, indent=4)

            templates_to_activate[template_section][cmd_template_json["id"]] = cmd_template_json

        custom_order_file = f'./server/console/template/custom_order_{cloud}.json'
        if os.path.exists(custom_order_file):
            with open(custom_order_file, 'r') as f:
                order = json.load(f)
        else:
            order = {}

        custom_template_file = f"./server/console/template/custom_template_{cloud}.json"
        if os.path.exists(custom_template_file):
            with open(custom_template_file, "r") as f:
                template_json = json.load(f)
        else:
            template_json = {"sections": []}

        # add section to final_template_{cloud}.json if not there already
        for section_id in templates_to_activate.keys():
            new_section = True
            for section in template_json['sections']:
                # print(section)
                if section_id == section['id']:
                    new_section = False
                    break
            if new_section:
                # print(section_id)
                template_json['sections'].append({
                    "type": "Theia::Section",
                    "label": section_id.capitalize(),
                    "route": section_id,
                    "id": section_id,
                    "enabled": True,
                    "actions": [
                    ]
                })

        # add activated actions to section
        for section in template_json['sections']:
            actions = {}
            if section['id'] in templates_to_activate:
                section_to_activate = templates_to_activate[section['id']]
                print(f"\n\tadding to section {section['id']}")

                # collect current actions by id
                for action in section['actions']:
                    actions[action['id']] = action

                # update order file
                if section['id'] not in order:
                    order[section['id']] = {}
                for action in section_to_activate.values():
                    if action['id'] not in order[section['id']]:
                        order[section['id']][action['id']] = 1000
                    action['order'] = order[section['id']][action['id']]
                    actions[action['id']] = action

                # sort actions
                print("\tsorting actions")
                section['actions'] = list(actions.values())
                section['actions'].sort(key=lambda x: x["order"])

        # save actions order
        with open(custom_order_file, 'w') as f:
            json.dump(order, f, indent=2)

        # save updated custom console template file
        with open(custom_template_file, "w") as f:
            print(f"\tsaving final custom template ...")
            print(f"\t\t{custom_template_file}\n")
            json.dump(template_json, f, indent=2)



    def deactivate(self, metadata=None):
        module_json, module_name, commands = self.activate_deactivate("deactivate")

        print("deactivating console templates ...")
        # collect actions to deactivate
        actions_to_deactivate = []
        for cmd in commands:
            with open(f"{CUSTOM_MODULE_HOME_DIR}/{module_name}/console/template_{module_name}_{cmd}.json", "r") as f:
                cmd_template_json = json.load(f)
                template_section = module_json[module_name][cmd]['template_section']
                action_id = cmd_template_json['id']
                actions_to_deactivate.append(f"{template_section}.{action_id}")
        print(actions_to_deactivate)

        # remove from main custom console template
        cloud = self.cloud_context["cloud"]
        template_file = f"./server/console/template/custom_template_{cloud}.json"
        with open(template_file, "r") as f:
            template_json = json.load(f)
            template_json_final = copy.deepcopy(template_json)
            template_json_final["sections"] = []

            # go through each template section
            for s in range(len(template_json["sections"])):
                section = template_json["sections"][s]
                # print(f"section: {section['id']}")
                enabled_actions = []
                # check each template action and remove if to be deactivated
                if "actions" not in section:
                    continue
                for a in range(len(section["actions"])):
                    action = section["actions"][a]
                    # print(f"\taction: {action['id']}")
                    action_fqn = f"{section['id']}.{action['id']}"
                    if action_fqn in actions_to_deactivate:
                        print(f"deactivating {action_fqn}")
                    else:
                        enabled_actions.append(action)
                if enabled_actions:
                    section["actions"] = []
                    section["actions"].extend(enabled_actions)
                    template_json_final["sections"].append(section)

            # save updated custom template
            with open(template_file, "w") as f:
                json.dump(template_json_final, f, indent=2)


    def export(self, metadata=None):
        module_name = self.args.module_name
        # create empty export dir
        export_dir = f"./temp/export"
        if not os.path.exists(export_dir):
            self.logger.info(f"creating root export_dir: {export_dir}")
            os.makedirs(export_dir)
        module_export_dir = f"{export_dir}/{module_name}"
        if os.path.exists(module_export_dir):
            self.logger.info(f"deleting module_export_dir: {module_export_dir}")
            shutil.rmtree(module_export_dir)

        module_init_py = f"{CUSTOM_MODULE_HOME_DIR}/{module_name}/__init__.py"
        self.logger.info(f"module_init_py: {module_init_py}")
        with open(module_init_py, "r") as f:
            shutil.copytree(f"{CUSTOM_MODULE_HOME_DIR}/{module_name}", module_export_dir)
            export_tf_modules_dir = f"{module_export_dir}/tf/modules"
            os.makedirs(export_tf_modules_dir)
            export_tf_templates_dir = f"{module_export_dir}/tf/custom_templates"
            os.makedirs(export_tf_templates_dir)

            init_py = f.readlines()
            for line in init_py:
                if "super().add_aws_resource" in line:
                    line = line.replace(' ', '').replace('\n', '')
                    if line[0] != '#':
                        line1 = line.replace("super().add_aws_resource", '').replace('(','').replace(')','')
                        resource_type = line1.split(",")[0].replace('\'', '').replace('\"', '')
                        if resource_type != "resource_type":
                            self.logger.info(line)
                            self.logger.info("\t" + line1)
                            self.logger.info("\t\t" + resource_type)
                            tf_template = f"./terraform/custom_templates/{resource_type}.j2"
                            if exists(tf_template):
                                self.logger.info("\t\t\t" + tf_template)
                                shutil.copy2(tf_template, f"{export_tf_templates_dir}/{resource_type}.j2")
                            tf_module = f"./terraform/modules/{resource_type}"
                            if exists(tf_module):
                                self.logger.info("\t\t\t" + tf_module)
                                shutil.copytree(tf_module, f"{export_tf_modules_dir}/{resource_type}")

            shutil.make_archive(f"./temp/export/rapid-cloud-module-{module_name}", 'zip', module_export_dir)


    def install(self, metadata=None):
        if not os.path.exists(self.args.module_zipfile_path):
            self.logger.error(f"Module archive is not found")
            return

        module_name = self.args.module_name
        module_dir = CUSTOM_MODULE_HOME_DIR
        # module_dir = f"./temp/installed/{self.args.name}"
        if os.path.exists(module_dir):
            self.logger.error(f"Module {self.args.name} already exists")
            return

        with ZipFile(self.args.module_zipfile_path, 'r') as module_zip_file:
            self.logger.info(f"extracting {self.args.module_zipfile_path} to {module_dir}")
            module_zip_file.extractall(module_dir)

            # move custom templates
            custom_templates_dir = f"{module_dir}/tf/custom_templates"
            target_dir = f"./terraform/custom_templates"
            for template_file in os.listdir(custom_templates_dir):
                tf_template = f"{target_dir}/{template_file}"
                if not os.path.exists(tf_template):
                    self.logger.info(f"{template_file} -> {tf_template}")
                    src_file = os.path.join(custom_templates_dir, template_file)
                    shutil.move(src_file, target_dir)
                else:
                    self.logger.info(f"{tf_template} already exists")

            # move TF modules
            tf_modules_dir = f"{module_dir}/tf/modules"
            target_dir = f"./terraform/modules"
            for dir in os.listdir(tf_modules_dir):
                if not os.path.exists(f"{target_dir}/{dir}"):
                    src_dir = os.path.join(tf_modules_dir, dir)
                    self.logger.info(f"{src_dir} -> {target_dir}")
                    shutil.move(src_dir, target_dir)
                else:
                    self.logger.info(f"{target_dir}/{dir} already exists")

        self.logger.info(f"You have successfully ibstalled {module_name} module")


    def create_template(self, metadata=None):
        template, file_name = self.get_template_file(metadata["template_module"], metadata["template_action"])
        if template:
            self.logger.info(f"backing up {file_name}")
            with open(file_name.replace(".json", "-OLD.json"), 'w') as f:
                json.dump(template, f, indent=2)

            changes = {
                "steps": []
            }

            grid = None
            if metadata["grid_enabled"]:
                grid = {
                    "type": "Theia::Step::Grid",
                    "id": template["id"],
                    "datasource": metadata.get("grid_datasource",""),
                    "columns": metadata.get("grid_columns","").replace(" ","").split(","),
                    "title": metadata.get("grid_title",""),
                    "description": metadata.get("grid_description","")
                }
                template["steps"][0].update(grid)
            else:
                self.logger.info("no grid step")

            if metadata["form_enabled"]:
                form = {
                    "type": "Theia::Step::Form",
                    "id": template["id"],
                    "title": metadata.get("form_title",""),
                    "description": metadata.get("form_description",""),
                    "submit": "Submit",
                    "commands": [{
                        "label": metadata.get("form_submit_label",""),
                        "command": {
                            "phase": metadata.get("module",""),
                            "command": metadata.get("command",""),
                            "refresh_status": metadata.get("form_submit_refresh_status",False)
                        }
                    }],
                    "controls": []
                }

                if metadata.get("form_enable_undo", False):
                    form["commands"].insert(0, {
                        "label": "Remove",
                        "command": {
                            "phase": "undo-command"
                        }
                    })

                for i in range(1, 21):
                    if metadata.get(f"arg{i}", False):
                        control = {
                            "type": "Theia::Control::" + metadata.get(f"arg{i}_type",""),
                            "id": metadata.get(f"arg{i}_name",""),
                            "label": metadata.get(f"arg{i}_label",""),
                            "help": metadata.get(f"arg{i}_help",""),
                            "inputType": metadata.get(f"arg{i}_inputType",""),
                            "readonly_edit": metadata.get(f"arg{i}_readonly_edit",False)
                        }
                        form["controls"].append(control)

                template["steps"][1 if grid else 0].update(form)

            else:
                self.logger.info("no form step")

            self.logger.info(f"saving {file_name}")
            with open(file_name.replace(".json", "-NEW.json"), 'w') as f:
                json.dump(template, f, indent=2)

