#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

import boto3
from git.repo import Repo

from commands import crypto_utils
from server.console.template import template

with open('./config/version.json', 'r') as f:
    version = json.load(f)


with open('./config/modules_config.json', 'r') as f:
    modules_config = json.load(f)
    modules_parent_dir = modules_config["modules_parent_dir"]


def get_modules(base_dir="."):
    modules = {}
    for file_name in glob.glob(f"{base_dir}/commands/modules/*/module.json", recursive=True):
        file_name = file_name.replace("\\","/") # fixes windows issue
        module_name = file_name.split("/")[-2]
        modules[module_name] = file_name
    return modules


def copy(src_file, dest_file, print_suffix=""):
    print(f"{print_suffix}copy {src_file} -> {dest_file}")
    try:
        shutil.copy2(src_file, dest_file)
    except Exception as e:
        print(e)

def copy_tree(src_dir, dest_dir, print_suffix=""):
    print(f"{print_suffix}copytree {src_dir} -> {dest_dir}")
    try:
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    except Exception as e:
        print(e)


def rm(file_name):
    try:
        os.remove(file_name)
    except Exception as e:
        print(e)


def rm_dir(dir):
    try:
        shutil.rmtree(dir)
    except Exception as e:
        print(e)


def exec_cmd(cmd):
    print("")
    print(cmd)
    proc = subprocess.run(cmd, shell=True, check=True, env=os.environ.copy(), cwd=os.getcwd())
    return proc.returncode


def get_external_modules(args, OS, refresh=False):
    external_modules_file = "./temp/external_modules.json"
    if not refresh and os.path.exists(external_modules_file):
        with open(external_modules_file, 'r') as f:
            external_modules = json.load(f)
    else:
        external_modules = {
            "repos": {}
        }
    external_modules["timestamp"] = str(datetime.now())

    if args.pipeline:
        exec_cmd("mkdir ../rapid-cloud-custom-modules")
    for repo, v in version["module_repos"].items():
        print(repo, v)
        if repo not in external_modules["repos"]:
            external_modules["repos"][repo] = {}
        repo_info = external_modules["repos"][repo]
        repo_dir = f"{modules_parent_dir}/{repo}"

        if OS != "win" and not args.pipeline:
            if v == "master":
                exec_cmd(f"cd {repo_dir}; git fetch --all; git checkout master; git reset --hard origin/master")
            else:
                exec_cmd(f"cd {repo_dir}; git fetch --all; git reset --hard {v}")
        elif OS != "win" and args.pipeline:
            exec_cmd(f"git clone -b {v} git@bitbucket.org:rapid-cloud-by-kc/{repo}.git {repo_dir}")

        for module_name, file_name in get_modules(base_dir=repo_dir).items():
            if module_name != "skeleton":
                repo_info[module_name] = [
                    f"commands/modules/{module_name}",
                    "terraform/custom_templates"
                ]

                # collect all terraform modules, minus existing RapidCloud native modules
                for file_name in glob.glob(f"{repo_dir}/terraform/modules/*", recursive=True):
                    tf_module_name = file_name.split("/")[-1]
                    if not os.path.exists(f"./terraform/modules/{tf_module_name}"):
                        repo_info[module_name].append(file_name.replace(f"{repo_dir}/",""))

                # custom_server.py
                repo_info[module_name].append("server/custom_server.py")

    print(json.dumps(external_modules, indent=2))
    return external_modules


def add_external_modules(OS, skip):
    external_modules = get_external_modules(args, OS, refresh=True)

    # save external modules info so we can delete later
    exec_cmd("touch ./temp/external_modules.json")
    with open("./temp/external_modules.json", "w") as external_modules_file:
        json.dump(external_modules, external_modules_file, indent=2)

    print("\nTemporarily copying external modules")
    for repo, modules in external_modules["repos"].items():
        repo_dir = f"{modules_parent_dir}/{repo}"
        print(f"{repo} ({repo_dir})")
        for module_name, dirs in modules.items():
            module_dir = f"{repo_dir}/commands/modules/{module_name}"
            print(f"  - {module_name} ({module_dir})")
            for dir in dirs:
                src = f"{repo_dir}/{dir}"
                if dir != "server/custom_server.py":
                    dest = f"./{dir}".replace("/custom_templates", "/templates")
                    copy_tree(src, dest, "      - ")
                else:
                    dest = f"./{dir}".replace("custom_server.py", f"{module_name}_custom_server.py")
                    copy(src, dest, "      - ")
            if OS != "win":
                exec_cmd(f"ls -latr {dir}")


