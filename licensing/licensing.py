#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import argparse
import copy
import http.client
import json
import logging
import os
import time
import traceback
from datetime import datetime

import boto3
import stripe
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

try:
    # lambda function mode
    import saas
except Exception as e:
    # local mode
    from licensing import saas


logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-5s:  %(message)s')
logger = logging.getLogger('licensing')
logger.setLevel(logging.INFO)

DEFAULT_TIER = "1"
PAID_TIER = "2"
ADMIN_TIER = "3"

session = saas.get_dft_boto_session({"app_env": os.environ.get("ENVIRONMENT", "dev")})
dynamodb_resource = session.resource('dynamodb')
sns_client = session.client('sns')
ses_client = session.client('ses')
s3_client = session.client('s3')
s3_resource = session.resource('s3')
secretsmanager_client = session.client('secretsmanager')
ecr_client = session.client("ecr")

ALLOW_MODULES_LIST = [
    "agree_terms",
    "console",
    "dynamodb_scan",
    "help",
    "status"
]

ALLOW_COMMANDS_LIST = [
    "init.set-env"
]

CONFIRMED_MESSAGE = "Your RapidCloud Activation has been successfully confirmed!"

STRIPE_EVENTS = [
    "checkout.session.async_payment_failed",
    "checkout.session.async_payment_succeeded",
    "checkout.session.completed",
    "checkout.session.expired",
    "checkout.session.async_payment_failed",
    "invoice.paid",
    "invoice.payment_succeeded",
    "invoice.payment_failed",
    "customer.subscription.deleted"
]


def get_table(table_name="theia_client_activation"):
    return dynamodb_resource.Table(table_name)


def allow_command(module, command, permissions):
    cmd = f"kc {module}"
    if command:
        cmd += f" {command}"

    cmd = f"{module}.{command}"
    logger.info(f"verifying permission for `{cmd}`:")
    allow = False

    if module in ALLOW_MODULES_LIST or cmd in ALLOW_COMMANDS_LIST or permissions.get("access_all", "none") == "read-write" or permissions.get(f"access_{module}", "none") == "read-write":
        allow = True

    return allow


def get_confirm_html(email, code):
    url = os.environ['LIC_URL']
    href= f"{url}/license/activate?action=confirm_activation&email={email}&code={code}"
    logger.info(href)
    return f'''
        <br/>
        &nbsp;&nbsp;<a href={href}>Confirm your RapidCloud Activation</a>
        <br/><br/>
        &nbsp;&nbsp;Sincerely,
        <br/>
        &nbsp;&nbsp;The RapidCloud Team.
        '''


