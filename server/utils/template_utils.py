#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import json
import logging
import os
import time

from boto3.dynamodb.conditions import Attr, Key
from commands import general_utils
from commands.cli_worker.license_worker import LicenseWorker
from server.utils import aws_metadata_utils, dashboard, permission_utils

logger = logging.getLogger("template_utils")
logger.setLevel(logging.INFO)


def add_subscription_links(action, tier, activation):
    # account info page
    if tier == "1" and action['id'] == 'activate':
        if action['steps'][0]['stripe_enabled']:
            logger.info(f"activation email {activation['email']}")
            description_upgrade = f"description_upgrade_{general_utils.get_app_mode()}"
            action['steps'][0]['description'] = action['steps'][0][description_upgrade]
    elif tier == "2" and action['id'] == 'activate' and 'stripe' in activation and 'current' in activation['stripe'] and 'auto-renew' in activation['stripe']['current'] and activation['stripe']['current']['auto-renew']:
        action['steps'][0]['commands'].insert(0, {
            "label": "Cancel Subscription",
            "require_confirmation": "true",
            "confirmation_message": "Are you sure you want to cancel your RapidCloud Premium Subscription? Once cancelled, you can continue using RapidCloud Premium until the end of your current subscription billing cycle.",
            "command": {
                "phase": "subscribe",
                "command": "cancel"
            }
        })

def add_notes(action):
    if 'steps' in action and len(action['steps']) == 2:
        if 'datasource' in action['steps'][0] and "data?type=metadata" in action['steps'][0]['datasource'] and 'controls' in action['steps'][1]:
            action['steps'][1]['controls'].append({
                "type": "Theia::Control::Input",
                "id": "notes",
                "label": "Notes",
                "readonly": True
            })

def add_common_read_only_fields(form_step):
    if "controls" in form_step:
        form_step["controls"].append({
            "type": "Theia::Control::Input",
            "id": "cmd_id",
            "label": "Command ID",
            "readonly": True,
            "hidden": "true"
        })
        form_step["controls"].append({
            "type": "Theia::Control::Input",
            "id": "fqn",
            "hidden": "true"
        })

def add_subscription_note(step1, form_step, tier, tiers):
    if "commands" in form_step:
        for cmd in form_step["commands"]:
            feature = cmd["command"]["phase"]
            if tier == "1" and feature in tiers and tiers[feature] in ["2,3","3"]:
                step1["allowMarkdown"] = "true"
                step1["description"] = f"{step1['description']}\n##### _(this feature is only available in premium version)_"
                step1["readonly"] = "true"
                return True
    return False

def get_grid_step(action):
    steps = action['steps']
    grid_step = None
    for step in steps:
        if step["type"] == "Theia::Step::Grid":
            grid_step = step
    return grid_step

def get_form_step(action):
    steps = action['steps']
    step1 = steps[0]
    form_step = None
    if step1["type"] == "Theia::Step::Form":
        form_step = step1
    elif len(steps) > 1:
        step2 = steps[1]
        if step2["type"] == "Theia::Step::Form":
            form_step = step2
    return form_step


def get_aws_template_extras(form_step, trend_enabled):
    if trend_enabled["application"] and form_step['id'] == "lambda":
        logger.debug(f"adding trend application security to {form_step['id']} form step")
        form_step["controls"].append({
            "type": "Theia::Control::Toggle",
            "id": "lambda_enable_trend",
            "label": "Enable Trend Micro Application Security. This will automatically add Trend Micro Application Security Lambda Layer to your Lambda function with the next infrastructure deployment (`kc tf apply`)"
        })
        form_step["controls"].append({
            "type": "Theia::Control::Select",
            "id": "lambda_trend_app_security_group",
            "label": "Trend Micro Application Security Group",
            "datasource": "trendmicro/as/groups?col=tm_as_name",
            "help": "Add security groups via RapidCloud `Trend Micro Cloud One -> Application Security Groups` page."
        })

    if trend_enabled["workload"] and form_step['id'] in ["ec2", "ec2_list", "ec2_list_launch_templates"]:
        logger.debug(f"adding trend workload security to {form_step['id']} form step")
        form_step["controls"].append({
            "type": "Theia::Control::Toggle",
            "id": "ec2_enable_trend",
            "label": "Enable Trend Micro Workload Security. If this EC2 instance has not been created in your AWS Account yet (you did not run `kc tf apply`), this will  add Trend Micro Workload Security agent to the instance User Data. If this is an existing EC2 instance, this will install and activate Trend Micro Workload Security agent immediately via SSM."
        })
        form_step["controls"].append({
            "type": "Theia::Control::Select",
            "id": "ec2_trend_workload_group",
            "label": "Trend Micro Workload Security Group",
            "datasource": "trendmicro/workload/groups?col=tm_workload_name",
            "help": "Add security groups via RapidCloud `Trend Micro Cloud One -> Workload Security Groups` page."
        })

    if trend_enabled["filestorage"] and form_step['id'] == "s3_create_bucket":
        logger.debug(f"adding trend file storage security to {form_step['id']} form step")
        form_step["controls"].append({
            "type": "Theia::Control::Toggle",
            "id": "s3_enable_trend",
            "label": "Enable Trend Micro File Storage Security. This will create a new File Storage Security Storage Stack. You must have an existing Scanner Stack. If you don't have one, go to RapidCloud `Trend Micro` -> `File Storage Security Stacks`, and create a scanner stack."
        })
        form_step["controls"].append({
            "type": "Theia::Control::Input",
            "id": "tm_fss_stackID",
            "label": "Trend Micro Cloud One - File Storage Security Stack ID",
            "readonly": True
        })