def remove_external_modules():
    if os.path.exists('./temp/external_modules.json'):
        with open('./temp/external_modules.json', 'r') as f:
            external_modules = json.load(f)
            for repo, modules in external_modules["repos"].items():
                repo_dir = f"{modules_parent_dir}/{repo}"
                for module_name, dirs in modules.items():
                    print(module_name)
                    for dir in dirs:
                        if "custom_templates" in dir:
                            for file_name in glob.glob(f"{repo_dir}/{dir}/*.j2"):
                                file_name = file_name.split("/")[-1]
                                file_name = f"./{dir}/{file_name}".replace("/custom_templates", "/templates")
                                print(f" - rm {file_name}")
                                rm(file_name)
                        elif dir != "server/custom_server.py":
                            print(f" - rmtree ./{dir}")
                            rm_dir(dir)
                        else:
                            file_name = f"./{dir}".replace("custom_server.py", f"{module_name}_custom_server.py")
                            print(f" - rm {file_name}")
                            rm(file_name)

    # remove untracked
    # "server/net_custom_server.py"
    # "terraform/modules/**"
    for untracked_file in git_untracked():
        if "_custom_server.py" in untracked_file or "terraform/modules/" in untracked_file:
            print(f"Removing {untracked_file}")
            rm(untracked_file)



def git_untracked():
    repo = Repo(".")
    print(repo)
    untracked = repo.untracked_files
    # print(json.dumps(untracked, indent=2))
    return untracked

def cleanup(args):
    try:
        # clean build folders
        print("")
        for dir in ["./build", "./dist", "./kc-rapid-cloud"]:
            try:
                print(f"removing {dir}")
                shutil.rmtree(dir)
            except Exception as e:
                print(f"\t{e}")

        # create dist structure
        dirs = [
            "dist/config/aws_profiles",
            "dist/config/azure_profiles",
            "dist/config/environments",
            "dist/config/gcp_profiles",
            "dist/data_scripts/kc_load_data_type_translation",
            "dist/logs",
            "dist/scripts",
            "dist/server/console/diagram",
            "dist/server/console/template",
            "dist/src",
            "dist/terraform/custom_templates",
            "dist/utils",
            "kc-rapid-cloud",
            "temp"
        ]
        print("")
        for dir in dirs:
            try:
                print(f"creating {dir}")
                os.makedirs(dir)
            except Exception as e:
                print(f"\t{e}")

    except Exception as e:
        print(e)


def pyinstaller(args, OS):
    try:
        sys.path.append('~/.cache/pip')
        datas = [('terraform/templates', 'terraform/templates')]
        hiddenimports = ['pymssql', 'commands.modules.trendmicro']
        for module_name, file_name in get_modules().items():
            datas.append((f"commands/modules/{module_name}/module.json", f"commands/modules/{module_name}"))
            hiddenimports.append(f"commands.modules.{module_name}")
            if os.path.exists(f"./server/{module_name}_custom_server.py"):
                hiddenimports.append(f"server.{module_name}_custom_server")

        # create kc.spec
        with open('kc.spec.template', 'r') as file :
        # with open('kc.spec.template', 'r') as file :
            kc_spec = file.read()
            kc_spec = kc_spec.replace('{{DATAS}}', str(datas)).replace('{{HIDDENIMPORTS}}', str(hiddenimports))
            # avoid temp dir for linux build when using pipeline arg
            if not args.pipeline:
                if OS == "amazon-linux":
                    kc_spec = kc_spec.replace("runtime_tmpdir=None", "runtime_tmpdir=\"/home/ec2-user/temp\"")
            with open('kc.spec', 'w') as file:
                file.write(kc_spec)

        # run pyinstaller
        # using pipeline arg to turn it into debug mode
        if args.debug:
            cmd = "pyinstaller --log-level=DEBUG kc.spec"
        else:
            cmd = "pyinstaller kc.spec"
        if not args.dry_run and OS != "win":
            exec_cmd(cmd)
        else:
            with open('pyinstaller.sh', 'w') as f:
                f.write(cmd)

    except Exception as e:
        print(e)


def pyinstaller_old(args, OS):
    try:
        add_data="--add-data terraform/templates:terraform/templates"
        hidden_imports = "--hidden-import pymssql"
        for module_name, file_name in get_modules().items():
            add_data += f" --add-data commands/modules/{module_name}/module.json:commands/modules/{module_name}"
            hidden_imports += f" --hidden-import commands.modules.{module_name}"
            if os.path.exists(f"./server/{module_name}_custom_server.py"):
                hidden_imports += f" --hidden-import server.{module_name}_custom_server"
        if OS == "win":
            add_data = add_data.replace(":", ";")

        collect_all = "--collect-all pyfiglet"
        log_level = "--log-level=FATAL"

        # run pyinstaller
        cmd = f"pyinstaller --clean {add_data} {hidden_imports} {collect_all} {log_level} kc --onefile"
        if not args.dry_run and OS != "win":
            exec_cmd(cmd)
        else:
            with open('pyinstaller.sh', 'w') as f:
                f.write(cmd)


    except Exception as e:
        print(e)


