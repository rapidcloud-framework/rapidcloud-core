__author__ = "Igor Royzis"
__license__ = "MIT"


from collections import OrderedDict
import glob
import json
import logging
import os
from os.path import exists
import sys
import importlib
import copy

from commands import print_utils
from commands.colors import colors


logger = logging.getLogger("cli_argument_utils")


def get_user_input(args, arg: str, prompt_info: dict, imported_module=None, curr_values=None):
    arg_name = prompt_info["name"]
    arg_prompt = prompt_info.get("prompt", f"Enter value")
    arg_required = prompt_info.get("required", True)

    arg_multi_value = prompt_info.get("multi-value", False)
    arg_keys = prompt_info.get("keys", None)

    curr_value = curr_values[arg] if curr_values else prompt_info["curr_value"]

    # Console or no-prompt mode - arguments are already in self.args
    if args.mode == 'console' or args.no_prompt:
        if imported_module:
            i_arg = f"{imported_module}_{arg}"
            value = getattr(args, i_arg, None)
        else:
            fq_arg = f"{args.module}_{arg}"
            value = getattr(args, fq_arg, None)
            if value is None:
                value = getattr(args, arg, None)
        print(f"{colors.OKBLUE}{arg}{colors.ENDC}: {value}")
        return value

    # CLI mode - text argument
    elif not arg_multi_value:
        return get_text_arg(arg_name, arg_prompt, curr_value, arg_required)

    # CLI mode - multi-value argument
    elif arg_multi_value:
        return get_multi_value_arg(arg_name, arg_prompt, curr_value, arg_required)


def get_text_arg(arg_name, arg_prompt, curr_value, arg_required):
    value = input(f"{colors.OKBLUE}{arg_prompt}{colors.ENDC} [{curr_value}]: ")
    if arg_required:
        while value == '' and (curr_value == '' or curr_value == 'none'):
            value = input(f"{colors.WARNING}{arg_name} is required:{colors.ENDC} ")
    if value == '':
        value = curr_value
    return value


def get_multi_value_arg(arg_name, arg_prompt, curr_value, arg_required):
    print(f"{colors.OKBLUE}{arg_prompt}{colors.ENDC}")
    values = []
    i = 0
    while True:
        more_values = "yes"
        if i > 0:
            more_values = input(f"\t\t{colors.OKBLUE}more?{colors.ENDC} (yes|no) [yes]: ")

        if more_values.lower() in ["", "yes"]:
            if curr_value and len(curr_value) > i:
                curr_value_i = curr_value[i]
            else:
                curr_value_i = ""
            value = input(f"\t{colors.OKBLUE}{i+1}.{colors.ENDC} [{curr_value_i}]: ")
            if arg_required:
                while value == '' and (curr_value == '' or curr_value == 'none'):
                    value = input(f"\t{colors.WARNING}{arg_name} is required:{colors.ENDC} ")
            if value == '':
                value = curr_value_i
            values.append(value)
            i += 1
        
        else:
            break
    
    return values
