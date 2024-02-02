__author__ = "Igor Royzis"
__license__ = "MIT"


import logging
import os
import sys
import json
import boto3
from os.path import exists
from azure.common.client_factory import get_client_from_cli_profile
from azure.common.credentials import get_cli_profile
from azure.mgmt.subscription import SubscriptionClient
from azure.identity import DefaultAzureCredential
from commands import config_utils
from commands import boto3_utils

import google.auth


from commands import print_utils
from commands.colors import colors
from server.utils.azure_environment_utils import AzureConfigUtils

TIERS = {
    "1": "FREE (1)",
    "2": "PREMIUM (2)",
    "3": "ADMIN (3)"
}

API = {
    "lic_dev_url":    "https://zo4sdqhv0b.execute-api.us-east-1.amazonaws.com/dev",
    "lic_live_url":   "https://xpqa1tj4sa.execute-api.us-east-1.amazonaws.com/live",
    "admin_dev_url":  "https://6cvjw1hoe1.execute-api.us-east-1.amazonaws.com/dev",
    "admin_live_url": "https://6cpyb9aav1.execute-api.us-east-1.amazonaws.com/live"
}

logger = logging.getLogger(__name__)


def check_prerequisites(cloud_context):
    cloud = cloud_context["cloud"]
    if cloud == "aws":
        return check_aws_access()
    elif cloud == "azure":
        return check_azure_access()
    elif cloud == "gcp":
        return check_gcp_access()


def check_aws_access():
    print("\nVerifying aws account access", end=" ")

    aws_profile, region = None, None
    with open('config/aws_profile.json') as f:
        config = json.load(f)
        if 'env' in config:
            env = config['env']
            env_config_file = f'config/environments/{env}_config.json'
            if os.path.exists(env_config_file):
                filesize = os.path.getsize(env_config_file)
                if filesize > 0:
                    with open(env_config_file) as f:
                        env_config = json.load(f)
                        if 'aws_profile' in env_config:
                            aws_profile = env_config['aws_profile']

        if aws_profile is None and 'aws_profile' in config:
            aws_profile = config['aws_profile']

        if 'default_region' in config:
            region = config['default_region']
        else:
            region = os.environ.get('AWS_DEFAULT_REGION')

        try:
            session = boto3_utils.get_boto_session(region=region, aws_profile=aws_profile)
            cid = session.client('sts').get_caller_identity()
            print(f"{cid['Arn']}:", end=" ")
            print(f"{colors.OKGREEN}ok{colors.ENDC}")

        except Exception as e:
            print(f"{colors.FAIL}failed{colors.ENDC}")
            print(f"\t{colors.FAIL}{e}{colors.ENDC}")
            if aws_profile:
                print(f"\t{colors.FAIL}Make sure your `{aws_profile}` AWS profile is properly configured{colors.ENDC}\n")
                sys.exit(1)

        return config


def get_app_mode(email=None):
    app_mode = "dev"
    home_dir = getattr(sys, '_MEIPASS', os.getcwd())

    if os.environ.get('RAPIDCLOUD_MODE') == "dev":
        app_mode = "dev"
    elif '_MEI' in home_dir or os.environ.get('RAPIDCLOUD_MODE') == "live" or exists("./base_library.zip"):
        app_mode = "live"

    return app_mode


def in_local_mode():
    return os.getenv('RAPIDCLOUD_MODE') == 'local'


def check_azure_access():
    print("\nVerifying Azure subscription access:", end=" ")

    print(f"Authenticating Azure..")

    azureprofile = AzureConfigUtils.get_azure_profile()
    #azureconfig = AzureConfigUtils.get_azure_environment_config(azureprofile['env'])
    selected_subscription_id = azureprofile["subscription"]

    print(f"Authenticating Environment: {azureprofile['subscription']}")


    try:
        sub_client = SubscriptionClient(DefaultAzureCredential())
        #sub_client = get_client_from_cli_profile(SubscriptionClient)
    except Exception as e:
        print(f"Cannot authenticate. Env: {azureprofile['env']}")
        logger.error("Not logged in, running az login or make sure you have the required environemnt variables set correctly")

    exists = any(list(filter(lambda x: x.subscription_id==selected_subscription_id, sub_client.subscriptions.list())))

    if exists:
        print(f"{colors.OKGREEN}ok{colors.ENDC}")
        return azureprofile

    print(f"{colors.FAIL}failed{colors.ENDC}")
    print(f"\t{colors.FAIL}{e}{colors.ENDC}")


