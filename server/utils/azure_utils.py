import logging
import json
import os

from flask import session
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from msgraph.core import GraphClient 
from azure.mgmt.msi import ManagedServiceIdentityClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault.keys import KeyClient

import ipaddress
import requests
import traceback

from server.utils.azure_environment_utils import AzureConfigUtils
from commands.kc_metadata_manager.azure_metadata import Metadata as AzureMetadata

logger = logging.getLogger("server")
logger.setLevel(logging.INFO)

def get_form_data_from_azure(request, session):
    form_data = []

    if request.args['type'] == "resource_groups":
        get_resource_groups(request, session, form_data)

    elif request.args['type'] == "locations":
        get_locations(request, session, form_data)

    elif request.args['type'] == "subnets":
        get_subnets(request, session, form_data)

    elif request.args['type'] == "logworkspaces":
        get_log_workspaces(request, session, form_data)

    elif request.args['type'] == "managedidentities":
        get_managed_identities(request, session, form_data)
    
    elif request.args['type'] == "ad_groups":
        get_ad_groups(request, session, form_data)

    elif request.args['type'] == "public_ips":
        get_public_ips(request, session, form_data)
    
    elif request.args['type'] == "kv_keys":
        get_kv_keys(request, session, form_data)

    return form_data

def get_form_data_from_azure_infra(request, session):
    form_data = []
    args = {}
    args["cloud"] = "azure"
    args["env"] = session["env"]
    azure_metadata = AzureMetadata(args)

    extra_filters = {"profile":f"{args['env']}", "command": request.args['type']}
    items = azure_metadata.get_all_resources(extra_filters=extra_filters)

    for item in items:
        label = item.get("resource_name")
        form_data.append(option(label, item.get("resource_name"), item.get("resource_name")))
    
    return form_data

def option(label, value, data):
    return {
        "type": "Theia::Option",
        "label": label,
        "value": {
            "type": "Theia::DataOption",
            "value": value,
            "data": data
        }
    }     

def get_label(session, label, tags):
    is_rc = ""
    if tags is not None:
        if tags.get('profile') is not None:
            if tags.get('profile').lower() == session.get('env').lower():
                is_rc = "value"
    if is_rc == '':
        return label
    else:
        return f"{label} (Managed by Rapid Cloud)"

def get_subscription(session):
    if "env_info" in session and "subscription" in session["env_info"]:
        return session["env_info"]["subscription"]
    
    profile = AzureConfigUtils.get_azure_profile()
    return profile["subscription"]
    
def get_resource_groups(request, session, form_data):
    # Acquire a credential object using CLI-based authentication.
    subscription_id = get_subscription(session)
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    group_list = resource_client.resource_groups.list()
    resource_groups = []
    sorted_entities = sorted(group_list, key=lambda x: x.name.lower(), reverse=False)
    rc_rgs = list(filter(lambda x: x.tags is not None and x.tags.get('profile') is not None and x.tags.get('profile') == session.get('env') ,sorted_entities))
    other_rgs = list(filter((lambda x: x.tags is None) ,sorted_entities))
    additional_rgs = list(filter((lambda x: x.tags is not None and x.tags.get('profile') is None) ,sorted_entities))

    final_list = rc_rgs + other_rgs + additional_rgs
    
    # for item in list(final_list):
    #     print(item.name)

    #sorted_entities = sorted(group_list, key=lambda x: x.name.lower(), reverse=False)
    for group in list(final_list):
        label = get_label(session, f"{group.name} ({group.location})", group.tags)
        form_data.append(option(label, group.name, group.id))

def get_locations(request, session, form_data):
    # Acquire a credential object using CLI-based authentication.
    subscription_id = get_subscription(session)
    credential = DefaultAzureCredential()

    subs_client = SubscriptionClient(credential)
    entities = subs_client.subscriptions.list_locations(subscription_id)

    for location in list(entities):
        label = f"{location.display_name}"
        form_data.append(option(label, location.name, location.name))

def get_subnets(request, session, form_data):
    # Acquire a credential object using CLI-based authentication.
    SUBSCRIPTION_ID = get_subscription(session)
    network_client = NetworkManagementClient(credential=DefaultAzureCredential(), subscription_id=SUBSCRIPTION_ID)
    vnets = network_client.virtual_networks.list_all()

    for vnet in list(vnets):
        for subnet in vnet.subnets:
            if "min_prefixlen" in request.args:
                ip_addr = ipaddress.ip_network(subnet.address_prefix)
                if ip_addr.prefixlen > int(request.args["min_prefixlen"]): continue  #subnet must be at least min_prefixlen
            
            if "endpoint" in request.args and subnet.service_endpoints is not None:
                if list(filter(lambda x: x.service == request.args["endpoint"], subnet.service_endpoints)).count == 0: continue

            label = f"{vnet.name} - {subnet.name} ({subnet.address_prefix})"
            form_data.append(option(label, subnet.id, subnet.id))