def verify(body):
    email, feature, cloud = body['email'], body['feature'], body.get('cloud','aws')
    msg = None
    if email is not None:
        activation = get_activation(body)
        if activation:
            permissions = {}

            if activation['tier'] == PAID_TIER and 'stripe' in activation:
                # allow 48 hours to fix the payment
                if time.time() - 48 * 60 * 60 > activation['stripe']['current']['period_end']:
                    msg = "Downgrading to FREE tier"
                    logger.warning(msg)
                    activation['tier'] = DEFAULT_TIER
                    get_table().put_item(Item=activation)

            try:
                if 'activations' in activation:
                    user_activation = activation['activations'][email]
                elif 'role' in activation:
                    user_activation = activation
                else:
                    user_activation = None

                if user_activation is not None:
                    activation_confirmed = user_activation['status'] == 'active'

            except Exception as e:
                msg = "Activation cannot be retrieved"
                logger.warning(msg)
                activation_confirmed = False
                traceback.print_exc()

            # try:
            #     agreed_terms = activation['agreed_terms'][email]['agreed'] == 'yes'
            # except Exception as e:
            #     msg = "You have not agreed to RapidCloud terms yet"
            #     logger.warning(msg)
            #     agreed_terms = False
            #     traceback.print_exc()

            try:
                verified = True
                if verified and user_activation and 'roles' in activation:
                    permissions = activation["roles"][user_activation.get("role", "RAPIDCLOUD_VIEWER")]
                else:
                    permissions = get_default_roles()[user_activation.get("role", "RAPIDCLOUD_VIEWER")]

            except Exception as e:
                msg = e
                logger.warning(e)
                logger.warning(msg)
                verified = False
                traceback.print_exc()

            try:
                authorized = False
                if feature:
                    feature_tiers = get_table('theia_subscription_tiers').query(
                            KeyConditionExpression=Key('feature').eq(feature))['Items']
                    if len(feature_tiers) > 0:
                        authorized = activation['status'] == 'active' and activation['tier'] in feature_tiers[0]['tiers'].split(',')
                    else:
                        logger.warning(f"Feature {feature} has no data in theia_subscription_tiers")
                        authorized = activation['tier'] in [PAID_TIER, ADMIN_TIER]
                else:
                    logger.warning("feature was not passed")

            except Exception as e:
                msg = f"Verification failed: {e.response['Error']['Message']}"
                logger.warning(msg)
                traceback.print_exc()

            return {
                "cloud": cloud,
                "email": email,
                "tier": activation['tier'] if 'tier' in activation else DEFAULT_TIER,
                "activation_confirmed": activation_confirmed,
                "agreed_terms": True,
                "verified": verified,
                "authorized": authorized,
                "msg": msg,
                "permissions": permissions
            }

    else:
        if feature not in ALLOW_MODULES_LIST:
            msg = f"Your RapidCloud instance has not been properly activated. Have you activated RapidCloud for {cloud.upper()}? "

    return {
        "cloud": cloud,
        "email": email,
        "activation_confirmed": False,
        "agreed_terms": None,
        "verified": False,
        "authorized": False,
        "msg": msg
    }


def send_confirm_email(body):
    SENDER = "RapidCloud  <iroyzis@gmail.com>"
    RECIPIENT = body['email']
    BCC_RECIPIENT = "iroyzis@gmail.com"
    SUBJECT = "RapidCloud Activation - Please Confirm"
    BODY_HTML = get_confirm_html(RECIPIENT, body['activation']['code'])
    CHARSET = "UTF-8"

    try:
        logger.info(f"sending confirmation email to {RECIPIENT}")
        response = ses_client.send_email(
            Destination={'ToAddresses': [RECIPIENT,],'BccAddresses': [BCC_RECIPIENT,],},
            Message={
                'Body': {
                    'Html': {'Charset': CHARSET,'Data': BODY_HTML,},
                    'Text': {'Charset': CHARSET,'Data': BODY_HTML,},
                },
                'Subject': {'Charset': CHARSET,'Data': SUBJECT,},
            },
            ReplyToAddresses=[
                'support@rapid-cloud.io',
            ],
            Source=SENDER
        )
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
        # traceback.print_exc()
    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])


def agree_terms(body):
    email, config = body['email'], body['config']
    activation = get_activation(body, include_free_domains=True)
    if 'agreed_terms' not in activation:
        activation['agreed_terms'] = {}
    if email not in activation['agreed_terms']:
        activation['agreed_terms'][email] = {
            "agreed": "yes",
            "config": config,
            "timestamp": str(datetime.now())
        }
        logger.info(json.dumps(activation, indent=2, default=str))
        get_table().put_item(Item=activation)
    return activation['agreed_terms']


