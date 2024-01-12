# #!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import glob
import json
import os
from os.path import exists
from sys import argv
import sys
from tabulate import tabulate

from commands import general_utils
from commands.modules import get_module_json_dirs

OKBLUE = '\033[94m' 
OKGREEN = '\033[92m' 
WARNING = '\033[93m' 
FAIL = '\033[91m'
ENDC = '\033[0m'
UNDERLINE = '\033[4m'

def gen_help_json(args):
    with open('./docs/help.json', 'r') as f:
        result = json.load(f)

    for cloud in ["aws", "azure"]:
        for module_name, modules_dir in args.modules_dirs[cloud].items():
            print(modules_dir)
            for file_name in glob.glob(modules_dir, recursive=True):
                file_name = file_name.replace("\\","/") + "/module.json" # fixes windows issue
                with open(file_name) as f:
                    filesize = os.path.getsize(file_name)
                    if filesize > 0:
                        module_config = json.load(f)
                        for feature, commands in module_config.items():                    
                            if feature not in commands:
                                result[feature] = {}
                            for command, command_config in commands.items():
                                if 'enabled' in command_config and command_config['enabled']:
                                    result[feature][command] = {
                                        "text": command_config['help'] if 'help' in command_config else '',
                                        "cmd": f"kc {feature} {command}"
                                    }
                                    if 'args' in command_config:
                                        result[feature][command]['args'] = command_config['args']

    # for feature in ['admin']:
    #     del result[feature]
    # print(json.dumps(result, indent=2))
    with open('./docs/help.json', 'w') as f:
        json.dump(result, f, indent=2)


def gen_help_terminal(args):
    with open('./docs/help.json', 'r') as f:
        
        # subscription tiers
        tiers = {}
        from commands.cli_worker.license_worker import LicenseWorker
        for tier in LicenseWorker(args).contact_lic_server("get_tiers"):
            if tier.get("enabled", True) or general_utils.get_app_mode() == "dev":
                tiers[tier['feature']] = tier['tiers'].split(",")[0]
        features = {
            "1": {},
            "2": {}
        }
        if general_utils.get_app_mode() == "dev":
            features["3"] = {} # admin help is only available in dev mode
        
        # help info sorted by tier and feature
        help = json.load(f)
        for feature in sorted(help.keys()):
            if feature not in tiers:
                # print(f"missing {feature}")
                continue
            item = help[feature]
            tier = tiers[feature]
            features[tier][feature] = item

        # header
        print(f"\n{OKGREEN}Usage: kc [--version] <module> <command> [args]{ENDC}\n")
        
        tier_label = {
            "1": "Free",
            "2": "Premium",
            "3": "Admin"
        }

        for tier in features.keys():
            curr_grid = None
            grid = []
            deploy_grid = []

            print(f"{OKBLUE}{tier_label[tier]} Tier Commands:{ENDC}\n")

            for feature in features[tier].keys():
                # print(f"{args.command} | {feature}")
                if args.command and feature != args.command:
                    continue
                if feature not in ["tf", "deploy"]:
                    curr_grid = grid
                else:
                    curr_grid = deploy_grid

                commands = sorted(help[feature].keys())
                for k in commands:
                    command = help[feature][k]
                    cmd = command['cmd']
                    s = cmd.split()
                    cmd2 = s[2] if len(s) > 2 and '--' not in s[2] else ''
                    if args.command and feature != args.command:
                        continue
                    
                    text = command['text']
                    curr_grid.append(["\t", f"{OKBLUE}{feature}{ENDC}", f"{OKBLUE}{cmd2}{ENDC}", "\t",f"{text}"])
                    if args.command:
                        curr_grid.append([])
                        curr_grid.append(["\t", "\t", "\t", "\t", f"$ {OKBLUE}kc {feature} {cmd2}{ENDC}"])
                        curr_grid.append([])
                        if 'args' in command:
                            for k,v in command['args'].items():
                                curr_grid.append(["\t", "\t", f"--{k}", "\t", v['prompt']])
                        else:
                            cmd_split_new = cmd.split("--")
                            if len(cmd_split_new) > 1:
                                for i in range(1, len(cmd_split_new)):
                                    j = cmd_split_new[i].find(" ")
                                    arg = cmd_split_new[i][:j]
                                    value = cmd_split_new[i][j + 1:].replace('\'', '')
                                    curr_grid.append(["\t", "\t", f"--{arg}", "\t", value])
                        curr_grid.append([])
            
            if curr_grid:
                # curr_grid.append([])
                grid += deploy_grid
            grid = tabulate(grid, tablefmt='plain')
            print(grid)
            print("")


def fix():
    result = {}
    with open('./docs/help_old.json', 'r') as f:
        commands = json.load(f)
        for text, v in commands.items():
            cmd = v['cmd']
            s = cmd.split()
            f = s[1]
            c = ''
            if len(s) > 2:
                c = cmd.split()[2]
            # print(f"kc {f} {c} -> {text}")
            if f not in result:
                result[f] = {}
            if c not in result[f]:
                result[f][c] = {
                    "text": text,
                    "cmd": cmd
                }
    print(json.dumps(result, indent=2))
    with open('./docs/help.json', 'w') as f:
        json.dump(result, f, indent=2)


# if __name__ == "__main__":
#     # 
#     print(argv)
#     if argv[1] == 'json':
#         gen_help_json()
#     elif argv[1] == 'terminal':
#         gen_help_terminal()    
#     elif argv[1] == 'fix':
#         fix()    