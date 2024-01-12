#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import datetime
import glob
import json
import logging
import os
import pprint
import subprocess
from datetime import datetime, timedelta

from commands import boto3_utils, general_utils
from commands.cli_worker.license_worker import LicenseWorker
from commands.colors import colors
from commands.modules.ec2 import ModuleMetadata as EC2Module
from commands.modules.workload import ModuleMetadata as WorkloadModule
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_cors import CORS
from flask_session import Session
from licensing import saas

from server.utils import (aws_metadata_utils, aws_utils, azure_utils,
                          cloud_metadata_utils, custom_module_utils,
                          diagram_utils, generic_metadata_utils,
                          permission_utils, saas_utils, template_utils,
                          trend_utils)
from server.utils.auth_helper import AuthHelper
from server.utils.cli_helper import CliHelper

logger = logging.getLogger("server")

# dev vs live mode
app_mode = general_utils.get_app_mode()

kc_config_file = './config/kc_config.json'
if os.path.exists(kc_config_file):
    with open(kc_config_file, 'r') as f:
        log_level = json.load(f)["logger_level"]
elif app_mode == "live":
    log_level = logging.WARNING
else:
    log_level = logging.INFO
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logger.setLevel(log_level)

kc_exec = None
kc_args = None
locked_environments = {}
UNAUTHORIZED = []

with open( './config/version.json', 'r') as f:
    version = json.load(f)["version"]

INCLUDE_DISABLED_APPS = os.environ.get('RAPIDCLOUD_ALL_APPS', "false") == "true"

# ------------------------------------------------------
# CLOUDS
# ------------------------------------------------------

# TODO we'll take these flags outside at some point
AWS_ENABLED = True
AZURE_ENABLED = True
GCP_ENABLED = os.environ.get('RAPIDCLOUD_GCP_ENABLED', "false") == "true"

CLOUDS = {}

if AWS_ENABLED:
    CLOUDS["aws"] ={
        "cloud_label": "AWS",
        "account_label": "Account",
        "region_label": "Region",
        "vpc_label": "VPC"
    }

if AZURE_ENABLED:
    CLOUDS["azure"] ={
        "cloud_label": "Azure",
        "account_label": "Subscription",
        "region_label": "Region",
        "vpc_label": "VNet"
    }

if GCP_ENABLED:
    CLOUDS["gcp"] = {
        "cloud_label": "GCP (coming soon)",
        "account_label": "Project",
        "region_label": "Region",
        "vpc_label": "VPC"
    }

# ------------------------------------------------------
# Flask setup for console
# ------------------------------------------------------