def copy_files(args, OS, SKIP_DISABLED_TEMPLATES):
    try:
        copy(f"server/upgrade-rapidcloud.sh", "dist/upgrade-rapidcloud.sh")
        copy("./build_tools/build_gitignore", "dist/.gitignore")
        copy("./config/version.json", "dist/config/version.json")
        copy("./config/kc_config.json", "dist/config/kc_config.json")
        copy("./config/modules_config.json", "dist/config/modules_config.json")
        copy("./data_scripts/kc_load_data_type_translation/data_type_translation.csv", "./dist/data_scripts/kc_load_data_type_translation/data_type_translation.csv")
        copy("./server/console.sh", "./dist/scripts/console.sh")
        copy("./scripts/amazon_linux_config.sh", "./dist/scripts/amazon_linux_config.sh")
        copy("./scripts/kc_run.sh", "./dist/scripts/kc_run.sh")
        copy("./server/custom_server.py", "./dist/server/custom_server.py")

        copy_tree("./docs", "./dist/docs")
        copy_tree("./data_scripts/job_templates", "dist/data_scripts/job_templates")
        copy_tree("./data_scripts/kc_streaming_glue_job_template", "dist/data_scripts/kc_streaming_glue_job_template")
        copy_tree("./commands/modules/skeleton", "dist/commands/modules/skeleton")
        copy_tree("./terraform/modules", "dist/terraform/modules")
        copy_tree("./terraform/tools", "dist/terraform/tools")
        copy_tree("./lambda", "./dist/lambda")
        copy_tree("./server/prod/app", "dist/server/app")

        # linux console restart script
        if os == "amazon-linux":
            copy("scripts/console.sh", "dist/console.sh")

        # default cloud context
        with open("dist/config/cloud_context.json", "w") as cloud_context_file:
            json.dump({
                "cloud": "aws",
                "supported_clouds": ["aws","azure","gcp"]
            }, cloud_context_file)

        # encrypt Jinja Templates
        if not os.path.exists("./temp/tf/templates"):
            os.makedirs("./temp/tf/templates")
        crypto_utils.encrypt_files("./terraform/templates/*.j2", "./temp/tf/templates")
        copy_tree("./temp/tf/templates", "dist/terraform/templates")

        # Multi-Cloud
        for cloud in ["aws", "azure", "gcp"]:
            template.generate_template(skip_disabled=SKIP_DISABLED_TEMPLATES, cloud=cloud)
            copy(f"./server/console/template/final_template_{cloud}.json", f"./dist/server/console/template/final_template_{cloud}.json")
            copy(f"./server/console/template/order_{cloud}.json", f"./dist/server/console/template/order_{cloud}.json")
            copy(f"./config/{cloud}_default_properties.json", f"dist/config/{cloud}_default_properties.json")
            copy(f"./config/{cloud}_default_profile.json", f"dist/config/{cloud}_profile.json")

            # Architecture Diagrams
            for diagram_type in ["solution", "lz", "net", "container"]:
                copy(f"./server/console/diagram/{cloud}_{diagram_type}_diagram.json", f"./dist/server/console/diagram/{cloud}_{diagram_type}_diagram.json")
                copy(f"./server/console/diagram/{cloud}_{diagram_type}_wizard.json", f"./dist/server/console/diagram/{cloud}_{diagram_type}_wizard.json")

    except Exception as e:
        print(e)


def zip_sign_and_upload(args, OS, VERSION, UPLOAD_LATEST):
    try:
        ZIP_FILE = f"kinect-rapid-cloud-{VERSION}-{OS}.zip"
        LATEST_ZIP_FILE = f"kinect-rapid-cloud-LATEST-{OS}.zip"
        DEV_ZIP_FILE = f"kinect-rapid-cloud-DEV-{OS}.zip"
        for zip_file in [ZIP_FILE, LATEST_ZIP_FILE, DEV_ZIP_FILE]:
            try:
                print(f"removing {zip_file}")
                os.remove(zip_file)
            except Exception as e:
                print(f"\t{e}")

        # sign binaries
        if OS == "macos" and not args.dry_run:
            exec_cmd("codesign --deep --force --options=runtime --entitlements ./build_tools/entitlements.plist --sign D90C376A88CE25FC059836A30A03872D81BDB8B6 --timestamp ./kc-rapid-cloud/kc")
        # elif OS == "win":
        #     if input(f"\nDid you sign kc.exe? [yes, no]: ") != 'yes':
        #         return

        # create zip
        shutil.make_archive(ZIP_FILE.replace(".zip",""), 'zip', root_dir=".", base_dir="kc-rapid-cloud")

        # notarize bundle for macos
        if OS == "macos" and not args.dry_run:
            exec_cmd(f'xcrun notarytool submit {ZIP_FILE} --keychain-profile "rapid-cloud-dev-profile" --wait')

        # upload zip files to S3
        if OS == "win" or not args.dry_run and input(f"\nUpload to S3 [yes, no]: ") == 'yes':
            print("")
            print(f"Uploading {ZIP_FILE}")

            s3_client = boto3.client('s3')
            s3_resource = boto3.resource('s3')
            bucket = "kinect-rapid-cloud"
            extra_args={'ACL': 'public-read'}

            s3_client.upload_file(ZIP_FILE, "kinect-rapid-cloud", f"downloads/{ZIP_FILE}", ExtraArgs=extra_args)

            if UPLOAD_LATEST:
                target_file = LATEST_ZIP_FILE
            else:
                target_file = DEV_ZIP_FILE

            print("")
            print(f"Copying {ZIP_FILE} to {target_file}")
            s3_resource.Bucket(bucket).copy({"Bucket": bucket, "Key": f"downloads/{ZIP_FILE}"}, f"downloads/{target_file}", ExtraArgs=extra_args)

    except Exception as e:
        print(e)


