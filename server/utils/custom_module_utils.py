#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


from collections import OrderedDict
import importlib
import json
import logging
import os
import sys
import traceback

from commands.modules import load_modules


logger = logging.getLogger("custom_module_utils")
logger.setLevel(logging.INFO)


def get_modules(args, user_session):
    custom_modules = []
    modules_info, module_dirs = get_custom_modules_for_cloud(user_session["cloud"])
    for module, commands in modules_info.items():
        for cmd in commands.keys():
            break
        custom_modules.append({
            "module_name": module,
            "module_action": cmd,
            "module_dir": module_dirs.get(module, None),
            "cmd_id": "N/A"
        })
    return sorted(custom_modules,  key=lambda x: x['module_name'])


def get_modules_select(args, user_session):
    select_options = []
    for module in get_modules(args, user_session):
        select_options.append({
            "type": "Theia::Option", 
            "label": module["module_name"], 
            "value": module["module_name"]
        })
    return select_options


def get_commands(args, user_session):
    custom_modules = []
    modules_info, module_dirs = get_custom_modules_for_cloud(user_session["cloud"])
    for module, commands in modules_info.items():
        for cmd, cmd_config in commands.items():
            # print(cmd_config)
            item = {
                "cli": f"kc {module} {cmd}",
                "module_name": module,
                "module_action": cmd,
                "enabled": cmd_config.get("enabled", False),
                "template_enabled": cmd_config.get("template_enabled", False),
                "template_section": cmd_config.get("template_section", ""),
                "id_arg": cmd_config.get("id", ""),
                "args": json.dumps(cmd_config.get("args",{}), indent=2)
            }
            custom_modules.append(item)
    return custom_modules


def get_templates(args, user_session):
    templates = []
    for module, commands in get_custom_templates(args, user_session["cloud"]).items():
        for command, info in commands.items():
            item = {
                "template_module": module,
                "template_action": command
            }
            item.update(info)
            templates.append(item)
    return templates



# load console templates info
def get_custom_templates(args, cloud):
    logger.info("loading custom templates ...")
    result = {}
    modules_for_cloud, module_dirs = get_custom_modules_for_cloud(cloud)
    for module, commands in modules_for_cloud.items():
        module_dir = args.modules_dirs[cloud][module]
        for cmd, cmd_config in commands.items():
            template_file = f"{module_dir}/console/template_{module}_{cmd}.json"
            if os.path.exists(template_file):
                with open(template_file) as f:
                    template = json.load(f)
                    if module not in result:
                        result[module] = {}

                    result[module][cmd] = {
                        "template_id": template["id"],
                        "label": template["label"]
                    }

                    # Grid
                    if template["steps"][0]["type"] == "Theia::Step::Grid":
                        grid = template["steps"][0]
                        result[module][cmd]["grid_enabled"] = True
                        for key in ["title","columns","datasource","description"]:
                            result[module][cmd][f"grid_{key}"] = grid.get(key, "")

                    # Form
                    if len(template["steps"]) > 1 and template["steps"][1]["type"] == "Theia::Step::Form":
                        form = template["steps"][1]
                        result[module][cmd]["form_enabled"] = True
                        result[module][cmd]["form_title"] = form["title"]

                        # Buttons
                        for form_cmd in form["commands"]:
                            # Remove button
                            if form_cmd["command"]["phase"] == "undo-command":
                                result[module][cmd]["form_undo_enabled"] = True
                                button = "undo"
                            # Submit button
                            else:
                                result[module][cmd]["form_submit_enabled"] = True
                                button = "submit"
                            # Button info
                            result[module][cmd][f"form_{button}_refresh_status"] = form_cmd["command"].get("refresh_status", False)
                            for key in ["label","require_confirmation","confirmation_message"]:
                                result[module][cmd][f"form_{button}_{key}"] = form_cmd.get(key, "")

                        i = 1
                        # Controls
                        controls = []
                        for control in form["controls"]:
                            arg = f"arg{i}"
                            result[module][cmd][arg] = True
                            for key in ["type","id","label","readonly","help","readonly_edit","datasource"]:
                                result[module][cmd][f"{arg}_{key}"] = control.get(key, "")
                            controls.append(control.get("id"))
                            i += 1
                        
                        # Arguments in modules.json that have no controls yet
                        for cmd_arg, info in cmd_config.get("args",{}).items():
                            if f"{module}_{cmd_arg}" not in controls and cmd_arg  not in controls:
                                # logger.info(f"adding control for {module}.{cmd}.{cmd_arg}")
                                arg = f"arg{i}"
                                result[module][cmd][arg] = False
                                result[module][cmd][f"{arg}_id"] = f"{module}_{cmd_arg}"
                                for key in ["type","label","readonly","help","readonly_edit","datasource"]:
                                    result[module][cmd][f"{arg}_{key}"] = info.get(key, "")
                                i += 1


    ordered = OrderedDict(sorted(result.items()))
    return ordered
    


# ------------------------------------------------------
# custom server for custom modules
# ------------------------------------------------------
def custom_endpoint(action, args, cloud_session, user_session_vars, cloud): 
    module_name = args['module_name_arg']
    result = None

    # custom module outside the bundle or dev mode
    # module_dir:
    #   /rapidcloud-core/./commands/modules/lambda
    #   /rapidcloud-modules/rc-aws-net/./commands/modules/net
    try:
        modules_by_cloud, modules_dirs, add_args_list = load_modules(skip_bundled=False)
        module_dir = modules_dirs.get(cloud, {}).get(module_name, None)
        if module_dir is not None:
            module_dir = module_dir.replace("/./", "/")
            logger.info(f"module_dir: {module_dir}")
            custom_server_file = module_dir.replace(f"/commands/modules/{module_name}", "/server/custom_server.py")
            if os.path.exists(custom_server_file):
                logger.info(f"checking custom_server: {action}")
                spec = importlib.util.spec_from_file_location("custom_server", custom_server_file)
                custom_server = importlib.util.module_from_spec(spec)
                sys.modules["custom_server"] = custom_server
                spec.loader.exec_module(custom_server)
                func = getattr(custom_server, "custom_endpoint")
                result = func(action, args, cloud_session, user_session_vars)

    except Exception as e:
        logger.error(e)
        if args.get("debug", 0) > 0:
            traceback.print_exc() 

    # external module <modul_name>_custom_server.py added during build process
    if result is None and '_MEI' in getattr(sys, '_MEIPASS', os.getcwd()):
        try:
            custom_server_name = f"{module_name}_custom_server"
            logger.info(f"checking {custom_server_name}: {action}")
            custom_server = importlib.import_module(f"server.{custom_server_name}")
            func = getattr(custom_server, "custom_endpoint")
            result = func(action, args, cloud_session, user_session_vars)
        except Exception as e:
            logger.info(e)
            if args.get("debug", 0) > 0:
                traceback.print_exc() 

    if result is None:
        return []
    
    return result


def get_custom_modules_for_cloud(cloud):
    modules_by_cloud, modules_dirs, add_args_list = load_modules(skip_bundled=True)
    return modules_by_cloud.get(cloud, {}), modules_dirs.get(cloud, {})


def action(args, action, user_session):
    if action == "get_modules":
        return get_modules(args, user_session)
    elif action == "get_commands":
        return get_commands(args, user_session)
    elif action == "get_modules_select":
        return get_modules_select(args, user_session)
    elif action == "get_templates":
        return get_templates(args, user_session)
