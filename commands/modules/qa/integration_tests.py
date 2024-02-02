#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"



import logging
import argparse
from datetime import datetime
import glob
import json
import os
import shutil
import subprocess
import sys
from os.path import exists
import time
import textwrap
from tabulate import tabulate
from commands import general_utils, print_utils
from commands.modules.module import module_utils


OKBLUE = '\033[94m' 
OKGREEN = '\033[92m' 
WARNING = '\033[93m' 
FAIL = '\033[91m'
ENDC = '\033[0m'
UNDERLINE = '\033[4m'

BLANK_2 = "  "
BLANK_4 = "    "
BLANK_6 = "      "
BLANK_8 = "        "
BLANK_10 = "          "

LEGACY_TEST_MODULES = ('init', 'ingest', 'transform', 'analytics')


class IntegrationTests(object):

    logger = logging.getLogger(__name__)

    def __init__(self, module):
        self.module = module
        self.args = module.args
        self.env = module.env

        self.log_file_path = f"./testing/integration/results/rc_tests_{self.args.env_suffix}"
        if os.path.exists(self.log_file_path):
            shutil.rmtree(self.log_file_path)
        os.makedirs(self.log_file_path)


    def run_test(self, module, command, test, n):
        env_vars = os.environ.copy()
        test = test.replace("{env_suffix}",self.args.env_suffix)
        log_file = f"{self.log_file_path}/{module}_{command}_{n}.log"
        result_file = f"{self.log_file_path}/{module}_{command}_{n}.json"
        cmd = test
        cmd_ = f"kc {module} {command}"
        test = test.replace(cmd_, f"{OKBLUE}{cmd_}{ENDC}")
        full_cmd = textwrap.fill(test, initial_indent=BLANK_6, subsequent_indent=BLANK_10, width=120)
        print(full_cmd)
        if os.path.isfile('kc_lock'):
            os.remove('kc_lock')
        if self.args.verbose:
            cmd += f" --result_path {result_file} --no-prompt | tee -a {log_file}"
            subprocess.run(cmd, shell=True, check=True, env=env_vars)
        else:
            cmd += f" --result_path {result_file} --no-prompt"
            with open(log_file, 'w') as f: 
                subprocess.run(cmd, shell=True, check=True, env=env_vars, stdout=f, stderr=subprocess.STDOUT)
        
        if exists(result_file):
            with open(result_file, 'r') as f:
                result_info = json.load(f)
                if "message" in result_info and result_info['message'] == "Command completed successfully":
                    status = "passed"
                    message = f"{OKGREEN}{status}{ENDC}" 
                else:
                    status = "failed"
                    if "message" in result_info:
                        message = f"{FAIL}failed{ENDC} ({result_info['message']})"
                    elif "error" in result_info:
                        message = f"{FAIL}failed{ENDC} ({result_info['error']})"
        else:
            status = "missing result file"
            message = f"{FAIL}missing result file{ENDC}"

        print("")
        print(f"{BLANK_6}==============================================")
        print(f"{BLANK_6}kc {module} {command} ({n}): {message}")
        print(f"{BLANK_6}==============================================")
        print("")

        return status


    def run_tests(self):
        qa_modules = self.args.qa_modules.split(",")
        print(qa_modules)
        print("")

        with open('./testing/integration/test_order.json', 'r') as f:
            test_order = json.load(f)

        with open('./testing/integration/legacy_tests.json', 'r') as f:
            legacy_tests = json.load(f)

        test_cases = self.load_test_cases()
        for test in LEGACY_TEST_MODULES:
            test_cases[test] = legacy_tests[test]
        for module in test_cases.keys():
            if module not in test_order:
                test_order[module] = 1000

        new_order = {}
        ordered = sorted(test_order.items(), key=lambda x:x[1])
        results = []
        for module, order in ordered:
            new_order[module] = order
            if "ALL" not in qa_modules and module not in qa_modules:
                continue

            print(f"\n - {OKBLUE}{module}{ENDC}")
            for command, test_info in test_cases[module].items():
                result = {
                    "module": module,
                    "command": command,
                    "count": 0,
                    "status": None
                }
                if test_info["tests"]:
                    n = 1
                    for test in test_info["tests"]:
                        print(f"   - {OKBLUE}{command}{ENDC}")
                        status = self.run_test(module, command, test, n)
                        result["count"] = n
                        result["status"] = status
                        if status != "passed" and "exit_on_fail" in test_info and test_info["exit_on_fail"]:
                            print(f"\n\n{FAIL}exiting tests{ENDC}\n\n")
                            return
                        n += 1

                else:
                    print(f"   - {command} {WARNING}(no tests found){ENDC}")
                    result["status"] = "no tests found"

                if result["status"] == "passed":
                    result["status"] = f"{OKGREEN}{result['status']}{ENDC}"
                elif result["status"] == "failed":
                    result["status"] = f"{FAIL}{result['status']}{ENDC}"
                else:
                    result["status"] = f"{WARNING}{result['status']}{ENDC}"
                results.append(result)
        
        print_utils.print_grid_from_json(results)

        with open('./testing/integration/test_order.json', 'w') as f:
            json.dump(new_order, f, indent=2)

        with open('./testing/integration/test_cases.json', 'w') as f:
            json.dump(test_cases, f, indent=2)


    def load_test_cases(self):
        modules = {}
        module_tests = {}

        # load modules and commands
        for file_name in glob.glob(f'{module_utils.CUSTOM_MODULE_HOME_DIR}/*/module.json', recursive=True):
            module_name = file_name.split("/")[-2]
            # print(f"{module_name}: {file_name}")
            modules[module_name] = {}
            module_tests[module_name] = {}
            if os.path.exists(file_name):
                with open(file_name) as f:
                    module_config = json.load(f)
                    for commands in module_config.values():
                        for cmd, cmd_config in commands.items():
                            modules[module_name][cmd] = {}
                            module_tests[module_name][cmd] = {}
                            sample_arg_line = f"kc {module_name} {cmd} --no-prompt"
                            if 'args' in cmd_config:
                                modules[module_name][cmd]["args"] = []
                                for arg in cmd_config['args'].keys():
                                    modules[module_name][cmd]["args"].append(arg)
                                    sample_arg_line = sample_arg_line + f" --{module_name}_{arg} {arg}"
                            module_tests[module_name][cmd] = {
                                "enabled": False,
                                "example": sample_arg_line,
                                "note": "Add tests in the `tests` list below. Each test must be a valid RaidCloud command. Don't forget to add `--no-prompt`",
                                "tests": []
                            }
        
            # load tests
            tests_file_name = file_name.replace("module.json", "tests.json")
            # if False:
            if os.path.exists(tests_file_name):
                with open(tests_file_name) as f:
                    module_tests = json.load(f)
                    for module, commands in module_tests.items(): 
                        for command, test_info in commands.items():
                            if test_info["enabled"]:
                                modules[module][command]["tests"] = test_info["tests"]
                            else:
                                modules[module][command]["tests"] = []
                                
            else:
                if module_name in module_tests:
                    test_cases = {
                        module_name: module_tests[module_name]
                    }
                    # tests_file_name = f"./testing/integration/tests/{module_name}_tests.json"
                    with open(tests_file_name, 'w') as f:
                        json.dump(test_cases, f, indent=2)

        return modules
