#!/usr/bin/env python3

import glob
import json
import argparse
import textwrap
import pprint
import os
from os.path import exists
import sys
import boto3
from datetime import datetime
from jinja2 import Template
from boto3.dynamodb.conditions import Attr
import subprocess
import shutil
import traceback
from botocore.exceptions import ClientError
from commands import crypto_utils


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DATE_FORMAT = '%Y-%m-%d'

templates_and_modules = {}

with open('./config/version.json', 'r') as f:
    rc_version = json.load(f)['version']

with open('./config/kc_config.json', 'r') as f:
    kc_config = json.load(f)

def get_boto3_session():
    return boto3.Session(profile_name=os.environ["AWS_PROFILE"], region_name=os.environ["AWS_REGION"])

def is_linux_based():
    return sys.platform.lower() in ['darwin', 'linux']

def get_args():
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\
            This script supports the following actions:
            - init: create terraform resource files from the provided table & downloads terraform modules
            - plan: runs a terraform plan (implies init)
            - apply: creates infrastructure (implies init)
            - destroy: destroys infrastructure (implies init)
         '''))
    parser.add_argument('--table', required=True, help="The dynamo table to query (probably aws_infra)")
    parser.add_argument('--profile', required=True, help="Theia environment name")
    parser.add_argument('--action', required=True, help='action to execute {consume|init|plan|apply|destroy}')
    parser.add_argument('--debug', action='store_true', required=False, help="Print Extra info")
    parser.add_argument('--no-prompt', action='store_true', required=False, help="Print Extra info")
    args = parser.parse_args()
    return args.table, args.profile, args.debug, args.action, args.no_prompt


def get_profile_info(profile):
    try:
        response = get_boto3_session().resource('dynamodb').Table('profile').get_item(Key={'name': profile})
        return response['Item']
    except ClientError as e:
        print(e.response['Error']['Message'])


def get_template_file_contents(args, resource_type, replace_path, subscription_tier, use_includes=True):
    '''
    this function reads j2 template file from either explicit file path or from bundled data
    It also provides include template functionality
    '''

    file_contents, templ_path, module_path = None, None, None
    print(" - " + f"getting {resource_type}")
    # dev mode or custom modules outside RC binary
    if resource_type in templates_and_modules:
        if "template" in templates_and_modules[resource_type]:
            templ_path = templates_and_modules[resource_type]["template"]
            print("   - template: " + templ_path)
        if "module" in templates_and_modules[resource_type]:
            module_path = templates_and_modules[resource_type]["module"]
            print("   - module: " + module_path)
        elif os.path.exists(f"./terraform/modules/{resource_type}"):
            module_path = os.path.abspath(f"./terraform/modules/{resource_type}")
            print("   - module: " + module_path)
        else:
            print("   - no module found")

    read_templ_path = False
    if templ_path is not None:
        if "custom_templates" in templ_path and subscription_tier in ["2","3"]:
            read_templ_path = True
        elif "custom_templates" not in templ_path:
            read_templ_path = True

    if read_templ_path and exists(templ_path):
        with open(templ_path, "r") as file:
            file_contents = file.read()

    if file_contents is None:
        # dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        # replace_path_win = replace_path.replace("/","\\")
        # dir = dir.replace(replace_path, "/").replace(replace_path_win, "\\")
        dir = "."
        path_to_file_dft = os.path.abspath(os.path.join(dir, f"terraform/templates/{resource_type}.j2"))
        path_to_file_encrypted = f"{path_to_file_dft}.encrypted"

        if exists(path_to_file_encrypted):
            print("   - template (encrypted): " + path_to_file_encrypted)
            file_contents = crypto_utils.read_encrypted_file(path_to_file_encrypted)
        elif exists(path_to_file_dft):
            print("   - template (dft): " + path_to_file_dft)
            with open(path_to_file_dft, "r") as file:
                file_contents = file.read()

        if module_path is None:
            if os.path.exists(f"./terraform/modules/{resource_type}"):
                module_path = os.path.abspath(f"./terraform/modules/{resource_type}")
                print("   - module: " + module_path)
            else:
                print("   - no module found")

    contents = ""
    start = 0

    if file_contents:
        # Include example: {{ "include/templates/sns_topic.j2" }}
        while use_includes:
            start = file_contents.find("include/templates/", start + 1)
            if start != -1:
                end = file_contents.find("\" }}", start)
                include_resource_type = file_contents[start + 7: end].split("/")[-1]
                include_contents, module_path = get_template_file_contents(args, include_resource_type, replace_path, subscription_tier, use_includes=True)
                if include_contents:
                    file_contents = f"{file_contents[0:start - 4]}{include_contents}{file_contents[end + 4:]}"
            else:
                use_includes = False

        contents = contents + file_contents

    if module_path:
        module_path = module_path.replace("\\","/") # fixes windows issue
    return contents, module_path


def create_resource_definition(args, profile_name, tmpl_file, params, base_path, resource_type, new_file=False):
    '''
    append to *.tf file from *.j2 template and parameters
    '''
    profile_path = os.path.join(base_path, profile_name)
    file_path = f'{profile_path}/_kc_{resource_type}.tf'
    resource_file = open(file_path, 'a')
    if new_file:
        resource_file.write(f'###\n')
        resource_file.write(f'### This file was generated by RapidCloud v{rc_version}\n')
        resource_file.write(f'### {datetime.now().strftime(DATETIME_FORMAT)}\n')
        resource_file.write(f'###\n\n\n')
    resource_file.write('###\n')
    resource_name = None
    if 'resource_name' in params:
        resource_name = params['resource_name']
        resource_file.write(f"### {resource_type}: {resource_name}\n")
    else:
        resource_file.write(f"### {resource_type}\n")
    resource_file.write('###\n')

    try:
        params["utils_version"] = kc_config['utils']['version']
        params["rapid_cloud_user"] = args.current_session_email if args.current_session_email else args.caller_arn if args.caller_arn else "rapid-cloud"
        params["rapid_cloud_version"] = rc_version
        if 'profile' in params:
            params["fully_qualified_name"] = f"{params['profile']}_{params['resource_name']}_{params['resource_type']}"
        if params.get("resource_type", "") == "lambda_layer":
            print(params["region"])
    except Exception as e:
        traceback.print_exc()
        pass

    try:
        for param in ["workload", "rapid_cloud_user", "rapid_cloud_version"]:
            print(f"{param} = {params[param]}")
        jinja_template = Template(tmpl_file)
        rendered_jinja_template = jinja_template.render(params)
        resource_file.write('\n')
        resource_file.write(rendered_jinja_template)
        resource_file.write('\n\n')
        resource_file.close()
    except FileNotFoundError as e:
        traceback.print_exc()
        pass

    print(" - " + f'saved: {file_path}')


def init_tf_base_resources(args, profile_name, env_info, base_path, subscription_tier, debug=False):
    '''
    base resources are default resources that are created regardless of dynamoDB defentions
    they use the same logic as create_resource however the <resource_type> is hardcoded in
    the base_items variable
    '''

    if (args.cloud == "aws"):
        base_items = ['aws_backend', 'vpc_data', 'glue_base', 'theia_roles', 'lambda_function_base']
    elif (args.cloud == "azure"):
        base_items = ['az_backend']
    elif (args.cloud == "gcp"):
        base_items = ['gcp_backend']
    else:
        raise RuntimeError(f"Unexpected cloud provider: '{args.cloud}'")

    print("\n\n-----------------------------------------------------------------")
    print(f"creating definitions for {len(base_items)} base resources ...")
    print("-----------------------------------------------------------------\n")

    for resource_type in base_items:
        print(f"\n{resource_type}")
        tmpl_file, module_path = get_template_file_contents(args, resource_type, "/terraform/bin", subscription_tier)
        if not tmpl_file:
            print(f"No base_items template found for resource_type='{resource_type}', skipping.")
            traceback.print_stack()
            continue

        env_info['module_source'] = module_path
        create_resource_definition(args, profile_name, tmpl_file, env_info, base_path, resource_type, new_file=True)


def init_tf_resources(args, profile_name: str, response_items: dict, base_path: str, subscription_tier, debug: bool=False) -> None:
    '''
    this function will collect all resource types and create
    an empty file matching the resources, the rest of the code
    will append to this file
    '''

    print("\n\n-----------------------------------------------------------------")
    print(f"initializing {len(response_items)} environment resource types ...")
    print("-----------------------------------------------------------------\n")

    profile_path = '{}/{}'.format(base_path, profile_name)
    items = set()
    for item in response_items:
        items.add(item['resource_type'])
        item['profile_dashed'] = item['profile'].replace('_', '-')

    for resource_type in items:
        print("\n" + resource_type)
        tf_file_name = '{}/_kc_{}.tf'.format(profile_path, resource_type)
        try:
            os.remove(tf_file_name)
        except FileNotFoundError:
            next

        tmpl_file, module_path = get_template_file_contents(args, resource_type, "/terraform/bin", subscription_tier)
        if tmpl_file:
            os.makedirs(os.path.dirname(tf_file_name), exist_ok=True)
            f = open(tf_file_name, 'w+')
            f.write(f'###\n')
            f.write(f'### This file was generated by RapidCloud v{rc_version}\n')
            f.write(f'### {datetime.now().strftime(DATETIME_FORMAT)}\n')
            f.write(f'###\n\n\n')
            f.close() # So far, we've only written the header comment without any real terraform code.
        else:
            print(f"No tf resource template found for resource_type='{resource_type}' in templates folder")
            traceback.print_stack()

def init_tf_create_definition(args, profile_name: str, profile_details: dict, items: list[dict], base_path: str, subscription_tier: str, debug=False) -> None:
    for item in items:
        if 'custom' not in item or not item['custom']:
            print(f"\n{item['resource_type']}:")
            print(f" - {item['fqn']}")
            if debug:
                pprint.pprint(item['params'])

            # add profile info to each item
            item.update(profile_details)
            create_resource(args, profile_name, item, base_path, subscription_tier, debug)
        else:
            print(f"\n{item['resource_type']} (custom):")
            print(f" - {item['fqn']}")

def create_resource(args, profile_name, item, base_path, subscription_tier, debug=False):
    '''
    this function creates a resource definition in the profile folder
    1. checks if a template_file called item['resource_type].j2 exists ( for example lambda_function.j2 )
    2. if the template file exists:
        - render the jinja template
        - append the rendered template to _kc_<resource_type>.tf
    '''
    tmpl_file, module_path = get_template_file_contents(args, item['resource_type'], "/terraform/bin", subscription_tier)
    if tmpl_file:
        item['module_source'] = module_path
        create_resource_definition(args, profile_name, tmpl_file, item, base_path, item['resource_type'])

def consume(args, profile_details, items, profile_name, base_path, subscription_tier, debug=False):
    '''
    consume will do the following:
    1. create the dms roles (dms_main)
    2. initiate the base tf resources (init_tf_base_resources)
    3. create empty files with all the resource types defined in dynamoDb, this is done to ensure deleted resources are removed.
       basicly we're re-creating the resource files from scrarch on each init run
    4. items is the list of resources pulled from the dynamodb table, we loop over them and for each resource we:
       - append profile_details to the item, profile_details adds 2 items:
            1. name_dashed, a lot of aws resource do not support _, so we add a name parameter with -
            2. arn_prefix, this is done to acomodate for regular vs gov arns, if the region contains "gov" we set the arn
               prefix to arn:aws-us-gov
    5. we then pass the item with the updated info to create_resources, which creates the resource definition based on the resource_type.j2
       template
    '''

    if (args.cloud == "aws"):
        dms_main(profile_details)

    # create base resources
    init_tf_base_resources(args, profile_name, profile_details, base_path, subscription_tier)

    # initialize empty files for each resource
    init_tf_resources(args, profile_name, items, base_path, subscription_tier)

    print("\n\n-----------------------------------------------------------------")
    print(f"creating definitions for {len(items)} environment resource types ...")
    print("-----------------------------------------------------------------\n")

    init_tf_create_definition(args, profile_name, profile_details, items, base_path, subscription_tier, debug)

    print("\n\n")


def dms_create_role(iam, role_name, policy_doc, policy_arn):
    ''' created a dms role in aws '''
    try:
        role = iam.create_role(RoleName=role_name,AssumeRolePolicyDocument=policy_doc)
        print('role {} created'.format(role_name))
        if not dms_attach_policy(iam, role_name, policy_arn):
            raise('errors attaching policy')
        return True
    except iam.exceptions.EntityAlreadyExistsException:
        print('role {} exists'.format(role_name))
        if not dms_attach_policy(iam, role_name, policy_arn):
            raise('errors attaching policy')
        return True
    except Exception as e:
        print(e)
        return False


def dms_attach_policy(iam, role_name, policy_arn):
    ''' attach policy to the dms role '''
    r = iam.list_attached_role_policies(RoleName=role_name)
    for policy in r['AttachedPolicies']:
        if policy['PolicyArn'] == policy_arn:
            return True
    try:
        print('attaching policy {} to {}'.format(policy_arn, role_name))
        response = iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        return True
    except Exception as e:
        print(e)
        return False


def dms_main(profile_details):
    ''' create the default dms roles needed '''
    iam = get_boto3_session().client('iam')
    dms_cw_role_name = "dms-cloudwatch-logs-role"
    dms_cw_role_policy_arn = "{}:iam::aws:policy/service-role/AmazonDMSCloudWatchLogsRole".format(profile_details['arn_prefix'])
    dms_cw_role_policy_doc = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
            "Service": "dms.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        },
        {
            "Effect": "Allow",
            "Principal": {
            "Service": "redshift.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
        ]
    })

    dms_vpc_role_name = 'dms-vpc-role'
    dms_vpc_role_policy_arn = "{}:iam::aws:policy/service-role/AmazonDMSVPCManagementRole".format(profile_details['arn_prefix'])
    dms_vpc_role_policy_doc = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
            "Service": "dms.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
        ]
    })
    dms_create_role(iam, dms_vpc_role_name, dms_vpc_role_policy_doc, dms_vpc_role_policy_arn)
    dms_create_role(iam, dms_cw_role_name, dms_cw_role_policy_doc, dms_cw_role_policy_arn)


def run(action, profile_name, base_path):
    action_split = action.split(' ')[0]
    env_vars = os.environ.copy()
    print(f"base_path: {base_path}")
    print(f"profile_name: {profile_name}")
    profile_path = os.path.join(base_path, profile_name)
    print(f"profile_path: {profile_path}")

    #log_file_name = os.path.join(f'{profile_path}', f'{action_split}.log')
    log_file_name = f'{action_split}.log'
    print(f"log_file: {log_file_name}")
    log_file = open(log_file_name, "w+")

    if is_linux_based():
        cmd = f'terraform {action} | tee -a {log_file_name}'
    else:
        terraform_exe = os.environ['TERRAFORM_EXE']
        cmd = f"{terraform_exe} {action}"
    print(f"\nrunning `{cmd}` ...\n")

    if is_linux_based():
        proc = subprocess.run(cmd, shell=True, check=True, env=env_vars, cwd=profile_path)
    else:
        proc = subprocess.run(cmd, shell=True, env=env_vars, cwd=profile_path, stdout=log_file, stderr=subprocess.STDOUT)

    if action_split in ['init', 'plan']:
        print("\n-----------------------------------------------------------------------------")
        print(f"Terraform modules for environment `{profile_name}` are in `./terraform/{profile_name}`\n")
        proc = subprocess.run(f"ls {profile_path}", shell=True)
        print(f"\n\nTerraform {action_split} log:\n./terraform/{profile_name}/{action_split}.log")
        print("-----------------------------------------------------------------------------\n")


def load_templates_and_modules(args):
    checked = []
    for cloud, dirs in args.modules_dirs.items():
        for module_name, dir in dirs.items():
            dir = dir + "/"
            module_repo_root = dir.replace("/./","/").replace("/" + module_name + "/", "").replace("/commands/modules", "")
            print(module_name, dir)
            print("  ", module_repo_root)

            # dev mode or custom modules only (module repos outside RC binary)
            if "_MEI" not in module_repo_root and module_repo_root not in checked:
                for template_dir in ["custom_templates", "templates"]:
                    for file_path in glob.glob(f"{module_repo_root}/terraform/{template_dir}/*.j2"):
                        file_path = file_path.replace("\\","/") # fixes windows issue
                        resource_type = file_path.split("/")[-1].replace(".j2","")
                        if resource_type not in templates_and_modules:
                            templates_and_modules[resource_type] = {}
                        templates_and_modules[resource_type]["template"] = file_path

                if os.path.exists(f"{module_repo_root}/terraform/modules"):
                    for resource_type in os.listdir(f"{module_repo_root}/terraform/modules"):
                        d = os.path.join(f"{module_repo_root}/terraform/modules", resource_type)
                        if os.path.isdir(d):
                            if resource_type not in templates_and_modules:
                                templates_and_modules[resource_type] = {}
                            templates_and_modules[resource_type]["module"] = d

                checked.append(module_repo_root)

    if os.getenv('RAPIDCLOUD_TEST_MODE') == "true":
        print("MODULE ROOTS:")
        print(json.dumps(checked, indent=2))
        print("\nTERRAFORM TEMPLATES AND MODULES:")
        print(json.dumps(templates_and_modules, indent=2))

def main(args, profile_details, items, profile_name, action, subscription_tier, no_prompt=False, debug=False):
    '''
    This function executes the main code depending on what the --action is
    '''

    load_templates_and_modules(args)

    base_path = os.getenv('terraform_dir', default = '.')
    if '\\' in base_path: # windows
        base_path = base_path.replace("/", "\\")
    profile_path='{}/{}'.format(base_path, profile_name)
    if os.path.isdir(profile_path):
        try:
            os.environ['skip_cleanup']
            print('skipping deletion of existing profile folder since skip_cleanup var was provided')
            pass
        except KeyError:
            print('deleting existing profile folder {}'.format(profile_path))
            print('you can skip this when developing by setting as `"skip_cleanup\" env var`')
            shutil.rmtree(profile_path)

    os.makedirs(profile_path, exist_ok=True)

    if action in ['init', 'consume']:
        consume(args, profile_details, items, profile_name, base_path, subscription_tier, debug)
        run('init -no-color', profile_name, base_path)
    elif action in ['plan']:
        consume(args, profile_details, items, profile_name, base_path, subscription_tier, debug)
        run('init -no-color', profile_name, base_path)
        run('{} -no-color'.format(action), profile_name, base_path)
    elif action in ['apply', 'plan', 'destroy']:
        consume(args, profile_details, items, profile_name, base_path, subscription_tier, debug)
        run('init -no-color', profile_name, base_path)
        if no_prompt:
            run('{}  -no-color -auto-approve -input=false'.format(action), profile_name, base_path)
        else:
            run('{} -no-color'.format(action), profile_name, base_path)
    else:
        print('unknown action, please derfer to --help')
