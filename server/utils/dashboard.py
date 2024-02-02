#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
from tomark import Tomark

from commands.cli_worker.license_worker import LicenseWorker


MARKDOWN = "Theia::Panel::Markdown"

def load_md(filename):
    with open(f"./server/console/template/dashboard/{filename}", 'r') as f:
        return f.read()

def create_subscription_status_panel():
    md = load_md("account_status_panel.md")

    # activation = LicenseWorker(kc_args).contact_lic_server("get_activation")
    # # print(json.dumps(activation, indent=2))
    # if 'activations' in activation:
    #     with open('./config/aws_profile.json', 'r') as f:
    #         config = json.load(f)
    #     user_activation = activation['activations'][session["email"]]
    #     user_activation['email'] = session['email']
    #     user_activation['aws_profile'] = config.get('aws_profile','')
    #     user_activation['tier'] = activation['tier']
    #     if 'stripe' in activation and 'current' in activation['stripe']:
    #         user_activation['start'] = datetime.fromtimestamp(int(activation['stripe']['current']['period_start']))
    #         user_activation['end'] = datetime.fromtimestamp(int(activation['stripe']['current']['period_end']))
    #         if 'auto-renew' in activation['stripe']['current']:
    #             user_activation['auto_renew'] = activation['stripe']['current']['auto-renew']
    #         user_activation['invoice_url'] = activation['stripe']['current']['hosted_invoice_url']

    return md

def create_panel(type, title, content, size=None):
    panel = {
        "columns": [
            {
                "panel": {
                    "type": type,
                    "title": title,
                    "content": content
                }
            }
        ]
    }

    if size is not None:
        panel["columns"][0]["size"] = size
    
    return panel


def get_dashboard(cloud, activation):
    # dashboard = {
    #     "id": "dashboard",
    #     "type": "Theia::Dashboard",
    #     "label": "Dashboard",
    #     "rows": [
    #         {
    #             "columns": [
    #                 {
    #                     "size": 12,
    #                     "rows": []
    #                 }
    #             ]
    #         }
    #     ]
    # }

    dashboard = {
        "id": "dashboard",
        "type": "Theia::Dashboard",
        "label": "Dashboard",
        "rows": [
            {},
            {
                "columns": [
                    {
                        "size": 4,
                        "rows": []
                    },
                    {
                        "size": 4,
                        "rows": []
                    },
                    {
                        "size": 4,
                        "rows": []
                    }
                ]
            }
        ]
    }


    dashboard["rows"][0] = create_panel(MARKDOWN, "Subscription Status", create_subscription_status_panel(), 12)

    md = "users_md"
    users_panel = create_panel(MARKDOWN, "Users", md)
    dashboard["rows"][1]["columns"][0]["rows"].append(users_panel)

    md = "env_md"
    env_panel = create_panel(MARKDOWN, "Environment Statistics", md)
    dashboard["rows"][1]["columns"][1]["rows"].append(env_panel)

    md = "release_notes_md"
    release_notes_panel = create_panel(MARKDOWN, "Release Notes", md)
    dashboard["rows"][1]["columns"][2]["rows"].append(release_notes_panel)

    return dashboard