cwd = os.getcwd()
static_folder=f"{cwd}/server/app"
template_folder=f"{cwd}/server/app"
if os.getenv("RAPIDCLOUD_MODE") is not None and os.getenv("RAPIDCLOUD_MODE") == 'live':
    static_folder=f"{cwd}/server/prod/app"
    template_folder=f"{cwd}/server/prod/app"
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
app.config['JSON_SORT_KEYS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
Session(app)
dir = './flask_session'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
SESS_VARS = ["authorized", "email", "host_url", "request_path", "cloud", "domain", "app", "app_role", "aws_profile", "x_acct_role_arn", "region", "started", "timestamp", "env", "env_info","env_cache"]
CORS(app)


# ------------------------------------------------------
# Cloud Context
# ------------------------------------------------------
cloud_context_file = "config/cloud_context.json"
with open(cloud_context_file) as f:
    cloud_context = json.load(f)


# ------------------------------------------------------
# user session
# ------------------------------------------------------
def get_session_vars():
    user_session = {}
    for var in SESS_VARS:
        user_session[var] = session[var] if var in session else ''
    return user_session


def update_session(request):
    cloud = general_utils.get_cloud_from_args(request.args, session).lower()
    with open(f"./config/{cloud}_profile.json", 'r') as f:
        config = json.load(f)
        if cloud not in session or cloud != session["cloud"]:
            session['aws_profile'] = config.get('aws_profile','?')
            session['region'] = config['default_region']
            session['domain'] = config["email"].split("@")[1] if "email" in config else ""
        if "env" in request.args:
            session["env"] = request.args.get("env")
        elif "env" not in session:
            session["env"] = config.get("env")
    session["cloud"] = cloud.lower()
    session["request_path"] = request.full_path


def logout():
    logger.info("logout")
    user_info = AuthHelper(kc_args, app_mode).get_user_info(request)
    if user_info and "email" in session:
        session.pop("authorized", None)
        session.pop("email", None)
        session.pop("domain", None)
        session.clear()


def endpoint_requires_auth():
    ignore_paths = ["/app/", "/?code=", "/api/clouds"]
    for path_substr in ignore_paths:
        if path_substr in request.full_path:
            return False
    return True


def print_session(triggered_by):
    sess = {}
    for var in SESS_VARS:
        sess[var] = session.get(var)
    logger.info(f"Session ({triggered_by}): {json.dumps(sess, indent=2, default=str)}")
    return sess


def verify_user_session(request):
    logger.info("verifing user session")
    cloud = general_utils.get_cloud_from_args(request.args, session).lower()
    with open(f'./config/{cloud}_profile.json', 'r') as f:
        config = json.load(f)

    session["timestamp"] = str(datetime.now()).split(".")[0]

    # only verify email for API requests
    new_session = False
    if "email" not in session and endpoint_requires_auth():
        new_session = True
        session["started"] = str(datetime.now()).split(".")[0]
        user_info = AuthHelper(kc_args, app_mode).get_user_info(request)
        if user_info:
            session["host_url"] = request.host_url[:-1]
            session["email"] = user_info["email"]

            domain_activation = LicenseWorker(kc_args).contact_lic_server("get_activation")
            session["domain_activation"] = domain_activation
            if domain_activation is not None and "activations" in domain_activation:
                user_activation = domain_activation["activations"].get(session["email"])
                if user_activation:
                    session["user_activation"] = user_activation
                    if user_activation.get("role", "RAPIDCLOUD_VIEWER") == "RAPIDCLOUD_ADMIN":
                        session["app_role"] = "admin"
                    else:
                        session["app_role"] = "engineer"

    # switch environment
    curr_env = session.get("env", None)
    new_env = request.args.get("env", None)
    env_changed = False
    if new_env and (curr_env and curr_env != new_env or curr_env is None):
        env_changed = True
        logger.info(f"switching env context from {curr_env} to {new_env}")
        cloud = session.get("cloud", request.args.get("cloud", "aws"))
        email = session.get("email")

        CliHelper(kc_args, app_mode).kc_build_and_call(cloud, email, new_env, locked_environments, kc_exec, "init", "set-env")
        session["env"] = new_env

        saas_params = {
            "action": "get_tenant",
            "email": email
        }

        tenant = LicenseWorker(kc_args).contact_lic_server("saas", params=saas_params)
        x_acct_roles = tenant.get('x-acct-roles', None)
        logger.info(f"verifing user session: {x_acct_roles}")

        if x_acct_roles is not None:
            logger.info(f"verifing user session: adding x_acct_role_arn from {x_acct_roles}")
            session["x_acct_role_arn"] = x_acct_roles[session["env"]]['role']
            session["region"] = x_acct_roles[session["env"]]['region']

    update_session(request)

    # save environment info in session
    if session.get("env_info") is None or session["env_info"].get("name") != session["env"]:
        env_info = cloud_metadata_utils.get_environment_info(session)
        del_keys = []
        for k in env_info.keys():
            if "wizard" in k: del_keys.append(k)
        for k in del_keys:
            del env_info[k]
        session["env_info"] = env_info

    # set authorized flag
    config_domain = config["email"].split("@")[1] if "email" in config else ""
    session["authorized"] = False
    if not endpoint_requires_auth():
        session["authorized"] = True
    elif "email" in session and config_domain == session["email"].split("@")[1]:
        session["authorized"] = True
    elif "email" in session and config_domain != "":
        logger.warning(f"User email doesn't match Account Domain - session: {session['email']} | config: {config_domain}")

    if (new_session or env_changed) and "/api/template" not in request.full_path and endpoint_requires_auth() and "/api/allowed_apps" not in request.full_path:
        print_session(request.full_path.split("?")[0])

    return session["authorized"]


def handle_env(cloud):
    if cloud != session.get("cloud",None):
        env_cache = session.get("env_cache",{})
        if session.get("cloud",None) is not None and session.get("env") is not None:
            env_cache[session["cloud"]] = session["env_info"]
            session["env"] = None
            session["env_info"] = {}


# ------------------------------------------------------
# routes
# ------------------------------------------------------

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        return

    if "/app" not in request.full_path:
        logger.info(f"{request.method} {request.full_path}")

    # application context
    cloud = general_utils.get_cloud_from_args(request.args, session).lower()
    handle_env(cloud)
    app_context = request.args.get("rc_app_context")
    if app_context is not None:
        session["app"] = app_context
    elif "app" not in session or session["app"] == "":
        session["app"] = cloud

    # clear paginated data cache
    if "/api/" in request.path and request.path != "/api/paginated_data":
        session["cached_data"] = None

    authorized = verify_user_session(request)

    # mask passwords
    if request.method == 'POST':
        req = copy.deepcopy(request.json)
        for k,v in req.items():
            if "password" in k:
                req[k] = "*************"
            elif k == "wizard":
                req[k] = "..."
        logger.info(json.dumps(req, indent=2))


def get_tenant(email):
    # logger.info(f"calling get tenant with {email}")
    saas_params = {
        "action": "get_tenant",
        "email": email
    }
    tenant = LicenseWorker(kc_args).contact_lic_server("saas", params=saas_params)
    # logger.info(f"get_tenant {json.dumps(tenant, indent=2)}")
    if tenant:
        session["tenant"] = tenant
        session["subscription"] = tenant.get("subscription", {})
        session["x-acct-roles"] = tenant.get("x-acct-roles", [])
        logger.info(f"license worker: tenant: {tenant.get('domain')}, status: {tenant.get('status')}, subscription: {tenant.get('subscription').get('status')}")


def render(page):
    return render_template(page)


@app.route('/', methods=['GET'])
def root():
    if "error" not in request.args:
        return render('index.html')
    else:
        return render_template('index.html')

@app.route('/app', defaults={'path': ''})
@app.route('/app/<path:path>')
def catch_all(path):
    return render_template('index.html')

@app.route('/app/auth-error', methods=['GET'])
def auth_error1():
    return render_template('index.html')

@app.route('/app/auth-error?', methods=['GET'])
def auth_error2():
    return render_template('index.html')

@app.route('/api/logout', methods=['GET'])
def api_logout():
    logout()
    return render_template('index.html')

@app.route('/app', methods=['GET'])
def app_home():
    return render('index.html')

@app.route('/app/callback', methods=['GET'])
def app_callback():
    return render_template('index.html')

@app.route('/app/register', methods=['GET'])
def register():
    return render_template('index.html')

@app.route('/app/action/<section>/<action>', methods=['GET'])
def refresh_any(section, action):
    # example: /app/action/publish/datawarehouse
    return render_template('index.html')

@app.route('/app/wizard', methods=['GET'])
def refresh_wizard():
    return render('index.html')

@app.route('/app/lzwizard', methods=['GET'])
def refresh_lzwizard():
    return render('index.html')

@app.route('/app/architecture', methods=['GET'])
def refresh_current():
    return render('index.html')

@app.route('/app/home', methods=['GET'])
def refresh():
    return render('index.html')

@app.route('/app/dashboard', methods=['GET'])
def dashboard():
    return render('index.html')

@app.route('/api/clouds', methods=['GET'])
def clouds():
    return jsonify(CLOUDS)

@app.route('/api/verify_status', methods=['GET'])
def verify_status():
    # logger.info(session)
    get_tenant(session["email"])
    referer_host = request.headers.get('Referer').split("//")[-1].split("/")[0].split('.')[0]
    tenant_host = session["email"].split("@")[1].split('.')[0]
    tenant_url = f"https://{tenant_host}.rapid-cloud.io"
    activation_status = session.get("domain_activation", {}).get('status')
    tenant_status = session.get("tenant", {}).get('status')
    subscription_status = session.get("subscription", {}).get("status")
    logger.info(f"verify_status: activation: {activation_status}, tenant: {tenant_status}, subscription: {subscription_status}")
    logger.info(f"verify_status: tenant_host: {tenant_host}, tenant_url: {tenant_url}, referer: {referer_host}")

    resp = {
        "activation_status": activation_status,
        "tenant_status": tenant_status,
        "subscription": session.get("subscription", {})
    }
    if tenant_host == 'kinect-consulting':
        return jsonify(resp)

    # post registration user_status = 'ACTIVE'
    if activation_status and activation_status.upper() == "ACTIVE":
        if tenant_status:
            # if status is pending it means tenant instance is not up yet
            if tenant_status.upper() == "PENDING":
                logger.info("verify_status: tenant is pending, will send to subscribe page")
                # display subscription page
                resp["page"] = "/action/setup/subscribe"
            elif tenant_status != 'ACTIVE':
                # tenat instance is being built
                logger.info("verify_status: tenant is not active, will send to inprogress page")
                resp["page"] = "/action/setup/inprogress"
            elif tenant_status == 'ACTIVE':
                logger.info("verify_status: tenant is active, will check subscriptions")
                if subscription_status:
                    if subscription_status.upper() == "ACTIVE":
                        logger.info("verify_status: tenant subscription is active")
                        # check if tenant has environments defined
                        environments = aws_metadata_utils.get_all_environments(session, kc_args)
                        # redirect to environments page is no environments
                        if tenant_host != referer_host and len(environments) == 0:
                            logger.info(f"redirecting to {tenant_url}/app/action/setup/environments, since {environments} is 0")
                            resp["redirect"] = f"{tenant_url}/app/action/setup/environments"
                        else:
                            logger.info(f"redirecting to /app/home since it has environments")
                            resp["page"] = "/home"
                else:
                    logger.info("verify_status: failed to get tenant subscription")
        else:
            logger.info("verify_status: failed to get tenant status")
    else:
        logger.info("verify_status: failed to get tenant activation")
    return jsonify(resp)


@app.route('/api/session', methods=['GET'])
def session_info():
    return jsonify(print_session("/api/session"))

@app.route('/api/all_apps', methods=['GET'])
def all_apps():
    lic_worker = LicenseWorker(kc_args)
    all_apps = lic_worker.contact_lic_server("get_app_context")["data"]["apps"]
    allowed_apps = lic_worker.contact_lic_server("get_activation").get("apps", "all")
    return jsonify(all_apps)

@app.route('/api/allowed_apps', methods=['GET'])
def allowed_apps():
    logger.info(f'in allowed_apps')
    lic_worker = LicenseWorker(kc_args)
    allowed_apps = lic_worker.contact_lic_server("get_activation").get("apps", "all")
    all_apps = lic_worker.contact_lic_server("get_app_context")["data"]["apps"]

    all_enabled_apps = {}
    if not INCLUDE_DISABLED_APPS:
         for app,info in all_apps.items():
             if info["enabled"]:
                 all_enabled_apps[app] = info
    else:
        all_enabled_apps = all_apps

    if allowed_apps == "all":
        result = all_enabled_apps
    else:
        result = {}
        for app in allowed_apps.split(','):
            if app in all_enabled_apps:
                result[app] = all_enabled_apps[app]

    sorted_result = {}
    for app in sorted(result.items(), key=lambda x: x[1]['order']):
        sorted_result[app[0]] = app[1]

    logger.info(f'AWS Only: {session["user_activation"].get("aws_only", False)}')
    logger.info(session["user_activation"])
    if "user_activation" in session and session["user_activation"].get("aws_only", False):
        sorted_result = {k:v for k,v in sorted_result.items() if v["cloud"] == "aws"}
    return jsonify(sorted_result)

@app.route('/api/template', methods=['GET'])
def template():
    cloud = general_utils.get_cloud_from_args(request.args).lower()
    setattr(kc_args, "current_session_email", session["email"])
    response = template_utils.get_template(kc_args, cloud, session)
    return jsonify(response)

@app.route('/api/readme', methods=['GET'])
def readme():
    response = get_readme()
    return jsonify(response)

@app.route('/api/data', methods=['GET'])
def data():
    if session["authorized"]:
        response = generic_metadata_utils.get_data(kc_args, session, request, app_mode)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/paginated_data_info', methods=['GET'])
def paginated_data_info():
    if session["authorized"]:
        response = generic_metadata_utils.get_paginated_data_info(kc_args, session, request, app_mode)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/paginated_data', methods=['GET'])
def paginated_data():
    if session["authorized"]:
        response = generic_metadata_utils.get_paginated_data(kc_args, session, request, app_mode)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/command', methods=['POST'])
def command():
    if session["authorized"]:
        response = CliHelper(kc_args, app_mode).post_command(session, request, locked_environments, kc_exec)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/log/<log_name>', methods=['GET'])
def log(log_name):
    with open('./logs/latest.log', 'r') as f:
        log = json.load(f)
        if "log" in log and log["log"]:
            log = log["log"]
        else:
            log = json.dumps(log, indent=2, default=str)
        return jsonify({"log": "\n" + log})

@app.route('/api/formdata', methods=['GET'])
def formdata():
    response = generic_metadata_utils.get_form_data(session, request, app_mode, kc_args)
    return jsonify(response)

@app.route('/api/formdata_from_aws', methods=['GET'])
def formdata_from_aws():
    response = aws_utils.get_form_data_from_aws(request, session)
    return jsonify(response)

@app.route('/api/formdata_from_azure', methods=['GET'])
def formdata_from_azure():
    response = azure_utils.get_form_data_from_azure(request, session)
    return jsonify(response)

@app.route('/api/formdata_from_azure_infra', methods=['GET'])
def formdata_from_azure_infra():
    response = azure_utils.get_form_data_from_azure_infra(request, session)
    return jsonify(response)

@app.route('/api/diagram/<diagram_type>', methods=['GET'])
def diagram(diagram_type):
    response = diagram_utils.gen_diagram(session, request, diagram_type)
    return jsonify(response)

@app.route('/api/diagram', methods=['GET'])
def current_state_aws():
    response = diagram_utils.gen_diagram(session, request, "solution")
    return jsonify(response)

@app.route('/api/wizard/<diagram_type>', methods=['GET'])
def wizard(diagram_type):
    profile = cloud_metadata_utils.get_environment_info(session)
    wizard_name = f"{session['cloud']}_{diagram_type}_wizard"
    if wizard_name in profile:
        wizard = profile[wizard_name]
    else:
        wizard = diagram_utils.get_default_wizard(session['cloud'], diagram_type)
    return jsonify(wizard)

@app.route('/api/status', methods=['GET'])
def status():
    if session["authorized"]:
        response = cloud_metadata_utils.get_status(request.args['env'], session, kc_args)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/tf_modules', methods=['GET'])
def tf_modules():
    if session["authorized"]:
        response = get_tf_modules(request.args['env'])
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/generated_code', methods=['GET'])
def generated_code():
    if session["authorized"]:
        response = get_generated_code(request.args['env'])
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/trendmicro/fss/stacks', methods=['GET'])
def trend_filestorage_stacks():
    if session["authorized"]:
        response = trend_utils.get_trend_filestorage_stacks(request, boto3_utils.get_boto_session(env_info=session.get("env_info")))
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/trendmicro/as/groups', methods=['GET'])
def trend_application_groups():
    if session["authorized"]:
        response = trend_utils.get_trend_application_groups(request, boto3_utils.get_boto_session(env_info=session.get("env_info")))
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/trendmicro/workload/groups', methods=['GET'])
def trend_workload_groups():
    if session["authorized"]:
        response = trend_utils.get_trend_workload_groups(request, boto3_utils.get_boto_session(env_info=session.get("env_info")))
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/trendmicro/workload/policies', methods=['GET'])
def trend_workload_policies():
    if session["authorized"]:
        response = trend_utils.get_trend_workload_policies(request, boto3_utils.get_boto_session(env_info=session.get("env_info")), kc_args)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/trendmicro/setup', methods=['GET'])
def trend_setup():
    if session["authorized"]:
        response = trend_utils.get_trend_setup(boto3_utils.get_boto_session(env_info=session.get("env_info")), session)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/resources/ec2', methods=['GET'])
def resources_ec2():
    if session["authorized"]:
        response = EC2Module(kc_args).list_unmanaged()
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/resources/ec2_launch_templates', methods=['GET'])
def resources_ec2_launch_templates():
    if session["authorized"]:
        response = EC2Module(kc_args).list_launch_templates()
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/cloud_profiles', methods=['GET'])
def cloud_profiles():
    if session["authorized"]:
        response = get_cloud_profiles(request.args['cloud_arg'])
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/account_info', methods=['GET'])
def account_info():
    if session["authorized"]:
        response = get_account_info()
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/account_users', methods=['GET'])
def account_users():
    if session["authorized"]:
        response = LicenseWorker(kc_args).account_details()
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/metadata/s3', methods=['GET'])
def metadata_s3():
    if session["authorized"]:
        response = get_metadata_s3(request.args['env'])
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/workload/status', methods=['GET'])
def workload_status():
    if session["authorized"]:
        response = WorkloadModule(kc_args).status()
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/custom/<action>', methods=['GET'])
def api_custom(action):
    if session["authorized"]:
        cloud = general_utils.get_cloud_from_args(request.args).lower()
        boto3_session = None
        if cloud == "aws":
            boto3_session = boto3_utils.get_boto_session(env_info=session.get("env_info"))
        response = custom_module_utils.custom_endpoint(action, request.args, boto3_session, get_session_vars(), cloud)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/roles', methods=['GET'])
def roles():
    if session["authorized"]:
        activation = LicenseWorker(kc_args).contact_lic_server("get_activation")
        response = permission_utils.get_roles(kc_args, activation)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/role_names_for_select', methods=['GET'])
def role_names_for_select():
    if session["authorized"]:
        activation = LicenseWorker(kc_args).contact_lic_server("get_activation")
        response = permission_utils.get_roles_select(activation)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/users_for_select', methods=['GET'])
def users_for_select():
    if session["authorized"]:
        activation = LicenseWorker(kc_args).contact_lic_server("get_activation")
        response = permission_utils.get_users_select(activation)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/module/<action>', methods=['GET','POST'])
def api_custom_module(action):
    if session["authorized"]:
        response = custom_module_utils.action(kc_args, action, get_session_vars())
    else:
        response = UNAUTHORIZED
    resp = jsonify(response)
    # resp.headers["Force-Template-Reload"] = "true"
    resp.headers["RapidCloud-Test-Header"] = "test"
    return resp

@app.route('/api/control_types', methods=['GET'])
def control_types():
    return jsonify(template_utils.get_control_types())

@app.route('/api/insufficient_permissions', methods=['GET'])
def insufficient_permissions():
    return jsonify([])

@app.route('/version', methods=['GET'])
def version():
    with open('./config/version.json', 'r') as f:
        return jsonify(json.load(f))

@app.route('/api/saas_actions', methods=['GET'])
def saas_actions():
    print("in saas_actions")
    if session["authorized"]:
        response = saas_utils.get_actions()
        print(response)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

@app.route('/api/saas', methods=['GET'])
def saas_exec():
    if session["authorized"]:
        response = saas.exec(request.args)
    else:
        response = UNAUTHORIZED
    return jsonify(response)

# ------------------------------------------------------
# other
# ------------------------------------------------------

def get_readme():
    with open('./README.md', 'r') as f:
        return json.load(f)


def get_log(log_name):
    log_file = f"./logs/{log_name}"
    with open(log_file, 'r') as f:
        contents = f.read()
        for color in [colors.OKBLUE,colors.OKGREEN,colors.WARNING,colors.FAIL,colors.ENDC,colors.UNDERLINE]:
            contents = contents.replace(color,"")
    return {"log": contents}


def get_tf_modules(env):
    dir = f"./terraform/{env}"
    logger.info(f"getting TF modules from {dir}")
    tf_modules = []
    for file_name in glob.glob(f'{dir}/*.tf'):
        logger.info(file_name)
        with open(file_name, "r") as f:
            contents = f.read()
        tf_modules.append({
            "filename": file_name,
            "contents": contents
        })
    return tf_modules


def get_generated_code(env):
    code = []
    for path in ["./lambda/*/*.py", "./data_scripts/*/*.py"]:
        logger.info(f"getting code templates from {path}")
        for file_name in glob.glob(path, recursive=True):
            if os.path.isfile(file_name):
                logger.info(file_name)
                with open(file_name, "r") as f:
                    contents = f.read()
                    if contents:
                        code.append({
                            "filename": file_name,
                            "contents": contents
                        })
    return code


def get_cloud_profiles(cloud_arg):
    select_options = [{
        "type": "Theia::Option",
        "label": "",
        "value": ""
    }]

    if cloud_arg == "aws":
        # aws configure list-profiles
        cmd = ['aws', 'configure', 'list-profiles']
        output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(output)
        for aws_profile_name in output.split("\n"):
            aws_acct_id = boto3_utils.get_aws_account_from_profile(aws_profile_name)
            if aws_acct_id:
                select_options.append({
                    "type": "Theia::Option",
                    "label": f"{aws_profile_name} ({aws_acct_id})",
                    "value": aws_profile_name
                })

    elif cloud_arg == "azure":
        # az account list
        cmd = ['az', 'account', 'list']
        output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(output)
        for azure_subscription in json.loads(output):
            select_options.append({
                "type": "Theia::Option",
                "label": f"{azure_subscription['name']} ({azure_subscription['id']})",
                "value": azure_subscription['id']
            })

    elif cloud_arg == "gcp":
        # gcloud config configurations list --format='value(name)'
        # cmd = ['gcloud', 'config', 'configurations', 'list', '--format=\'value(name)\'']
        cmd = ['gcloud', 'config', 'configurations', 'list']
        output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(output)
        gcp_profile_row = False
        for line in output.split("\n"):
            if gcp_profile_row and line != "":
                if line.split()[1] == "True":
                    select_options.append({
                        "type": "Theia::Option",
                        "label": f"{line.split()[0]} ({line.split()[2]}, {line.split()[3]})",
                        "value": line.split()[0],
                    })
            else:
                line_split = line.split()
                if "NAME" in line_split and "IS_ACTIVE" in line_split:
                    gcp_profile_row = True

    return select_options


    # from azure.common.client_factory import get_client_from_cli_profile
    # from azure.mgmt.resource import SubscriptionClient

    # def _run_az_cli_login():
    #     process = subprocess.Popen(
    #         ["az", "login"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    #     )
    #     for c in iter(lambda: process.stdout.read(1), b""):
    #         sys.stdout.write(c.decode(sys.stdout.encoding))

    # def list_subscriptions():
    #     logger = logging.getLogger(__name__)
    #     try:
    #         sub_client = get_client_from_cli_profile(SubscriptionClient)
    #     except Exception:
    #         logger.info("Not logged in, running az login")
    #         _run_az_cli_login()
    #         sub_client = get_client_from_cli_profile(SubscriptionClient)

    #     return [["Subscription_name", "Subscription ID"]] + [
    #         [sub.display_name, sub.subscription_id]
    #         for sub in sub_client.subscriptions.list()
    #     ]


    # from azure.mgmt.resource import SubscriptionClient

    # def list_subscriptions():
    #     logger = logging.getLogger(__name__)

    #     credential = DefaultAzureCredential()
    #     sub_client = SubscriptionClient(credential)

    #     return [["Subscription_name", "Subscription ID"]] + [
    #         [sub.display_name, sub.subscription_id]
    #         for sub in sub_client.subscriptions.list()
    #     ]



def get_account_info():
    tags = "{'tag1':'value1','tag2':'value2'}"

    setattr(kc_args, "current_session_email", session["email"])
    activation = LicenseWorker(kc_args).contact_lic_server("get_activation")

    user_activation = None
    if 'activations' in activation:
        user_activation = activation['activations'][session["email"]]
    elif 'role' in activation:
        user_activation = activation

    user_activation['email'] = session['email']
    user_activation['tier'] = activation['tier']

    return [user_activation]


def get_metadata_s3(env):
    aws_infra = generic_metadata_utils.get_data(kc_args, session, request, app_mode)
    fss_stacks = trend_utils.get_trend_filestorage_stacks(request, boto3_utils.get_boto_session(env_info=session.get("env_info")))
    logger.info(json.dumps(fss_stacks, indent=2))
    for item in aws_infra:
        item['name'] = item['resource_name']
        item['bucket'] = f"{env}-{item['resource_name']}".replace('_','-')
        for fss_stack in fss_stacks:
            if item['name'] == fss_stack['bucket']:
                item['s3_enable_trend'] = True
                item['tm_fss_stackID'] = fss_stack['tm_fss_stackID']
    aws_infra.sort(key=lambda x: x["name"])
    return aws_infra



if __name__=="__main__":
    app.run(host='0.0.0.0')
