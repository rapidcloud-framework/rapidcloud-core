__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import boto3
import argparse
import datetime
from boto3.dynamodb.conditions import Key, Attr
from jose import jwt
from six.moves.urllib.request import urlopen, Request


DEFAULT_WIZARD_EMAIL = "theia_wizard@xxxxxxxxxxxx.com"
AUTH0_DOMAIN = "theia-architecture-dev.us.auth0.com"
API_AUDIENCE = "https://architecture.kinect-theia.com/"
ALGORITHMS = ["RS256"]

session = boto3.Session()
kms_client = session.client('kms')
dynamodb_resource = session.resource('dynamodb')


def get_token(event):
    if 'Authorization' in event['headers']:
        return event['headers']['Authorization'].split()[1]
    else:
        return None


def get_email(event):
    token = get_token(event)
    if token is not None:
        jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            print(payload)
            user_info = get_user_info(token)
            print(user_info)
            return user_info['name']

    else:
        return DEFAULT_WIZARD_EMAIL


def get_user_info(token):
    request = Request(f"https://{AUTH0_DOMAIN}/userinfo")
    request.add_header("Authorization", f"Bearer {token}")
    data = urlopen(request).read().decode()
    return json.loads(data)
 

def upgrade_wizard(model, default_model):
    ids = []
    for parent in model['wizard']:
        if 'checked' in parent and parent['checked']:
            ids.append(parent['id'])
        if 'children' in parent:
            for child in parent['children']:
                if 'checked' in child and child['checked']:
                    ids.append(child['id'])
    print(ids)
    
    for parent in default_model['wizard']:
        if 'id' in parent and parent['id'] in ids:
            parent['checked'] = True
        if 'children' in parent:
            for child in parent['children']:
                if 'id' in child and child['id'] in ids:
                    child['checked'] = True
    
    return default_model


def get_model(event, email=None):
    # verify logged in
    if email is None:
        email = get_email(event)
    print(email)

    model = dynamodb_resource.Table('theia_model').query(
        KeyConditionExpression=Key('email').eq(email))['Items']
        
    if len(model) > 0:
        return model[0]


def save_model(event):
    # verify logged in
    email = get_email(event)

    body = json.loads(event['body'])
    # body = event['body']

    dynamodb_resource.Table('theia_model').put_item(Item={
        'email': email,
        'wizard': body['wizard'],
        'diagram': body['diagram'],
        'timestamp': str(datetime.datetime.now())
    })
    return get_model(event)


def json_converter(obj):
    return str(obj)


def lambda_handler(event, context): 
    print(json.dumps(event, indent=2))
    method = event['httpMethod']    
    
    if method == 'GET':
        response = get_model(event)
        if response is not None:
            default_model = get_model(event, DEFAULT_WIZARD_EMAIL)
            if 'version' not in response['diagram'] or response['diagram']['version'] != default_model['diagram']['version']:
                response = upgrade_wizard(response, default_model)

    elif method == 'POST':
        response = save_model(event)

    return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'
            },
            'body': json.dumps(response, default=json_converter)
        }    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    parser.add_argument('--email')
    args = parser.parse_args()