def send_subscription_limit_email(account):
    try:
        SENDER = "iroyzis@gmail.com"
        RECIPIENT = "support@rapid-cloud.io"
        BCC_RECIPIENT = "iroyzis@gmail.com"
        SUBJECT = f"Maximum allowed activations reached"
        CHARSET = "UTF-8"
        BODY_HTML = f"""
        Maximum allowed activations reached
        <br/><br/>
        Current count: {len(account['activations'])}
        <br/><br/>
        {json.dumps(account['activations'], indent=2, default=str)}
        """
        logger.info(f"sending subscription limit email to {RECIPIENT}")
        response = ses_client.send_email(
            Destination={'ToAddresses': [RECIPIENT,],'BccAddresses': [BCC_RECIPIENT,],},
            Message={
                'Body': {
                    'Html': {'Charset': CHARSET,'Data': BODY_HTML,},
                    'Text': {'Charset': CHARSET,'Data': BODY_HTML,},
                },
                'Subject': {'Charset': CHARSET,'Data': SUBJECT,},
            },
            Source=SENDER
        )
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
        traceback.print_exc()
    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])
        traceback.print_exc()


def download(body):
    SENDER = "iroyzis@gmail.com"
    RECIPIENT = "support@rapid-cloud.io"
    BCC_RECIPIENT = "iroyzis@gmail.com"
    SUBJECT = f"RapidCloud Download for {body['os']}, {body['email']}"
    CHARSET = "UTF-8"
    BODY_HTML = f"{body['email']}: {body['os']}"
    try:
        logger.info(f"sending download email to {RECIPIENT}")
        response = ses_client.send_email(
            Destination={'ToAddresses': [RECIPIENT,],'BccAddresses': [BCC_RECIPIENT,],},
            Message={
                'Body': {
                    'Html': {'Charset': CHARSET,'Data': BODY_HTML,},
                    'Text': {'Charset': CHARSET,'Data': BODY_HTML,},
                },
                'Subject': {'Charset': CHARSET,'Data': SUBJECT,},
            },
            Source=SENDER
        )
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
        traceback.print_exc()
    else:
        logger.info("Email sent! Message ID:")
        logger.info(response['MessageId'])
        traceback.print_exc()

    return f"https://rapid-cloud.s3.amazonaws.com/downloads/rapid-cloud-LATEST-{body['os'].lower()}.zip"


def auth0_callback(body):
    logger.info("in auth0_callback")
    if "email" in body:
        body.update({
            "phone": "",
            "hostname": "auth0",
            "config": {
                "aws_profile": "",
                "phone": ""
            }
        })

        # activate email and domain if it's the first activation
        activation = activate(body, from_auth0=True)

        # create SaaS tenant
        if not is_free_domain(body):
            tenant = saas.create_tenant(body)

    return body


def get_default_roles():
    return {
        "RAPIDCLOUD_ADMIN": {
            "access_all": "read-write",
            "access_description": "RapidCloud Administrator Role"
        },
        "RAPIDCLOUD_VIEWER": {
            "access_all": "read-only",
            "access_description": "RapidCloud View Role"
        }
    }


def activate(body, from_auth0=False):
    email, phone, hostname, config = body['email'], body['phone'], body['hostname'], body['config']
    domain = email.split('@')[1]
    activation = get_activation(body)
    assign_default_role = False
    if not activation:
        # new activation
        assign_default_role = True
        logger.info(f"Activating {domain} ...")
        item = {
            'domain': domain,
            'email': email,
            'phone': phone,
            "hostname": hostname,
            'tier': DEFAULT_TIER,
            'timestamp': str(datetime.now()),
            'status': "active",
            'apps': "aws,azure,gcp",
            'activations': {}
        }
    else:
        item = activation
        logger.info(f"{domain} has been activated on {activation['timestamp']}")

    # new org activation
    if 'activations' not in item:
        item['activations'] = {}

    # check for existing active activation for email/hostname
    existing_active_user = False
    if not from_auth0 and email in item['activations']:
        act_item = item['activations'][email]
        logger.info(f"existing activation for {email}")
        logger.info(json.dumps(act_item, indent=2, default=str))
        if act_item["status"] == "active": # and act_item["hostname"] == hostname:
            existing_active_user = True
            logger.info(f"ignoring activation for {email}")

    # new user activation or repeat activation for pending user
    if not existing_active_user:
        activation_code = int(round(time.time() * 1000))
        item['activations'][email] = {
            "from_auth0": from_auth0,
            "code": activation_code,
            "status": "pending",
            "hostname": hostname,
            "aws_profile": config.get('aws_profile',''),
            "azure_subscription": config.get('subscription',''),
            "gcp_profile": config.get('gcp_profile',''),
            "phone": config.get('phone',''),
            'timestamp': str(datetime.now())
        }

        # default account roles and default first user (admin) role
        if assign_default_role:
            item["roles"] = get_default_roles()
            item['activations'][email]["role"] = "RAPIDCLOUD_ADMIN"
        elif "role" not in item['activations'][email]:
            item['activations'][email]["role"] = "RAPIDCLOUD_VIEWER"

        get_table().put_item(Item=item)

        # send confirmation email
        body['activation'] = item['activations'][email]
        send_confirm_email(body)
        logger.info(f"{domain}: {len(item['activations'])} activations")
        if len(item['activations']) > 10:
            send_subscription_limit_email(item)

    return item


