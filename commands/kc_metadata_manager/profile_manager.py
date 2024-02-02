#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import os

_cloud_name      = None
_profile_manager = None
logger = logging.getLogger(__name__)


class ProfileManager(object):

    def __init__(self):
        self.activation_profile_dict = None
        self.curr_env_dict           = None


    def get_cloud_name(self) -> str:
        '''
        Get the currently effective cloud provider name.

        :return: 'aws' or 'azure' or 'gcp'
        '''
        return _get_cloud_name()


    def get_activation_profile_json(self) -> dict:
        '''
        :return: A JSON object (dict) which is loaded from, e.g., ./config/gcp_profile.json.
        '''
        if self.activation_profile_dict:
            return self.activation_profile_dict

        filename          = f"config/{self.get_cloud_name()}_profile.json"
        fallback_filename = f"config/{self.get_cloud_name()}_default_profile.json"

        self.activation_profile_dict = load_json_file(filename, fallback_filename)

        assert self.activation_profile_dict, f"activation_profile_dict should not be null. filename='{filename}'"
        return self.activation_profile_dict


    def get_curr_env_json(self) -> dict:
        '''
        :return: A JSON object (dict) which is loaded from ./config/environments/{CURRENT_ENV}_config.json
                 where CURRENT_ENV is the "env" attribute of ./config/{aws|azure|gcp}_profile.json
        '''
        env_name = self.get_activation_profile_json()['env']

        if not env_name:
            return None

        self.curr_env_dict = self.get_named_env_json(env_name)
        return self.curr_env_dict


    def get_named_env_json(self, env_name: str) -> dict:
        return load_json_file(f"config/environments/{env_name}_config.json")


    # def get_cloud_account_id_for_metadata() -> str:
    #     '''
    #     Returns the cloud account ID (AWS Account ID, GCP Project ID, Azure Subscription ID)
    #     which hosts the Rapid Cloud metadata NoSQL tables (AWS DynamoDB, GCP Firestore, Azure CosmosDB.)
    #     This is the account (or implied account) for './kc activate'.
    #     See Also: get_cloud_account_id_for_target_env().
    #     '''
    #     raise RuntimeError("Subclass should override this method: get_cloud_account_id_for_metadata().")


class AwsProfileManager(ProfileManager):
    pass


class AzureProfileManager(ProfileManager):
    pass


class GcpProfileManager(ProfileManager):
    def get_env_project_id(self) -> str:
        '''
        A convenience method.

        :return: The project_id for the current Rapid Cloud environment.
                 This does not necessarily equal the RC activation project ID (where the NoSQL metadata tables are.)
        '''
        return self.get_curr_env_json()['env_project_id']


def get_profile_manager() -> ProfileManager:
    '''
    :return: The singleton instance of the ProfileManager class.
    '''
    global _profile_manager

    if _profile_manager:
        return _profile_manager

    cloud_name = _get_cloud_name()
    if cloud_name   == 'aws':
        _profile_manager = AwsProfileManager()
    elif cloud_name == 'azure':
        _profile_manager = AzureProfileManager()
    elif cloud_name == 'gcp':
        _profile_manager = GcpProfileManager()
    else:
        raise RuntimeError(f"Unexpected cloud provider: '{cloud_name}'")

    assert _profile_manager, "_profile_manager should not be None at this point!"
    return _profile_manager


def reload_profile_manager() -> ProfileManager:
    _reset()
    return get_profile_manager()


def load_json_file(filename: str, fallback_filename: str=None):
    '''
    If the JSON filename exists, load it (as a dict, list, etc.); otherwise, return an empty dict '{}'.
    '''
    config = _load_one_json_file(filename)

    if config is None or config == {}:
        if fallback_filename:
            config = _load_one_json_file(fallback_filename)

    return config


def _load_one_json_file(filename: str):
    result = {}
    if os.path.exists(filename):
        filesize = os.path.getsize(filename)
        if filesize == 0:
            result = {}
        else:
            with open(filename, 'r') as f:
                logger.info(f"Reading from file '{filename}'")
                result = json.load(f)
    else:
        # The caller will/should subsequently open this (non-existent) file for WRITE and therefore create the file.
        result = {}

    return result


def _reset():
    global _cloud_name, _profile_manager
    _cloud_name      = None
    _profile_manager = None


def _get_cloud_name() -> str:
    global _cloud_name
    if _cloud_name:
        return _cloud_name

    cloud_context_file = "config/cloud_context.json"
    logging.info(f"Reading cloud_context_file='{cloud_context_file}' ...")
    with open(cloud_context_file, "r") as f:
        cloud_context = json.load(f)

    _cloud_name = cloud_context.get("cloud")
    logging.info(f"Cloud provider name: '{_cloud_name}', cloud_context_file='{cloud_context_file}'")
    assert _cloud_name, f"JSON attribute 'cloud' is null in cloud_context_file='{cloud_context_file}'"
    assert _cloud_name in ["aws","azure", "gcp"], f"Unexpected cloud provider name '{_cloud_name}' in cloud_context_file='{cloud_context_file}'"
    return _cloud_name


# ................ Unit Test ................
if __name__ == "__main__":
    mgr = get_profile_manager()
    # apj = mgr.get_activation_profile_json()
    proj_id = mgr.get_env_project_id()
    pass # Placeholder to allow a potential debugger breakpoint
