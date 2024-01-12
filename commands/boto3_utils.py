__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging

import boto3

logger = logging.getLogger(__name__)

def get_boto_session(region="us-east-1", aws_profile=None, x_acct_role_arn=None, env_info=None):
    # logger.info(f"get_boto_session: profile: {aws_profile}, x_acct_role_arn: {x_acct_role_arn}")
    # logger.info(f"get_boto_session: env_info: {json.dumps(env_info, indent=2)}")

    if not x_acct_role_arn and not aws_profile and env_info:
        x_acct_role_arn = env_info.get("x_acct_role_arn")
        aws_profile = env_info.get("aws_profile")
        region = env_info.get("region",region)

    try:
        if x_acct_role_arn:
            sts_client = boto3.client('sts')
            src_acct_id = sts_client.get_caller_identity()["Account"]
            external_id=f"{src_acct_id}-{str(src_acct_id)[::-1]}"
            cust_acct = sts_client.assume_role(
                RoleArn = x_acct_role_arn,
                RoleSessionName="rapidcloud-x-acct-role",
                ExternalId=external_id
            )
            boto_session = boto3.Session(
                region_name = region,
                aws_access_key_id = cust_acct['Credentials']['AccessKeyId'],
                aws_secret_access_key = cust_acct['Credentials']['SecretAccessKey'],
                aws_session_token = cust_acct['Credentials']['SessionToken'])

        elif aws_profile:
            boto_session = boto3.Session(region_name=region, profile_name=aws_profile)

        else:
            boto_session = boto3.Session(region_name=region)

        return boto_session

    except Exception as e:
        print("")
        logger.error(e)
        if x_acct_role_arn:
            logger.error(f"Make sure your cross-account role `{x_acct_role_arn}` is properly configured")
        elif aws_profile:
            logger.error(f"Make sure your `{aws_profile}` AWS profile is properly configured")
        return None


def get_aws_account_from_profile(aws_profile_name):
    try:
        return get_boto_session(region="us-east-1", aws_profile=aws_profile_name).client("sts").get_caller_identity()["Account"]
    except Exception as e:
        return None

def get_aws_account_from_x_acct_role(x_acct_role_arn):
    try:
        return get_boto_session(x_acct_role_arn=x_acct_role_arn).client("sts").get_caller_identity()["Account"]
    except Exception as e:
        return None