def update_ecr_policy(acct):
    ecr_repo_policy = ecr_client.get_repository_policy(repositoryName="file_workflow_lambda")
    policy = json.loads(ecr_repo_policy["policyText"])
    accts = policy["Statement"][0]["Condition"]["ForAnyValue:StringEquals"]["aws:SourceAccount"].split(',')
    if acct not in accts:
        accts.append(acct)
        policy["Statement"][0]["Condition"]["ForAnyValue:StringEquals"]["aws:SourceAccount"] = accts
        response = ecr_client.set_repository_policy(
            repositoryName='file_workflow_lambda',
            policyText=json.dumps(policy, indent=2),
            force=True
        )
        logger.info(response)
    return {}


def set_account_permissions(body):
    update_ecr_policy(body["extra_params"]["account"])
    return {}


def save_role(body, verify_result):
    role = body["extra_params"]["role"]
    activation = get_activation(body)
    if allow_command("access", "create_role", verify_result["permissions"]):
        if "roles" not in activation:
            activation["roles"] = {}
        roles = activation["roles"]
        roles[role["name"]] = role
        get_table().put_item(Item=activation)


def assign_role(body, verify_result):
    user_email = body["extra_params"]["email"]
    user_role = body["extra_params"]["role"]
    ux_context = body["extra_params"].get("ux_context", "admin")
    activation = get_activation(body)
    if allow_command("access", "assign_role", verify_result["permissions"]):
        if user_email in activation["activations"]:
            user = activation["activations"][user_email]
            user["role"] = user_role
            user["ux_context"] = ux_context
            get_table().put_item(Item=activation)


def confirm_activation(body):
    if 'extra_params' in body:
        email = body['extra_params']['email']
        code = body['extra_params']['code']
    else:
        email = body['email']
        code = body['code']
    activation = get_activation(body, include_free_domains=True)

    if email in activation['activations']:
        user_activation = activation['activations'][email]
        if user_activation['status'] == 'pending' and str(user_activation['code']) == str(code):
            logger.info(f"Confirmed RapidCloud activation for {email}")
            user_activation['status'] = 'active'
            user_activation['timestamp'] = str(datetime.now())
            get_table().put_item(Item=activation)
        else:
            logger.info(f"Activation Confirmation is not valid")
        return user_activation
    return None


def redirect_to_auth0_confirm(body):
    env = os.environ['ENVIRONMENT'].upper()
    AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

    # 1. get token
    payload = {
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials"
    }

    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", json.dumps(payload, default=str), headers)
    token = json.loads(conn.getresponse().read().decode("utf-8"))
    logger.info(f"\n{json.dumps(token, indent=2, default=str)}")

    # 2. get user id
    headers = {
        "content-type": "application/json",
        "authorization": f"{token['token_type']} {token['access_token']}"
    }
    conn.request("GET", f"/api/v2/users-by-email?email={body['email']}", headers=headers)
    user_id = json.loads(conn.getresponse().read().decode("utf-8"))[0]["user_id"]

    # 3. get verify link
    payload = {
        "user_id": user_id,
    }
    conn.request("POST", "/api/v2/tickets/email-verification", json.dumps(payload, default=str), headers)
    ticket_url = json.loads(conn.getresponse().read().decode("utf-8"))["ticket"]

    # 4. redirect to auth0 confirmed email page
    return {
        'isBase64Encoded': False,
        'statusCode': 302,
        'headers': {
            'Location': ticket_url,
        }
    }