def get_azure_template_extras():
    pass


def get_gcp_template_extras():
    pass


def update_module_create_template(form, tier):
    for i in range(1, 21):
        form["controls"][-1]["modules"].append({
            "type": "Theia::Control::Toggle",
            "id": f"arg{i}",
            "label": f"Argument {i}",
            "value": False,
            "controls": [
                {
                    "type": "Theia::Control::Input",
                    "id": f"arg{i}_id",
                    "label": "Argument ID from module.json"
                },
                {
                    "type": "Theia::Control::Input",
                    "id": f"arg{i}_label",
                    "label": "Argument Label"
                },
                {
                    "type": "Theia::Control::Select",
                    "id": f"arg{i}_type",
                    "label": "Argument Control Type",
                    "datasource": "control_types?extra=true"
                },
                {
                    "type": "Theia::Control::Toggle",
                    "id": f"arg{i}_readonly",
                    "label": "Read Only"
                },
                {
                    "type": "Theia::Control::Toggle",
                    "id": f"arg{i}_readonly_edit",
                    "label": "Read Only in Edit Mode"
                },
                {
                    "type": "Theia::Control::Input",
                    "id": f"arg{i}_datasource",
                    "label": "Data Source Endpoint",
                    "help": "Data source for Select and MultiSelect only"
                },
                {
                    "type": "Theia::Control::KeyValue",
                    "id": f"arg{i}_options",
                    "label": "Select or MultiSelect Option Values",
                    "add_value_label": "Add Option",
                    "help": "Values for Select and MultiSelect only (if Data Source not provided)",
                    "default": ""
                },
                {
                    "type": "Theia::Control::Input",
                    "id": f"arg{i}_help",
                    "label": "Argument Help Information"
                }
            ]
        })


def get_trendmicro_setup_info(session):
    trend_enabled = {
        "application": False,
        "workload": False,
        "filestorage": False
    }
    try:
        dynamodb_resource = aws_metadata_utils.dynamodb_resource(session)
        trend_info = dynamodb_resource.Table("metadata").scan(FilterExpression=Attr('module').eq('trendmicro') & Attr('command').eq('setup'))['Items']
        if len(trend_info) > 0:
            trend_enabled["application"] = trend_info[0]['params']['trendmicro_enable_application_security'] == "true"
            trend_enabled["workload"] = trend_info[0]['params']['trendmicro_enable_workload_security'] == "true"
            trend_enabled["filestorage"] = trend_info[0]['params']['trendmicro_enable_filestorage_security'] == "true"
    except Exception as e:
        # logger.error(f"get_trendmicro {e}")
        pass
    return trend_enabled


