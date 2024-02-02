__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import os
from os.path import exists
import glob
import shutil
import sys
import traceback


CUSTOM_MODULE_HOME_DIR = "./commands/modules"
with open('./config/modules_config.json', 'r') as f:
    modules_config = json.load(f)
    CUSTOM_MODULES_PROJECT_DIR = modules_config["modules_parent_dir"]
TEMPLATE_HOME_DIR = "./server/console/template/"

class colors:
    OKBLUE = '\033[94m' 
    OKGREEN = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

MODULAR = [    
]

NON_MODULAR = [    
]

NO_LONGER_USED = [    
]

def add_action_to_template(template, section, action):
    print(f"    {section} -> {action}")
    for template_section in template['sections']:
        if template_section['id'] == section and action not in template_section['actions']:
            template_section['actions'].append(action)


def get_imported_controls(command, module_json, module_json_files):
    imported_controls = {}
    if "import_modules" in command:
        for i_module in command["import_modules"].split(","):
            i_feature = i_module.split(".")[0]
            i_command = i_module.split(".")[1]

            # "rds": "/Users/iroyzis/Workspace/kinect/kinect-frameworks/rapidcloud-core/commands/modules/rds/module.json"
            module_dir = module_json_files[i_feature].replace("/module.json", "")
            # print(f"{i_feature} dir: {module_dir}")
            i_module_template_file = f'{module_dir}/console/template_{i_feature}.json'

            if not exists(i_module_template_file):
                i_module_template_file = f'{module_dir}/console/template_{i_feature}_{i_command}.json'
            
            if not exists(i_module_template_file):
                print(f"{i_feature}.{i_command}  has no console template")
            
            else:
                with open(i_module_template_file) as ifile:
                    i_module_template = json.load(ifile)
                    form_step = i_module_template['steps'][1] if len(i_module_template['steps']) > 1 else i_module_template['steps'][0]
                    imported_controls[i_feature] = {
                        "help": module_json[i_feature][i_command]['help'],
                        "controls": form_step['controls']
                    }
                    
    return imported_controls


def append_imported_controls(target_file_name, imported_controls):
    with open(target_file_name, "r") as target_file:
        target_template = json.load(target_file)        
        target_controls = target_template['steps'][1]['controls']
        accordion = {
            "type": "Theia::Control::CompositeModule",
            "id": "composite_module",
            "modules": []
        }
        target_controls.append(accordion)

        for i_module, form in imported_controls.items():
            module_toggle = {
                "type": "Theia::Control::Toggle",
                "id": f"{i_module}_enabled",
                "label": form['help'],
                "controls": []
            }
            accordion["modules"].append(module_toggle)

            for control in form['controls']:
                if control['id'] == 'name':
                    control['id'] = f'{i_module}_name'
                module_toggle["controls"].append(control)            

    with open(target_file_name, "w") as target_file:
        json.dump(target_template, target_file, indent=2)


def copy_template_file(module_dir, module_name, command_name, action_template_dir, template_section, imported_controls):
    src_file_name = f"{module_dir}console/template_{module_name}.json"
    src_file_name_w_command = f"{module_dir}console/template_{module_name}_{command_name}.json"
    target_file_name = None

    # determine target template file name
    if exists(src_file_name):
        target_file_name = f"{action_template_dir}/template_{template_section}_{module_name}.json"
    elif exists(src_file_name_w_command):
        src_file_name = src_file_name_w_command
        target_file_name = f"{action_template_dir}/template_{template_section}_{module_name}_{command_name}.json"

    if target_file_name:
        # append module_name param to all /custom endpoints
        with open(src_file_name, 'r') as f:
            src_templ = json.load(f)
            step_no = 0
            if "steps" in src_templ.copy():
                for step in src_templ["steps"]:
                    if step["type"] == "Theia::Step::Form":
                        ctl_no = 0
                        for ctl in step["controls"]:
                            for attr, value in ctl.items():
                                if attr == "datasource":
                                    c = "&" if "?" in value else "?"
                                    if "module_name_arg" not in src_templ["steps"][step_no]["controls"][ctl_no]["datasource"]:
                                        src_templ["steps"][step_no]["controls"][ctl_no]["datasource"] = f"{value}{c}module_name_arg={module_name}"
                            ctl_no += 1
                    step_no += 1

        # shutil.copy2(src_file_name, target_file_name)
        with open(target_file_name, "w") as target_file:
            json.dump(src_templ, target_file, indent=2)

        if imported_controls:
            append_imported_controls(target_file_name, imported_controls)
        MODULAR.append(target_file_name)