def build(args):
    OS = args.os
    VERSION = version["version"]
    UPLOAD_LATEST = args.upload_latest
    SKIP_DISABLED_TEMPLATES = args.skip_disabled_templates
    BUILD_STAGE = args.build_stage
    NO_PROMPT = args.no_prompt
    PIPELINE = args.pipeline

    if not args.dry_run and BUILD_STAGE in ["all"]:
        if not NO_PROMPT:
            if input(f"Do you want to build RapidCloud {OS} v{VERSION} [yes, no]: ") != 'yes':
                return

        if OS == "macos":
            if input(f"Did you create Production Console App? [yes, no]: ") != 'yes':
                return

    try:
        if OS != "win" and BUILD_STAGE == "all" or BUILD_STAGE == "cleanup":
            # avoid removing external modules and cleanup when using pipeline argument
            if not args.pipeline:
                remove_external_modules()
            cleanup(args)

        # bring in modules from other repos
        if not args.skip_tf_modules:
            if OS != "win" and BUILD_STAGE == "all" or BUILD_STAGE == "add_external_modules":
                add_external_modules(args, OS)

        # prepare pyinstaller arguments
        if OS != "win" and BUILD_STAGE == "all" or BUILD_STAGE == "pyinstaller":
            pyinstaller(args, OS)

        # copy required files
        if OS != "win" and BUILD_STAGE == "all" or BUILD_STAGE == "copy_files":
            copy_files(args, OS, SKIP_DISABLED_TEMPLATES)

        copy_tree("./dist", "./kc-rapid-cloud")

        # build zip files (version specific and latest)
        # using pipeline arg to avoid zip sign and upload
        if (OS != "win" and (BUILD_STAGE == "all" or BUILD_STAGE == "zip_sign_and_upload")) and not PIPELINE:
            zip_sign_and_upload(args, OS, VERSION, UPLOAD_LATEST)

    except Exception as e:
        print(e)

    # avoid removing and cleaning up when using pipeline arg
    finally:
        # remove all external modules
        if not args.dry_run and BUILD_STAGE in ["all", "zip_sign_and_upload"] and not PIPELINE:
            remove_external_modules()



if __name__ == "__main__":
    # production build:
    '''
    python build.py --action build --os macos --skip_disabled_templates --build_stage all --upload_latest
    '''

    # dev build only (does not upload LATEST bundle):
    '''
    python build.py --action build --os macos --skip_disabled_templates --build_stage all
    '''

    # dry run - skip building, notarizing and uploading
    '''
    python build.py --action build --os macos --skip_disabled_templates --build_stage all --dry_run
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help="Accepted values are [build]")
    parser.add_argument('--os', help="Accepted values are [macos] [amazon-linux]")
    parser.add_argument('--upload_latest', action='store_true')
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('--skip_disabled_templates', action='store_true')
    parser.add_argument('--skip_tf_modules', action='store_true')
    parser.add_argument('--local_testing', action='store_true')
    parser.add_argument('--build_stage', help="Accepted values are [all] [cleanup] [add_external_modules] [pyinstaller] [copy_files] [zip_sign_and_upload]")
    parser.add_argument('--no-prompt', action='store_true', help="Run process unattendend")
    parser.add_argument('--pipeline', action='store_true', help="Avoid prompts and cleanups to run process on a CI system")
    parser.add_argument('--debug', action='store_true', help="Adds debug level to pyinstaller execution")
    args = parser.parse_args()

    if args.action == "build":
        build(args)
    # elif args.action == "get_external_modules":
    #     get_external_modules()
    # elif args.action == "add_external_modules":
    #     add_external_modules()
    # elif args.action == "remove_external_modules":
    #     remove_external_modules()
    # elif args.action == "git_untracked":
    #     git_untracked()
