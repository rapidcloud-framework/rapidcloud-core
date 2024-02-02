#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"



def get_actions():
    actions = [
        "get_tenant",
        "get_tenant_details",
        "send_command",
        "get_ssm_command_output",
        "generate_cross_account_role_cf_template",
        "get_cross_account_role_cf_template_url",
        "list_tenants",
        "build_tenant",
        "stop_instance",
        "start_instance",
        "start_trial",
        "end_trial",
        "set_to_paid"
    ]
    select_options = []
    for action in actions:
        select_options.append({
            "type": "Theia::Option", 
            "label": action, 
            "value": action
        })
    return select_options