def create_subdomain(body):
    # check to make sure it's either RC admin or an active customer
    allow = True
    if body["feature"] != "admin":
        user = get_user_activation(body)
        if not user or user["status"] != "active":
            allow = False
    if not allow:
        logger.warning("create_subdomain is not allowed")
        return None

    sts_client = boto3.Session().client('sts')
    subdomain = body['extra_params']['subdomain']
    public_ip = body['extra_params']['public_ip']
    shared_acct = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::504938655456:role/rapidcloud-add-route53-record-{body['env']}-role",
        RoleSessionName=f"CreateSubdomain-{subdomain}"
    )
    logger.info(shared_acct)

    route53_client = boto3.client(
        'route53',
        aws_access_key_id=shared_acct['Credentials']['AccessKeyId'],
        aws_secret_access_key=shared_acct['Credentials']['SecretAccessKey'],
        aws_session_token=shared_acct['Credentials']['SessionToken'],
    )
    logger.info(route53_client)

    try:
        response = route53_client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': subdomain,
                            'ResourceRecords': [
                                {
                                    'Value': public_ip,
                                },
                            ],
                            'TTL': 60,
                            'Type': 'A',
                        },
                    },
                ]
            },
            HostedZoneId='Z0492496FEX20GV7IWTO'
        )
        logger.info(json.dumps(response, indent=2, default=str))
        return response
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return e


def is_free_domain(body):
    root_dir = os.environ.get('LAMBDA_TASK_ROOT')
    if root_dir is None:
        root_dir = "./licensing"
    file = open(f"{root_dir}/free_domains.txt", "r")
    content_list = file.read().splitlines()
    domain = body['email'].split('@')[1]
    is_free = domain in content_list
    if is_free:
        logger.info(f"free domain: {domain}")
    return is_free


def upgrade(body):
    activation = get_activation(body)
    if activation is not None:
        logger.info(json.dumps(activation, indent=2, default=str))
        object = body['data']['object']
        activation['tier'] = PAID_TIER
        activation['status'] = 'active'
        activation['timestamp'] = str(datetime.now())
        if 'stripe' not in activation:
            activation['stripe'] = {}
        activation['stripe'][object['id']] = {
            "amount_paid": object['amount_paid'],
            "hosted_invoice_url": object['hosted_invoice_url'],
            "subscription": object['lines']['data'][0]['subscription'],
            "period_start": object['lines']['data'][0]['period']['start'],
            "period_end": object['lines']['data'][0]['period']['end']
        }
        activation['stripe']['current'] = activation['stripe'][object['id']]
        activation['stripe']['current']['auto-renewal'] = True

        get_table().put_item(Item=activation)


def stripe_callback(body):
    logger.info(f"stripe_callback:\n{json.dumps(body, indent=2)}\n")
    type = body['type']
    try:
        email = body['data']['object']['customer_email']
    except:
        email = None
        pass
    logger.info(f"Stripe [{type}] {email}")
    if type == "invoice.payment_succeeded":
        body['email'] = email
        upgrade(body)