def get_template(kc_args, cloud="aws", session=None):
    start_time = time.time()

    # final cloud specific template
    with open(f'./server/console/template/final_template_{cloud}.json', 'r') as f:
        final_template = json.load(f)

    license_worker = LicenseWorker(kc_args)

    # get all tiers by feature
    tiers = {}
    try:
        for tier in license_worker.contact_lic_server("get_tiers"):
            if tier.get("enabled", True) or general_utils.get_app_mode() == "dev":
                tiers[tier['feature']] = tier['tiers']
    except Exception as e:
        logger.error(f"get_template tiers {e}")
    # logger.info(tiers)

    # get customer subscription tier
    app = session.get("app", cloud)
    try:
        # logger.info("getting activation")
        activation = license_worker.contact_lic_server("get_activation")
        # logger.info(f"activation: {activation}")
        tier = activation['tier']
        allowed_apps = activation.get("apps", "all").split(",")
        session["allowed_apps"] = allowed_apps
        # logger.info(f"allowed_apps {allowed_apps}")
        if app not in allowed_apps and allowed_apps[0] != "all":
            final_template["sections"] = []
            return final_template
    except Exception as e:
        logger.error(f"get_template subscription {e}")
        return final_template

    # add custom sections and actions to the final template
    #   note: custom actions take precedence over native actions
    custom_template_file = f"./server/console/template/custom_template_{cloud}.json"
    if os.path.exists(custom_template_file):
        with open(custom_template_file, "r") as f:
            custom_template = json.load(f)
            if 'sections' in custom_template:
                for custom_section in custom_template['sections']:
                    # logger.info(f"custom_section = {custom_section['id']} {custom_section['label']}")

                    # check if native section with the same id exists
                    duplicate_section = False
                    for native_section in final_template['sections']:
                        if native_section["id"] == custom_section["id"]:
                            # logger.info(f"native_section = {native_section['id']} {native_section['label']}")

                            # custom action takes precedence
                            native_dict = {d["id"]: d for d in native_section["actions"]}
                            custom_dict = {d["id"]: d for d in custom_section["actions"]}
                            native_section["actions"] = list({**native_dict, **custom_dict}.values())
                            duplicate_section = True
                            break
                    if not duplicate_section:
                        final_template['sections'] = final_template['sections'] + custom_template['sections']

    # check for app and app_role and add dynamic elements to the template
    if cloud == "aws":
        trend_enabled = get_trendmicro_setup_info(session)
    if activation:
        cloud = session.get("cloud")
        # get application context
        try:
            # logger.info("getting app_context")
            app_context = license_worker.contact_lic_server("get_app_context")["data"]
        except Exception as e:
            logger.error(f"get_template app context {e}")
            with open('./server/console/template/app_context.json', 'r') as f:
                app_context = json.load(f)
                # logger.info(f"app context {json.dumps(app_context, indent=2)}")

        template_copy = copy.deepcopy(final_template)
        template_copy["sections"] = []
        for section in final_template['sections']:

            # "app" specific sections
            section_apps = app_context[cloud].get(section['id'], cloud)
            if section_apps == "":
                section_apps = cloud
            section_apps = section_apps.split(",")
            if app not in section_apps and "all" not in section_apps:
                # logger.info(f"skipping section `{section['id']}` ({app} - {section_apps})")
                continue

            section_copy = copy.deepcopy(section)
            if 'actions' in section:
                section_copy["actions"] = []
                for action in section['actions']:
                    # logger.info(f"action id {action.get('id')}, type {action.get('type')}, desc {action.get('description')}, section id {section.get('id')}")
                    # "app_role" specific actions
                    app_role = session.get("app_role", "all")
                    action_app_roles = action.get("app_roles", "all").split(",")
                    if app_role not in action_app_roles and "all" not in action_app_roles:
                        logger.info(f"skipping action `{section['id']} -> {action['id']}`")
                        continue

                    # add_subscription_links(action, tier, activation)

                    if 'steps' in action:
                        grid_step = get_grid_step(action)
                        form_step = get_form_step(action)

                        if grid_step:
                            if action['id'] == "environments" and grid_step['id'] == "environments" and cloud == "aws":
                                logger.info(f"populating x_acct_role_cf_url in template grid_type: {grid_step['type']}, grid_step: {grid_step['id']}")
                                set_x_acct_role_cf_url(grid_step, session, license_worker)

                        if form_step:
                            if form_step['id'] == "access_create_role":
                                permission_utils.update_role_template(kc_args, form_step, tier)
                            elif form_step['id'] == "module_create_template":
                                update_module_create_template(form_step, tier)
                            if cloud == "aws":
                                if action['id'] == "environments" and form_step['id'] == "environments":
                                    logger.info(f"populating x_acct_role_cf_url in template grid_type: {grid_step['type']}, grid_step: {grid_step['id']}")
                                    set_x_acct_role_cf_url(form_step, session, license_worker)
                                get_aws_template_extras(form_step, trend_enabled)
                            add_common_read_only_fields(form_step)
                            paid_marked = add_subscription_note(action['steps'][0], form_step, tier, tiers)
                            if paid_marked:
                                continue

                    add_notes(action)

                    section_copy["actions"].append(action)
                    # logger.info(f"appending id {action.get('id')}, type {action.get('type')}, desc {action.get('description')}, section id {section.get('id')}")

            template_copy["sections"].append(section_copy)


    # if cloud == "aws":
    #     dashboard_action = dashboard.get_dashboard(cloud, activation)
    #     final_template["sections"][0]["actions"].append(dashboard_action)

    # apply role to restrict access to console features
    template_copy = permission_utils.apply_permissions(template_copy, activation, session)
    footer_version = template_copy["footer"]["columns"][2]["content"]
    rc_app_context = session.get("app", session.get("cloud"))
    template_copy["footer"]["columns"][2]["content"] = f'{footer_version} ({rc_app_context})'
    logger.info(f"template took {round(time.time() - start_time, 2)}s")
    return template_copy


def set_x_acct_role_cf_url(form_step, session, license_worker):
    params = {
        "action": "get_cross_account_role_cf_template_url",
        "email": session.get("email"),
    }
    try:
        x_acct_role_cf_url = license_worker.contact_lic_server("saas", params=params).get("x_account_role_cf_template_url", None)
        logger.info(f"x_acct_role_cf_url {x_acct_role_cf_url}")
        if x_acct_role_cf_url is not None:
            form_step["description"] = form_step["description"].replace("{{x_acct_role_cf_url}}",x_acct_role_cf_url)
        else:
            form_step["description"] = ""
    except Exception as e:
        logger.error(f"get_x_acces_role {e}")


def get_control_types():
    select_options = []
    TYPES = ["Input", "TextArea", "Select", "Toggle", "MultiSelect", "KeyValue"]
    for control_type in TYPES:
        select_options.append({
            "type": "Theia::Option",
            "label": control_type,
            "value": f"Theia::Control::{control_type}"
        })
    return select_options
