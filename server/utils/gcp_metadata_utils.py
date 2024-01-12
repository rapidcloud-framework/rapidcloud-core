#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import json
import logging
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

from googleapiclient import discovery

from commands import print_utils
from commands.kc_metadata_manager.profile_manager import get_profile_manager

logger = logging.getLogger("gcp_metadata_utils")
logger.setLevel(logging.INFO)


def get_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    logger.info("in gcp_metadata_utils.get_data")
    mock = copy.deepcopy(MOCK_ENV)
    if params["table_name"] == "profile":
        for diagram_type in ["lz", "net", "solution"]:
            file_name = f'./server/console/diagram/gcp_{diagram_type}_wizard.json'
            if os.path.exists(file_name):
                with open(file_name) as f:
                    mock[f"gcp_{diagram_type}_wizard"] = json.load(f)
    return [mock]


def get_form_data(kc_args, session, request, filters, params, dev_or_live, email=None, args=None):
    return []


# Get the gcloud CLI's current configuration profile name by executing:
#       gcloud config configurations list --filter=is_active:True --format="value(name)"
# Ref:
#   - https://cloud.google.com/sdk/docs/configurations
def get_gcloud_cli_configuration_name():
    # The last array element (i.e., '--format=value(name)') does NOT quote the part after the equal sign (=).
    # Such quotes are only needed when running interactively in a shell in order to
    # prevent the shell from treating the round brackets as special characters.
    # Our Python call to subprocess.run() isn't spawning a shell.
    run_args = ['gcloud', 'config', 'configurations', 'list', '--filter=is_active:True', '--format=value(name)']
    print_utils.info("{}".format(' '.join(run_args)))

    output = subprocess.run(run_args, stdout=PIPE, stderr=STDOUT, text=True, encoding='utf-8')
    print_utils.info(f"gcloud returncode={output.returncode}, stdout={output.stdout}")
    if output.returncode == 0:
        return output.stdout.strip()
    else:
        # Without 'gcloud', the other way is to set the env var GOOGLE_APPLICATION_CREDENTIALS
        google_application_credentials_env_var = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if google_application_credentials_env_var:
            print_utils.info(f"Using GOOGLE_APPLICATION_CREDENTIALS={google_application_credentials_env_var} because you don't have a gcloud profile.")
            return None
        else:
            raise RuntimeError(f"gcloud failed (and you don't have GOOGLE_APPLICATION_CREDENTIALS): returncode={output.returncode}, stdout/stderr={output.stdout}")


def get_gcloud_cli_project_id():
    run_args = ['gcloud', 'config', 'list', '--format=value(core.project)']
    print_utils.info("{}".format(' '.join(run_args)))

    output = subprocess.run(run_args, stdout=PIPE, stderr=STDOUT, text=True, encoding='utf-8')
    print_utils.info(f"gcloud returncode={output.returncode}, stdout={output.stdout}")
    if output.returncode == 0:
        return output.stdout.strip()
    else:
        raise RuntimeError(f"gcloud failed: returncode={output.returncode}, stdout/stderr={output.stdout}")

def get_gcloud_cli_region():
    run_args = ['gcloud', 'config', 'list', '--format=value(compute.region)']
    print_utils.info("{}".format(' '.join(run_args)))

    output = subprocess.run(run_args, stdout=PIPE, stderr=STDOUT, text=True, encoding='utf-8')
    print_utils.info(f"gcloud returncode={output.returncode}, stdout={output.stdout}")
    if output.returncode == 0:
        return output.stdout.strip()
    else:
        raise RuntimeError(f"gcloud failed: returncode={output.returncode}, stdout/stderr={output.stdout}")

def get_first_vpc_id(project_id: str=None) -> str:
    if not project_id:
        project_id = get_profile_manager().get_env_project_id()

    run_args = ['gcloud', 'compute', 'networks', 'list', '--format=value(name)', '--limit=1']
    if project_id:
        run_args.append(f'--project={project_id}')

    print_utils.info("{}".format(' '.join(run_args)))

    output = subprocess.run(run_args, stdout=PIPE, stderr=STDOUT, text=True, encoding='utf-8')
    print_utils.info(f"gcloud returncode={output.returncode}, stdout={output.stdout}")
    if output.returncode == 0:
        return output.stdout.strip()
    else:
        raise RuntimeError(f"gcloud failed: returncode={output.returncode}, stdout/stderr={output.stdout}")