def check_gcp_access():
    print("\nVerifying GCP project access:", end=" ")

    try:
        config = load_json_file('./config/gcp_profile.json', './config/gcp_default_profile.json')

        # https://google-auth.readthedocs.io/en/master/user-guide.html#application-default-credentials
        # https://stackoverflow.com/questions/65821436/programmatically-get-current-service-account-on-gcp
        credentials, rc_activation_project_id = google.auth.default() # The rc_activation_project_id is not to be confused with each environment's target project ID.

        if hasattr(credentials, "service_account_email"):
            google_application_credentials_env_var = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if google_application_credentials_env_var:
                print_utils.info(f"You've authenticated via GOOGLE_APPLICATION_CREDENTIALS={google_application_credentials_env_var}")
                if rc_activation_project_id:
                    print(f"{credentials.service_account_email} (from GOOGLE_APPLICATION_CREDENTIALS) project_id={rc_activation_project_id} {colors.OKGREEN}ok{colors.ENDC}")
                else:
                    raise RuntimeError(f"{colors.FAIL}You're using GOOGLE_APPLICATION_CREDENTIALS={google_application_credentials_env_var} but the JSON file is missing the attribute 'project_id'. This is an unexpected scenario.{colors.ENDC}")
            else:
                # https://stackoverflow.com/questions/65821436/programmatically-get-current-service-account-on-gcp/73700292#73700292
                # TODO: This has been tested on a MacOS laptop where the credential is obtained from local files ~/.config/gcloud/*. We still need to test when running on a GCP VM where the credential is obtained from GCP metadata server (analogous to AWS EC2 Instance Profile's IAM role).
                print_utils.info(f"You've running on a GCP VM and authenticated with the VM's attached service account.")
                if rc_activation_project_id:
                    print(f"{credentials.service_account_email} (from GCP Compute Engine metadata server) project_id={rc_activation_project_id} {colors.OKGREEN}ok{colors.ENDC}")
                else:
                    raise RuntimeError(f"{colors.FAIL}You're using the service account attached to this GCP VM but it is somehow missing 'project_id'. This is an unexpected scenario.{colors.ENDC}")

        else:
            if hasattr(credentials, "quota_project_id"):
                if credentials.quota_project_id:
                    # Strictly speaking, GCP doesn't requre these 2 project IDs to equal each other; however, not being so will be confusing
                    # and in all likelihood is an unintentional misconfiguration on user's part. So, we require them to equal.
                    assert rc_activation_project_id == credentials.quota_project_id, f"project_id('{rc_activation_project_id}') should == credentials.quota_project_id('{credentials.quota_project_id}') to avoid confusion"
                    print(f"{colors.OKGREEN}ok{colors.ENDC} [You're using Application Default Credential ('gcloud auth application-default login'). project_id={rc_activation_project_id}]")
                else:
                    # This is a misconfiguration by the user.
                    #
                    # Strictly speaking, 'gcloud' (or GCP Python SDK) doesn't require any project_id at the time of authentication (so, it's not a misconfiguration from GCP perspective.)
                    # For example, 'gcloud config list' doesn't absolutely have to contain a project_id in the output -- in which case a subsequent
                    # 'gcloud auth application-default login' will create a file '~/.config/gcloud/application_default_credentials.json' __without__ project_id in it.
                    #
                    # However, not having such a project_id will cause confusion in Rapid Cloud because:
                    #       - either we won't readily have a project_id to host the NoSQL tables for RC metadata;
                    #       - or, if we prompt the user to enter a project_id, it'll potentially conflict with the project_id in 'gcloud config list'
                    #
                    # It is simply a lot better if we require that a project_id (let's call it the "RC Activation" project_id) already exists
                    # (in 'gcloud' CLI profile) at the time of GCP authentication (or, equivalently, at the time of './kc activate').
                    # That's what we're telling the user to fix now.
                    print(f"{colors.FAIL}It appears you're using Application Default Credential but it is missing 'quota_project_id'. Make sure you do 'gcloud config set project MY-PROJECT-ID' (where MY-PROJECT-ID is used for Rapid Cloud activation) before 'gcloud auth application-default login'; the result should be that your '~/.config/gcloud/application_default_credentials.json' has the attribute 'quota_project_id'.{colors.ENDC}")
                    sys.exit(1)
            else:
                raise RuntimeError("Can't determine which authentication method you're using. This is an unexpected scenario!")

        assert rc_activation_project_id, "rc_activation_project_id shouldn't be null at this point."
        logger.debug(f"check_gcp_access(): rc_activation_project_id='{rc_activation_project_id}'")

    except Exception as e:
        print(f"{colors.FAIL}failed{colors.ENDC}")
        print(f"\t{colors.FAIL}{e}{colors.ENDC}")
        print(f"{colors.FAIL}You haven't done 'export GOOGLE_APPLICATION_CREDENTIALS=...' or 'gcloud auth application-default login'? Please do either one.{colors.ENDC}")
        sys.exit(1)

    return config

# If the filename exists, load it as a JSON; otherwise, return an empty JSON object (i.e., {}).
def load_json_file(filename, fallback_filename=None):
    config = load_one_json_file(filename)

    if config == {} and fallback_filename is not None:
        config = load_one_json_file(fallback_filename)

    return config


def load_one_json_file(filename):
    config = {}
    if os.path.exists(filename):
        filesize = os.path.getsize(filename)
        if filesize == 0:
            config = {}
        else:
            with open(filename, 'r') as f:
                config = json.load(f)
    else:
        # The caller will/should subsequently open this (non-existent) file for WRITE and therefore create the file.
        config = {}

    return config

def get_cloud_from_args(args, session=None):
    if 'cloud' in args:
        cloud = args.get('cloud')

    elif session is not None and 'cloud' in session and session['cloud'] != "":
        cloud = session['cloud']

    else:
        cloud_context = config_utils.get_config('cloud_context')
        cloud = cloud_context['cloud']

    # TODO temp fix for the angular caching issue
    if cloud not in ["aws", "azure", "gcp"]:
        cloud = "aws"
    
    return cloud