def cancel_subscription(body):
    activation = get_activation(body)
    if 'stripe' in activation and 'current' in activation['stripe'] and 'subscription' in activation['stripe']['current']:
        try:
            secret_id = f"{os.environ['ENVIRONMENT']}/stripe/api"
            stripe_api_secret = secretsmanager_client.get_secret_value(SecretId=secret_id)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
        else:
            if 'SecretString' in stripe_api_secret:
                # cancel in Stripe
                subscription_id = activation['stripe']['current']['subscription']
                logger.info(f"cancelling RapidCloud Premium Subscription {subscription_id}")
                stripe.api_key = json.loads(stripe_api_secret['SecretString'])['secret']
                try:
                    resp = stripe.Subscription.delete(subscription_id)
                    logger.info(json.dumps(resp, indent=2, default=str))
                except Exception as e:
                    logger.error(e)
                    traceback.print_exc()

                # mark cancelled in RapidCloud
                activation['stripe']['current']['auto-renew'] = False
                get_table().put_item(Item=activation)
                logger.info(json.dumps(activation, indent=2, default=str))

                return activation


def verify_activation_code(body):
    email, token, config = body['email'], body['token'], body['config']
    logger.info(email)
    logger.info(token)
    verified = False
    activation = get_activation(body)
    if activation:
        verified = activation['token'] == token
    return {"verified": verified}


def get_activation(body, include_free_domains=False):
    email = body['email']
    domain = email.split('@')[1]
    activations = get_table().query(KeyConditionExpression=Key('domain').eq(domain))['Items']
    if len(activations) > 0:
        activation = activations[0]
        if not include_free_domains and is_free_domain(body):
            return get_user_activation(body, activation=activation)
        return activation
    return None


def get_user_activation(body, activation=None):
    user_activation = None
    if activation is None:
        activation = get_activation(body)
    if activation:
        if 'activations' in activation:
            user_activation = activation['activations'][body['email']]
        elif 'role' in activation:
            user_activation = activation

        if user_activation:
            user_activation['email'] = body['email']
            user_activation['tier'] = activation['tier']

    return user_activation


def get_tiers(body):
    return get_table('theia_subscription_tiers').scan()['Items']

def get_app_context(body):
    return get_table('rapidcloud_ux_context').query(
        KeyConditionExpression=Key('setting').eq("app_context"))['Items'][0]


def print_event_string(body):
    event_str = ["EVENT -> "]
    if 'env' in body: event_str.append(f"env={body['env']},")
    if 'email' in body: event_str.append(f"email={body['email']},")
    if 'action' in body: event_str.append(f"action={body['action']},")
    if 'feature' in body: event_str.append(f"feature={body['feature']},")
    if 'hostname' in body: event_str.append(f"hostname={body['hostname']},")
    if 'extra_params' in body: event_str.append(f"extra_params={body['extra_params']},")
    logger.info(" ".join(event_str))


def save_event(body):
    try:
        logger.info(f"Licensing Event:")
        logger.info(json.dumps(body, indent=2))
        events_bucket = f"rapid-cloud-{body['env']}"

        email, domain, env, feature, command = 'none', 'none', 'none', 'none', 'none'
        if "email" in body and body["email"] is not None and body["email"] != "":
            email = body["email"]
            domain = email.split('@')[1]
        if 'config' in body and 'env' in body['config']:
            env = body['config']['env']
        if 'feature' in body:
            feature = body['feature']
        if 'command' in body:
            command = body['command']

        timestamp = str(datetime.now()).split('.')[0].replace(' ','_')
        event_file = f"events/domain_p={domain}/env_p={env}/feature_p={feature}/command_p={command}/email_p={email}/{timestamp}.json"
        s3object = s3_resource.Object(events_bucket, event_file)
        logger.info(f"saving {event_file}")

        body_flat = flatten(copy.deepcopy(body), "config", fully_qualify_nested=True)
        body_flat = flatten(body_flat, "extra_params", fully_qualify_nested=True)
        # logger.info(json.dumps(body_flat, indent=2, default=str))
        s3object.put(Body=(bytes(json.dumps(body_flat).encode('UTF-8'))))

    except Exception as e:
        logger.error(e)
        traceback.print_exc()