def get_gcp_environment_config(env):
    if not env:
        logger.info(f"get_gcp_environment_config(): 'env' is None.")
        return {}

    filename = f"./config/environments/{env}_config.json"

    try:
        with open(filename, 'r') as f:
            env_config= json.load(f)
            return env_config
    except FileNotFoundError as e:
        logger.error(e)
        return None


def get_all_gcp_environments():
    filename = './config/all_gcp_profiles.json'
    try:
        with open(filename, 'r') as f:
            envs = json.loads(f.read())
            return envs
    except FileNotFoundError as e:
        logger.info(e) # It's OK
        return {}


def save_environment(env, project_id):
    assert project_id, "project_id should not be null in save_environment()."
    envs = get_all_gcp_environments()
    envs[env] = project_id
    with open('./config/all_gcp_profiles.json', 'w') as f:
        json.dump(envs, f, indent=2)

def get_gcp_service_api_state(api_name: str, project_id: str=None) -> str:
    if not project_id:
        project_id = get_profile_manager().get_env_project_id()

    assert project_id, "project_id should not be null in get_gcp_service_api_state()."
    assert api_name,   "api_name should not be null in get_gcp_service_api_state()."

    api_name = ensure_google_api_suffix(api_name)

    # https://stackoverflow.com/questions/57526808/how-do-you-enable-gcp-apis-through-the-python-client-library/76047799#76047799
    # https://bitbucket.org/kinect-consulting/kinect-theia-main/annotate/f45ad8de688846c36947754ca6a28482b73cd448/README.md?at=master#README.md-47
    #
    # The 'service' object is of datatype 'googleapiclient.discovery.Resource':
    #   - docs: https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery.Resource-class.html
    #   - src:  https://github.com/googleapis/google-api-python-client/blob/585d11392a1721a3fbdca6a2f8e190e71fa55f26/googleapiclient/discovery.py#L1342-L1547
    service = discovery.build("serviceusage", "v1")

    try:
        services = service.services() # The method name 'services()' refers to the name ('services') of this REST API: https://cloud.google.com/service-usage/docs/reference/rest/v1/services

        # The method name 'get()' refers to this verb: https://cloud.google.com/service-usage/docs/reference/rest/v1/services#get
        # Sidebar: The docs and src listed above for googleapiclient.discovery.Resource don't have a statically-defined method 'get()';
        #          rather, the get() method is dynamically defined by Python at this line:
        #               - https://github.com/googleapis/google-api-python-client/blob/585d11392a1721a3fbdca6a2f8e190e71fa55f26/googleapiclient/discovery.py#L1043
        #          which is called by:
        #               - https://github.com/googleapis/google-api-python-client/blob/585d11392a1721a3fbdca6a2f8e190e71fa55f26/googleapiclient/discovery.py#L1408
        #
        # I have dug deep into the GCP library code in order to determine that it doesn't encapsulate any implicit project_id.
        # Therefore, we must explicitly supply the project_id as we do next.
        request = services.get(
            name=f"projects/{project_id}/services/{api_name}" # This param refers to the field 'name' in the above REST API. The string's format is documented there, too.
        )
        response = request.execute()
    finally:
        service.close() # https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md#build-the-service-object

    return response.get('state')


def enable_gcp_service_apis(api_name_list: list[str], project_id: str=None) -> None:
    if not project_id:
        project_id = get_profile_manager().get_env_project_id()

    for api_name in api_name_list:
        enable_gcp_service_api(api_name, project_id)


def enable_gcp_service_api(api_name: str, project_id: str=None) -> None:
    if not project_id:
        project_id = get_profile_manager().get_env_project_id()

    state = get_gcp_service_api_state(api_name, project_id)
    if state == 'DISABLED':
        do_enable_gcp_service_api(api_name, project_id)


def do_enable_gcp_service_api(api_name: str, project_id: str=None) -> None:
    if not project_id:
        project_id = get_profile_manager().get_env_project_id()

    api_name = ensure_google_api_suffix(api_name)

    service = discovery.build("serviceusage", "v1")

    try:
        # See get_gcp_service_api_state() for comments on how this GCP API works.
        request = service.services().enable(
            name=f"projects/{project_id}/services/{api_name}"
        )

        print_utils.info(f"Enabling the GCP API '{api_name}' in project '{project_id}' ...")

        # If no 'HttpError' thrown in the following call, it means success.
        # https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md#execution-and-response
        response = request.execute()
    finally:
        service.close()


def ensure_google_api_suffix(api_name: str) -> str:
    if not api_name.endswith(".googleapis.com"):
        api_name += ".googleapis.com"

    return api_name
