__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import requests
import boto3

logger = logging.getLogger(__name__)

FILE_STORAGE_SECURITY = "filestorage"
APPLICATION_SECURITY = "application"
WORKLOAD_SECURITY = "workload"

URLS = {
    FILE_STORAGE_SECURITY: "https://filestorage.us-1.cloudone.trendmicro.com/api",
    APPLICATION_SECURITY: "https://application.us-1.cloudone.trendmicro.com",
    WORKLOAD_SECURITY: "https://workload.us-1.cloudone.trendmicro.com/api"
}

# https://cloudone.trendmicro.com/docs/workload-security/api-reference#section/Authentication
# 
# 

def call_api(env, product, method, action, params={}, boto3_session=None):
    secrets_client = boto3_session.client("secretsmanager")
    try:
        API_KEY = secrets_client.get_secret_value(SecretId="trendmicro/api_key")['SecretString']
    except:
        return None
        
    # Authentication header
    headers = { 
        "Authorization" : f"ApiKey {API_KEY}",
        "Api-Version": "v1"
    }

    url = f"{URLS[product]}/{action}"

    if product == FILE_STORAGE_SECURITY:
        params['provider'] = "aws"
    logger.info(json.dumps(params, indent=2))

    if method == "POST":
        headers["Content-Type"] = "application/json"
        result = requests.post(url, data = json.dumps(params), headers=headers).json()
    elif method == "PUT":
        result = requests.put(url, data = json.dumps(params), headers=headers)
    elif method == "GET":
        url += "?"
        for param,value in params.items():
            url += f"{param}={value}&"
        logger.info(url)
        result = requests.get(url, headers=headers).json()
    elif method == "DELETE":
        url += f"/{params['id']}"
        logger.info(url)
        result = requests.delete(url, headers=headers)

    return result