def copy_md_files(module_dir, module_name, command_name, action_template_dir, template_section):
    suffix = {
        "": "_info",
        "_description": ""
    }
    for src_suffix,target_suffix in suffix.items():
        src_file_name = f"{module_dir}console/template_{module_name}{src_suffix}.md"
        src_file_name_w_command = f"{module_dir}console/template_{module_name}_{command_name}{src_suffix}.md"

        target_file_name = None
        if exists(src_file_name):
            target_file_name = f"{action_template_dir}/template_{template_section}_{module_name}{target_suffix}.md"
        elif exists(src_file_name_w_command):
            src_file_name = src_file_name_w_command
            target_file_name = f"{action_template_dir}/template_{template_section}_{module_name}_{command_name}{target_suffix}.md"

        if target_file_name:
            shutil.copy2(src_file_name, target_file_name)


def get_module_json_files():
    modules_jsons = []

    # multi-repo custom modules
    if os.path.exists(CUSTOM_MODULES_PROJECT_DIR):
        modules_jsons.append(f"{os.path.abspath(CUSTOM_MODULES_PROJECT_DIR)}/*/{CUSTOM_MODULE_HOME_DIR}/*/module.json")
    
    # for bundle also collect custom modules from local file system
    home_dir = getattr(sys, '_MEIPASS', os.getcwd())
    if '_MEI' in home_dir:
        modules_jsons.append(f'{CUSTOM_MODULE_HOME_DIR}/*/module.json')

    # bundled modules (or main repo in dev mode)
    modules_jsons.append(f'{home_dir}/{CUSTOM_MODULE_HOME_DIR}/*/module.json')
    module_json_files = {}
    for modules_dir in modules_jsons:
        for file_name in glob.glob(modules_dir, recursive=True):
            file_name = file_name.replace("\\","/") # fixes windows issue
            module_name = file_name.split("/")[-2]
            if module_name == "skeleton":
                continue
            module_json_files[module_name] = file_name.replace("/./", "/")
    return module_json_files


def copy_module_templates(template, skip_disabled):
    module_json_files = get_module_json_files()
    module_json_files_keys = list(module_json_files.keys())
    module_json_files_keys.sort()
    module_json_files = {i: module_json_files[i] for i in module_json_files_keys}
    print(json.dumps(module_json_files, indent=2))

    # collect all module commands information
    module_json = {}
    for module_name, file_name in module_json_files.items():
        with open(file_name) as file:
            module_config = json.load(file)
            for module, commands in module_config.items():
                module_json[module] = {}
                for command_name, command in commands.items():
                    module_json[module][command_name] = command

    # copy module templates to proper section dir `console/template/*/*.json`
    for module_name, file_name in module_json_files.items():
        module_dir = file_name.replace(file_name.split("/")[-1], "")
        with open(file_name) as file:
            print(f">> {module_name}: {module_dir}")
            module_config = json.load(file)
            for module, commands in module_config.items():
                for command_name, command in commands.items():
                    if 'template_section' in command:
                        template_section = command['template_section']
                        if template_section != "" and command['template_enabled']:

                            # add action to main template
                            action_name = f"{module}_{command_name}"
                            print(f"   {template_section}: {action_name}")
                            if os.path.exists(f"{module_dir}/console/template_{module}.json"):
                                add_action_to_template(template, template_section, module)
                            else:
                                add_action_to_template(template, template_section, action_name)
                            action_template_dir = TEMPLATE_HOME_DIR + template_section

                            # Make sure section dir exists. Create otherwise
                            if not os.path.exists(action_template_dir):
                                os.makedirs(action_template_dir)

                            imported_controls = get_imported_controls(command, module_json, module_json_files)
                            
                            copy_template_file(module_dir, module_name, command_name, action_template_dir, template_section, imported_controls)
                            
                            copy_md_files(module_dir, module_name, command_name, action_template_dir, template_section)


def add_action(section, order, action, skip_disabled, actions):
    # action_template_file = f"./server/console/template/{section['id']}/template_{section['id']}_{action}.json"    

    # account for actions from other sections via "::" separator
    if "::" not in action:
        action_template_file = f"./server/console/template/{section['id']}/template_{section['id']}_{action}.json"    
    else:
        section_id = action.split("::")[0]
        action_id = action.split("::")[1]
        action_template_file = f"./server/console/template/{section_id}/template_{section_id}_{action_id}.json"    

    # make sure template file exists
    if os.path.isfile(action_template_file):
        if action_template_file not in MODULAR:
            NON_MODULAR.append(action_template_file)
        
        with open(action_template_file, 'r') as f:
            action_template = json.load(f)
            action_template['order'] = order[section['id']][action]

            if skip_disabled and action_template.get('disabled'):
                return False

            # info file
            # info_md_file = f"./server/console/template/{section['id']}/template_{section['id']}_{action}_info.md"

            # account for actions from other sections via "::" separator
            if "::" not in action:
                info_md_file = f"./server/console/template/{section['id']}/template_{section['id']}_{action}_info.md"
            else:
                section_id = action.split("::")[0]
                action_id = action.split("::")[1]
                info_md_file = f"./server/console/template/{section_id}/template_{section_id}_{action_id}_info.md"

            if os.path.isfile(info_md_file):
                with open(info_md_file, 'r') as f:
                    action_template['info'] = "\n".join(f.readlines())

            # description markdown
            if "steps" in action_template:
                step1 = action_template['steps'][0]
                if "allowMarkdown" in step1 and step1['description'] == "":
                    action_md_file = f"./server/console/template/{section['id']}/template_{section['id']}_{action}.md"
                    with open(action_md_file, 'r') as f:
                        step1['description'] = "\n".join(f.readlines())

            actions.append(action_template) 
            return True, action_template
    else:
        print(f"{action_template_file} not found:", end=" ")
    return False, {}