def lambda_handler(event, context):
    # logger.info(f"Licensing Event:\n{json.dumps(event, indent=2)}\n")
    local_mode = os.getenv('RAPIDCLOUD_MODE') == 'local'

    body = {}
    try:
        if not local_mode:
            if 'httpMethod' in event and event['httpMethod'] == 'POST':
                if event['queryStringParameters'] and event['queryStringParameters']['action'] == 'download':
                    name = ""
                    for line in event['body'].split("\r\n"):
                        if "Content-Disposition:" in line:
                            name = line.split("name=")[-1].replace('\"', '')
                        elif line and "--" not in line:
                            body[name] = line
                else:
                    if 'body' in event:
                        body = json.loads(event['body'])
            elif 'httpMethod' in event and event['httpMethod'] == 'GET':
                body = event['queryStringParameters']
            elif 'type' in event and event['type'] in STRIPE_EVENTS:
                response = stripe_callback(event)
                return {
                    'statusCode': 200,
                    'body': response
                }
        else:
            body = json.loads(event['body'])

        body["execution_mode"] = "local" if local_mode else "lambda"
        body['env']  = "dev"

        if 'requestContext' in event:
            logger.info(event['requestContext']['path'])
            if 'live/' in event['requestContext']['path']:
                body['env'] = "live"

        print(json.dumps(body, indent=2, default=str))

        # if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None:
        #     save_event(body)
        # else:
        #     print(json.dumps(body, indent=2, default=str))

        if 'config' not in body:
            body['config'] = {}

        if local_mode:
            action = body["action"]
        else:
            action = body.get('action', event["resource"].split("/")[-1])

        # verify
        if action not in ['activate','verify','console'] and 'feature' in body:
            logger.info("verifying access again, in case someone is trying to hack in ...")
            verify_result = verify(body)
            if not verify_result['verified']:
                logger.warning(json.dumps(verify_result, indent=2, default=str))
                return {
                    'statusCode': 401,
                    'body': json.dumps(verify_result, default=str)
                }

        if action == 'verify':
            response = verify(body)

        elif action == 'download':
            response = download(body)

        elif action == 'activate':
            response = activate(body)

        elif action == 'set_account_permissions':
            response = set_account_permissions(body)

        elif action == 'save_role':
            response = save_role(body, verify_result)

        elif action == 'assign_role':
            response = assign_role(body, verify_result)

        elif action == 'confirm_activation':
            user_activation = confirm_activation(body)
            if user_activation["from_auth0"]:
                return redirect_to_auth0_confirm(body)
            else:
                response = CONFIRMED_MESSAGE

        elif action == 'agree_terms':
            response = agree_terms(body)

        elif action == 'get_activation':
            response = get_activation(body)

        elif action == 'get_user_activation':
            response = get_user_activation(body)

        elif action == 'get_tiers':
            response = get_tiers(body)

        elif action == 'get_app_context':
            response = get_app_context(body)

        elif action == 'cancel_subscription':
            response = cancel_subscription(body)

        elif action == 'auth0_callback':
            response = auth0_callback(body)

        elif action == 'create_subdomain': # used for setting up *.rapid-cloud.io subdomain
            logger.info("create_subdomain")
            response = create_subdomain(body)

        elif action == 'auth0_login':
            response = saas.auth0_login(body)

        elif action == "saas":
            user_activation = get_user_activation(body)
            if not is_free_domain(body):
                args = {}
                for arg in ["action", "domain", "email", "output_key", "cmd", "x_acct_role_arn", "x_acct_role_env", "x_acct_role_region", "tenant_instance_role_arn"]:
                    args[arg] = body.get("extra_params",{}).get(arg)
                response = saas.exec(args)
            else:
                response = {}

        if response is None:
            response = body

        response = {
            'isBase64Encoded': False,
            'statusCode': 200,
            'body': json.dumps(response, default=str)
        }

    except Exception as e:
        logger.info(e)
        traceback.print_exc()
        response = {
            'isBase64Encoded': False,
            'statusCode': 500,
            'body': e
        }

    # logger.info(f"Licensing Response:\n{json.dumps(response, indent=2, default=str)}\n")
    return response


