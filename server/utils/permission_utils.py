#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import copy
import json
import logging
from commands import general_utils

from commands.cli_worker.license_worker import LicenseWorker

logger = logging.getLogger("permission_utils")
logger.setLevel(logging.INFO)

EXCLUDE_LIST = [
    "admin",
    "alb",
    "agree_terms",
    "architecture",
    "confirm",
    "console",
    "dynamodb_scan",
    "env",
    "help",
    "qa",
    "status",
    "test",
]

PERMISSION_OPTIONS = [
    {"type": "Theia::Option", "label": "read-only", "value": "read-only"},
    {"type": "Theia::Option", "label": "read-write", "value": "read-write"},
    {"type": "Theia::Option", "label": "none", "value": "none"},
]

INSUFFICIENT_PERMISSIONS = {
    "type": "Theia::Step::Grid",
    "datasource": "insufficient_permissions",
    "id": "not_allowed_",
    "hide_add": True
}

OPTION_ALL = {
    "type": "Theia::Option", 
    "label": "All", 
    "value": "all"
}

DEFAULT_ROLES = {
    "RAPIDCLOUD_ADMIN": {
        "access_all": "read-write",
        "access_description": "RapidCloud Administrator Role"
    },
    "RAPIDCLOUD_VIEWER": {
        "access_all": "read-only",
        "access_description": "RapidCloud View Role"
    }
} 

def get_roles(kc_args, activation):
    account_tier = activation["tier"]
    if "roles" in activation:
        roles = []
        for role_name, permissions in activation["roles"].items():
            role = {
                "name": role_name
            }
            role.update(permissions)
            if permissions.get("access_all", "granular") != "granular":
                modules = get_modules(kc_args, account_tier)
                for module, description in modules.items():
                    role[f"access_{module}"] = permissions["access_all"]
            roles.append(role)
        response = roles
    else:
        response = []
    return response


def get_roles_select(activation):
    select_options = []
    if "roles" in activation:
        for role in activation["roles"].keys():
            select_options.append({
                "type": "Theia::Option", 
                "label": role, 
                "value": role
            })
    return select_options


def get_users_select(activation):
    select_options = []
    if "activations" in activation:
        emails = []
        for email, info in activation["activations"].items():
            if info["status"] == "active":
                emails.append(email)
        emails.sort()
        for email in emails:
            select_options.append({
                "type": "Theia::Option", 
                "label": email, 
                "value": email
            })
    return select_options


def get_modules(kc_args, account_tier):
    modules = {}
    # permissions are based on allowed features/modules for the account tier
    tiers = LicenseWorker(kc_args).contact_lic_server("get_tiers")
    tiers.sort(key=lambda x: x["feature"])
    for tier in tiers:
        if not tier.get("enabled", True) and not general_utils.get_app_mode() == "dev":
            continue 

        if account_tier not in tier["tiers"].split(","):
            continue 

        if tier["feature"] in EXCLUDE_LIST:
            continue
        
        modules[tier["feature"]] = tier.get("description", "")
    return modules


def update_role_template(kc_args, access_create_role_form, account_tier):
    modules = get_modules(kc_args, account_tier)
    enable_disable_controls = []
    for module, description in modules.items():
        label = f"{module} ({description})" if description != "" else module
        control_id = f"access_{module}"
        access_create_role_form["controls"].append({
            "type": "Theia::Control::Select",
            "id": control_id,
            "label": label,
            "default": "read-only",
            "options": PERMISSION_OPTIONS,
        })

        enable_disable_controls.append(control_id)

    # update disable_controls and enable_controls when selecting value for "ALL"
    for control in access_create_role_form["controls"]:
        if control["id"] == "access_all":
            for option in control["options"]:
                if option["value"] == "granular":
                    action = "enableControls"
                else:
                    action = "disableControls"
                option["value"] = {
                    "type": "Theia::DataOption",
                    "value": option["value"],
                    action: enable_disable_controls
                }
            break


def apply_permissions(tmpl, activation, session):
    logger.info("applying permissions to console template ...")
    final_tmpl = copy.deepcopy(tmpl)
    final_tmpl["sections"] = []

    # email must match account domain
    if "email" in session and "domain" in session and session["domain"] != session["email"].split("@")[1]:
        logger.info(f'{session["domain"]} does not match {session["email"]}')
        return final_tmpl

    if 'activations' in activation:
        user_activation = activation['activations'][session["email"]]
    elif 'role' in activation:
        user_activation = activation

    user_role = user_activation.get("role", "RAPIDCLOUD_VIEWER")
    permissions = activation.get("roles", DEFAULT_ROLES).get(user_role, {})
    # print(permissions)

    # apply permissions
    for section in tmpl["sections"]:
        final_section = copy.deepcopy(section)
        final_section["actions"] = []

        # add empty section
        final_tmpl["sections"].append(final_section)

        for action in section.get("actions", []):
            if "steps" not in action:
                # always add action that has no steps (e.g. home, diagram)
                final_section["actions"].append(action)
            else:
                final_action = copy.deepcopy(action)
                final_action["steps"] = []
                
                for step in action["steps"]:
                    permission = permissions.get("access_all", None)
                    module = action['module'] if "module" in action else "unknown"
                    if permission is None or permission not in ["read-only", "read-write"]:
                        if module != "unknown":
                            permission = permissions.get(f"access_{module}", None)
                            if permission is None:
                                permission = "read-only"
                        else:
                            permission = "read-only"

                    allow_readonly = permission and permission in ["read-only", "read-write"]
                    if allow_readonly:
                        if permission != "read-write":
                            if step["type"] == "Theia::Step::Form":
                                # remove buttons
                                step["commands"] = []
                                # make all form fields readonly
                                if "controls" in step:
                                    for control in step["controls"]:
                                        control["readonly"] = True
                            elif step["type"] == "Theia::Step::Grid":
                                # remove add icon ("+")
                                step["hide_add"] = True

                        final_action["steps"].append(step)
                    else:
                        INSUFFICIENT_PERMISSIONS["title"] = "Insufficient Permissions",
                        final_action["steps"].append(INSUFFICIENT_PERMISSIONS)
                    
                    # logger.info(f"{section['id']}.{action['id']} ({module}): {permission}")
                
                # add action to section
                final_section["actions"].append(final_action)

    # logger.info("")
    return final_tmpl
