#!/usr/bin/env python3
import json
import pprint
import re
import subprocess
import sys
import time
import os
import argparse
import textwrap
import tempfile



def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
                This script will clone repos from KC's bitbucket,
                into the RapidCloud framework terraform template folder.
                It runs in DRY MODE and will require a --exec switch to be executed
        '''))
    parser.add_argument('--exec', action='store_true', required=False, help="Print Extra info")
    args = parser.parse_args()
    dry_run = False if args.exec else True
    return  dry_run


def main():
    dry_run = get_args()
    staging_folder = tempfile.TemporaryDirectory(prefix='Theia')
    template_folder = 'templates'
    modules_folder = 'modules'
    sources = json.loads(open('{}/sources.json'.format(template_folder)).read())

    for module, module_source in sources.items():
        if 'git' in module_source:
            repo_url, repo_path = module_source.split('.git')
            _, _, bbhost, bbns, gitrepo = repo_url.split('/')
            path, tag = repo_path.split('?ref=')
            if re.match('^\/\/', path):
                subfolder = path.replace('//', '')
            else:
                subfolder = ''
            print('*** will clone {repo} to {staging_folder} and move {subfolder} to {modules_folder}/{module}'.format(
                staging_folder=staging_folder.name,
                repo=gitrepo,
                subfolder=subfolder,
                modules_folder=modules_folder,
                module=module
            ))

            # git clone the repo/tag
            print('*** cloning  ')
            cmd = 'git -c advice.detachedHead=false clone -b {tag} {host}:{ns}/{repo}.git {staging_folder}/{module}'.format(
                tag=tag,
                host=bbhost,
                ns=bbns,
                repo=gitrepo,
                staging_folder=staging_folder.name,
                module=module
            )
            print('--- {}'.format(cmd))
            if not dry_run:
                proc = subprocess.run(cmd, shell=True, check=True)

            print('*** move to modules  ')
            cmd = 'rm -rvf {modules_folder}/{module} && mv {staging_folder}/{module}/{subfolder} {modules_folder}/{module} && rm -rf {modules_folder}/{module}/.git'.format(
                staging_folder=staging_folder.name,
                subfolder=subfolder,
                modules_folder=modules_folder,
                module=module
            )
            print('--- {}'.format(cmd))
            if not dry_run:
                proc = subprocess.run(cmd, shell=True, check=True)

            print('====================================================')

            if dry_run:
                print('This was a DRY RUN !!!')
                print('To execute, run with --exec switch')

if __name__ == "__main__":
    main()