def save_tiers(aws_profile):
    dynamo_res = boto3.Session(profile_name=aws_profile).resource('dynamodb')
    with open("licensing/tiers.json") as f:
        tiers = json.load(f)
        for tier in tiers:
            logger.info(tier)
            dynamo_res.Table('theia_subscription_tiers').put_item(Item=tier)


def show_tiers(aws_profile):
    dynamo_res = boto3.Session(profile_name=aws_profile).resource('dynamodb')
    items = dynamo_res.Table('theia_subscription_tiers').scan()['Items']
    for item in items:
        logger.info(f"{item['feature']} -> {item['tiers']}")


def show_allowed_apps(aws_profile, domain):
    dynamo_res = boto3.Session(profile_name=aws_profile).resource('dynamodb')
    items = dynamo_res.Table('theia_client_activation').query(
        KeyConditionExpression=Key('domain').eq(domain))['Items']
    allowed_apps = items[0]["apps"].split(',')
    logger.info(json.dumps(allowed_apps, indent=2, default=str))
    return allowed_apps


def update_allowed_apps(aws_profile, domain, app, action):
    apps = show_allowed_apps(aws_profile, domain)
    if action == "add":
        if app not in apps:
            apps.append(app)
    elif action == "remove":
        if app in apps:
            apps.remove(app)
    dynamo_res = boto3.Session(profile_name=aws_profile).resource('dynamodb')
    dynamo_res.Table('theia_client_activation').update_item(
        Key = {"domain": domain},
        UpdateExpression = "SET apps = :apps",
        ExpressionAttributeValues = {":apps": ','.join(apps)}
    )
    show_allowed_apps(aws_profile, domain)


def save_app_context(aws_profile):
    dynamo_res = boto3.Session(region_name="us-east-1", profile_name=aws_profile).resource('dynamodb')
    with open("./server/console/template/app_context.json") as f:
        app_context = json.load(f)
        dynamo_res.Table('rapidcloud_ux_context').put_item(
            Item = {"setting": "app_context", "data": app_context})


def flatten(body, sub_item_name, exclude_cols=[], fully_qualify_nested=False):
    if sub_item_name not in body:
        return body
    for col in exclude_cols:
        if col in body[sub_item_name]:
            del body[sub_item_name][col]
    if fully_qualify_nested:
        for k,v in body[sub_item_name].items():
            body[f"{sub_item_name}.{k}"] = v
    else:
        body.update(body[sub_item_name])
    body.pop(sub_item_name)
    return body


if __name__ == "__main__":
    # --action save_tiers --profile [default | rc_prod]
    parser = argparse.ArgumentParser()
    for arg in ["action", "profile", "domain", "email", "output_key", "cmd", "app", "app_action"]:
        parser.add_argument(f'--{arg}')
    args = parser.parse_args()

    if args.action == 'save_tiers':
        save_tiers(args.profile)
    elif args.action == 'show_tiers':
        show_tiers(args.profile)
    elif args.action == 'save_app_context':
        save_app_context(args.profile)
    elif args.action == 'show_allowed_apps':
        show_allowed_apps(args.profile, args.domain)
    elif args.action == 'update_allowed_apps':
        update_allowed_apps(args.profile, args.domain, args.app, args.app_action)

    else:
        params = {
            "action": "saas",
            "email": args.email,
            "extra_params": {}
        }
        for arg in ["action", "profile", "domain", "email", "output_key", "cmd"]:
            params["extra_params"][arg] = getattr(args, arg, None)
        if getattr(args, arg, None) is not None:
            saas.aws_profile = getattr(args, arg)
        lambda_handler({
            "resource": "/license/activate",
            "path": "/license/activate",
            "httpMethod": "GET",
            "queryStringParameters": params
        }, None)