def get_log_workspaces(request, session, form_data):
    # Acquire a credential object using CLI-based authentication.
    subscription_id = get_subscription(session)
    credential = DefaultAzureCredential()

    log_client = LogAnalyticsManagementClient(credential,subscription_id)
    entities = log_client.workspaces.list()

    for workspace in list(entities):
        label = f"{workspace.name}"
        form_data.append(option(label, workspace.id, workspace.id))

def get_managed_identities(request, session, form_data):
    subscription_id = get_subscription(session)
    credential = DefaultAzureCredential()
    msi_client = ManagedServiceIdentityClient(credential, subscription_id)
    entities = msi_client.user_assigned_identities.list_by_subscription()

    for user in list(entities):
        label = f"{user.name}"
        id = user.id.replace("resourcegroups","resourceGroups") #workaround
        form_data.append(option(label, id, id))

# def get_managed_identities(request, form_data):
#     subscription_id = get_subscription(session)
#     token = get_new_token()
#     api_call_headers = {'Authorization': 'Bearer ' + token}
#     response = requests.get(f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.ManagedIdentity/userAssignedIdentities?api-version=2023-01-31",
#                             headers=api_call_headers, verify=False)

#     response2 = json.loads(response.text)
#     for identity in response2['value']:
#         form_data.append(option(identity['name'], identity['id'], identity['id']))

# def get_new_token():
#     tokenCredential = DefaultAzureCredential()
#     scope = "https://management.core.windows.net/.default"
#     access_token = tokenCredential.get_token(scope)
#     return access_token.token

def get_ad_groups(request, session, form_data):
    # Acquire a credential object using CLI-based authentication.
    try:
        graph_client = GraphClient(credential=DefaultAzureCredential())
        groups = graph_client.get('/groups?$select=displayName,id')
        entities_groups = json.dumps(groups.json())
        ent_groups = json.loads(entities_groups)

    except Exception as e:
        traceback.print_exc()
    #For the groups 
    for group in list(ent_groups.get('value')):
        label = f"{group.get('displayName')}"
        form_data.append(option(label, group.get('id'), group.get('id')))

def get_ad_users(request, session, form_data):
    # Acquire a credential object using CLI-based authentication.
    try:
        graph_client = GraphClient(credential=DefaultAzureCredential())
        users = graph_client.get('/users?$select=displayName,id')
        entities_users = json.dumps(users.json())
        ent_users = json.loads(entities_users)

    except Exception as e:
        traceback.print_exc()
    #For the users 
    for user in list(ent_users.get('value')):
        label = f"{user.get('displayName')}"
        form_data.append(option(label, user.get('id'), user.get('id')))
    
def get_public_ips(request, session, form_data):
    subscription_id = get_subscription(session)
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id)
    entities = network_client.public_ip_addresses.list_all()
    sorted_entities = sorted(
        entities, key=lambda x: x.name.lower(), reverse=False)
    # rc_ips = list(filter(lambda x: x.tags is not None and x.tags.get(
    #     'managed') == 'rc', sorted_entities))

    for ip in list(sorted_entities):
        label = get_label(session, f"{ip.name} ({ip.ip_address})", ip.tags)
        form_data.append(option(label, ip.id, ip.id))

def get_kv_keys(request, session, form_data):
    subscription_id = get_subscription(session)
    credential = DefaultAzureCredential()
    kv_client = KeyVaultManagementClient(credential,subscription_id)
    entities = kv_client.vaults.list_by_subscription()

    allkeys = []
    for keyvault in list(entities):
        kv_id = keyvault.id
        try:
            key_client = KeyClient(keyvault.properties.vault_uri, credential)
            kv_keys = key_client.list_properties_of_keys()
            for key in list(kv_keys):
                key_versions = key_client.list_properties_of_key_versions(key.name)
                versions = []
                for key_version in list(key_versions):
                    versions.append(key_version)
                if len(versions) > 0:
                    key.last_version = versions[-1].version
                key.vault_id = kv_id
                allkeys.append(key)
        except Exception as e:
            print(f"Key vault error: {e}")
            continue

    for key in list(allkeys):
        #val = f"{key.vault_id}|{key.name}"
        #if key.last_version is not None:
        #    val = f"{key.id}/{key.last_version}"
        val = key.id
        label = f"{key.name}"
        form_data.append(option(label, val, val))