def generate_template(skip_disabled=False, cloud=None):
    print("")
    print("Generating console template")
    try:
        if not skip_disabled:
            skip_disabled = sys.argv[1] == "skip_disabled"
        if not cloud:
            cloud = sys.argv[2]

        order_file = f'./server/console/template/order_{cloud}.json'
        version_file = './config/version.json'
        template_skeleton_file = f'./server/console/template/template_{cloud}.json'
        final_template_file = f'./server/console/template/final_template_{cloud}.json'
        console_home_file = f'./docs_internal/readme/CONSOLE_HOME_{cloud.upper()}.md'

        for f in [order_file,version_file,template_skeleton_file,final_template_file,console_home_file]:
            print(f)

        with open(order_file, 'r') as f:
            order = json.load(f)  

        with open(version_file, 'r') as f:
            version_config = json.load(f) 
            version = version_config['version'] 
            copyright = version_config['copyright'] 

        with open(template_skeleton_file, 'r') as f:
            template = json.load(f)
            for footer in template['footer']['columns']:
                footer['content'] = footer['content'].replace("{version}", version)
                footer['content'] = footer['content'].replace("{copyright}", copyright)

        # copy module console templates to ./server/console/temnplate/*
        copy_module_templates(template, skip_disabled)
        
        sections = [] 
        for section in template['sections']:
            # print(section)
            if section['id'] not in order:
                order[section['id']] = {}

            if skip_disabled and not section['enabled']:
                # print(f"[{section['id']}]: disabled")
                continue
            
            sections.append(section)
            actions = []
            if 'actions' in section:
                print(f"> {section['id']} ({section['label']})")
                for action in section['actions']:
                    if action not in order[section['id']]:
                        order[section['id']][action] = 1000
                    ok, action_template = add_action(section, order, action, skip_disabled, actions)
                    print(f"\t{action} ({action_template.get('label')}):", end=" ")
                    if ok:
                        print(f"{colors.OKGREEN}ok{colors.ENDC}")
                    else:
                        print(f"{colors.FAIL}disabled{colors.ENDC}")
                
                actions.sort(key=lambda x: x["order"])
                section['actions'] = actions
        
        template['sections'] = sections 
        
        with open(order_file, 'w') as f:
            json.dump(order, f, indent=2)

        with open(console_home_file, 'r') as f:
            home_markdown = "\n".join(f.readlines())
            dashboard = {
                "id": "dashboard",
                "type": "Theia::Dashboard",
                "label": "Dashboard",
                "rows": [{
                    "columns": [{
                        "size": 12,
                        "panel": {
                            "type": "Theia::Panel::Markdown",
                            "title": f"RapidCloud for {cloud.upper()} - Automation & Acceleration Framework",
                            "content": home_markdown
                        }
                    }]
                }]
            }            
            template['sections'][0]['actions'].append(dashboard)

        with open(final_template_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        # print("Modular:")
        # print(json.dumps(MODULAR, indent=2))
        # print("")
        # print("Non-Modular:")
        # print(json.dumps(NON_MODULAR, indent=2))

        # # collect all module commands information
        # for file_name in glob.glob("./server/console/template/*/*", recursive=True):
        #     json_file_name = file_name.replace("_info.md", ".json")
        #     md_file_name = file_name.replace(".md", ".json")
        #     if file_name not in MODULAR and file_name not in NON_MODULAR and json_file_name not in MODULAR and json_file_name not in NON_MODULAR and md_file_name not in MODULAR and md_file_name not in NON_MODULAR:
        #         NO_LONGER_USED.append(file_name)
        # print("")
        # print(f"No Used for {cloud}:")
        # print(json.dumps(NO_LONGER_USED, indent=2))


    except Exception as e:
        traceback.print_exc() 
        print(e)
    
    print("")


if __name__ == "__main__":
    generate_template()
    