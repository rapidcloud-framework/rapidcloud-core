#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import traceback
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from commands import boto3_utils

logger = logging.getLogger("aws_utils")
logger.setLevel(logging.INFO)


def option(data, label, value):
    return {
        "type": "Theia::Option",
        "label": label,
        "value": {
            "type": "Theia::DataOption",
            "value": value,
            "data": data
        }
    }       

def get_form_data_from_aws(request, session):
    print(f"type={request.args['type']}")
    print(f"get form data from aws args: {request.args}")
    form_data = []

    env = request.args.get('env')
    if env:
        with open(f"./config/environments/{env}_config.json", 'r') as f:
            config = json.load(f)
            region = config["region"]
    else:
        with open(f"./config/aws_profile.json", 'r') as f:
            config = json.load(f)
            region = config["default_region"]
    try:
        aws_profile = config["aws_profile"]
        env_vpc_id = config.get('vpc')
    except KeyError as e:
        # logger.error(f"get_form_data_from_aws {e}")
        return form_data

    boto3_session = boto3_utils.get_boto_session(region=region, aws_profile=aws_profile)
    logger.info(f"region={region}, aws_profile={aws_profile}")


    if request.args['type'] == "key_pairs":
        get_key_pairs(request, env, boto3_session, form_data)

    elif request.args['type'] == "vpcs":
        get_vpcs(request, env, boto3_session, form_data)

    elif request.args['type'] == "vpc_security_groups":
        get_vpc_security_groups(request, env, boto3_session, env_vpc_id, form_data)

    elif request.args['type'] == "availability_zones":
        get_availability_zones(request, env, boto3_session, form_data)
    
    elif request.args['type'] == "subnets":
        get_subnets(request, env, boto3_session, env_vpc_id, form_data)

    elif request.args['type'] == "roles":
        get_roles(request, env, boto3_session, form_data)

    elif request.args['type'] == "amis":
        get_amis(request, env, boto3_session, form_data)

    elif request.args['type'] == "buckets":
        get_buckets(request, env, boto3_session, form_data)
    
    elif request.args['type'] == "datasync_locations":
        get_datasync_locations(request, env, boto3_session, form_data)
    
    elif request.args['type'] == "subnet_arns":
        get_subnets_arns(request, env, boto3_session, env_vpc_id, form_data)

    elif request.args['type'] == "generate_presigned_url":
        generate_presigned_url(request, session, env, boto3_session, form_data)

    return form_data


def get_vpc_security_groups(request, env, boto3_session, env_vpc_id, form_data):
    # resp = boto3_client("ec2",region).describe_security_groups(Filters=[
    #     {'Name': 'tag:env', 'Values': [env]}
    # ])
    resp = boto3_session.client("ec2").describe_security_groups()
    sec_groups = resp['SecurityGroups']
    sec_groups.sort(key=lambda x: x["GroupName"])
    for item in sec_groups:
        use = True
        # make sure sec group in curr env vpc
        if item['VpcId'] != env_vpc_id:
            continue
        
        if 'Tags' in item:
            for tag in item['Tags']:
                if tag['Key'] == "profile" and tag['Value'] != env:
                    use = False
                    break

        if use:
            form_data.append(option(item, f"{item['GroupName']} ({item['Description']})", item['GroupId']))


def get_subnets(request, env, boto3_session, env_vpc_id, form_data):
    filters = []
    if 'vpc_id' in request.args:
        filters.append({'Name': 'vpc-id', 'Values': [request.args["vpc_id"]]})
    else:
        filters.append({'Name': 'vpc-id', 'Values': [env_vpc_id]})
    if 'az' in request.args:
        filters.append({'Name': 'availability-zone', 'Values': [request.args['az']]})
    logger.info(f"env_vpc_id={env_vpc_id}")
    resp = boto3_session.client("ec2").describe_subnets(Filters=filters)
    subnets = resp['Subnets']
    subnets.sort(key=lambda x: x["SubnetId"])
    for item in subnets:
        if 'Tags' in item:
            pub_pri = None
            for tag in item['Tags']:
                if tag['Key'] == 'Tier':
                    pub_pri = tag['Value']
                    break
            form_data.append(option(item, f"{item['SubnetId']} ({item['AvailabilityZone']}, {pub_pri})", item['SubnetId']))


def get_subnets_arns(request, env, boto3_session, env_vpc_id, form_data):
    filters = []
    if 'vpc_id' in request.args:
        filters.append({'Name': 'vpc-id', 'Values': [request.args["vpc_id"]]})
    else:
        filters.append({'Name': 'vpc-id', 'Values': [env_vpc_id]})
    if 'az' in request.args:
        filters.append({'Name': 'availability-zone', 'Values': [request.args['az']]})
    resp = boto3_session.client("ec2").describe_subnets(Filters=filters)
    subnets = resp['Subnets']
    subnets.sort(key=lambda x: x["SubnetId"])
    for item in subnets:
        if 'Tags' in item:
            pub_pri = None
            for tag in item['Tags']:
                if tag['Key'] == 'Tier':
                    pub_pri = tag['Value']
                    break
            form_data.append(option(item, f"{item['SubnetId']} ({item['AvailabilityZone']}, {pub_pri})", item['SubnetArn']))


def get_roles(request, env, boto3_session, form_data):
    iam_client = boto3_session.client("iam")
    resp = iam_client.list_roles()
    roles = resp['Roles']
    while resp['IsTruncated']:
        resp = iam_client.list_roles(Marker=resp['Marker'])
        roles += resp['Roles']
    for item in roles:
        if env in item['RoleName'] or env.replace('_','-') in item['RoleName']:
            form_data.append(option(item, f"{item['RoleName']}", item['RoleName']))


def get_availability_zones(request, env, boto3_session, form_data):
    resp = boto3_session.client("ec2").describe_availability_zones()
    for item in resp['AvailabilityZones']:
        form_data.append(option(item, f"{item['ZoneName']}", item['ZoneName']))


def get_key_pairs(request, env, boto3_session, form_data):
    resp = boto3_session.client("ec2").describe_key_pairs()
    for item in resp['KeyPairs']:
        form_data.append(option(item, f"{item['KeyName']}", item['KeyName']))


def get_vpcs(request, env, boto3_session, form_data):
    resp = boto3_session.client("ec2").describe_vpcs()
    for item in resp['Vpcs']:
        label = item['VpcId']
        if "Tags" in item:
            for tag in item["Tags"]:
                if tag['Key'] == "Name":
                    label += f" ({tag['Value']})"
                    break
        form_data.append(option(item, label, item['VpcId']))


def get_amis(request, env, boto3_session, form_data):
    dft_amis = {
        "ami-0022f774911c1d690": "Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2 (ami-0022f774911c1d690), Free Tier eligible",
        "ami-0c4e4b4eb2e11d1d4": "Amazon Linux 2 AMI 2.0.20221004.0 x86_64 HVM gp2 (ami-0c4e4b4eb2e11d1d4), Free Tier eligible",
        "ami-017cdd6dc706848b2": "Microsoft Windows Server 2022 Full Locale English AMI provided by Amazon (ami-017cdd6dc706848b2), Free Tier eligible",
        "ami-026bb75827bd3d68d": "Microsoft Windows Server 2019 with Desktop Experience Locale English AMI provided by Amazon (ami-026bb75827bd3d68d), Free Tier eligible"
    }
    
    form_data.append(option("", "", ""))
    for ami_id, description in dft_amis.items():
        form_data.append(option("", description, ami_id))

    resp = boto3_session.client("ec2").describe_images(Owners=['self'])
    for item in resp['Images']:
        label = f"{item['Name']} ({item['ImageId']})"
        form_data.append(option(item, label, item['ImageId']))

def get_datasync_locations(request, env, boto3_session, form_data):
    resp = boto3_session.client("datasync").list_locations()
    for item in resp['Locations']:
        tags = boto3_session.client("datasync").list_tags_for_resource(ResourceArn=f"{item['LocationArn']}")
        if 'Tags' in tags:
            for tag in tags['Tags']:
                if tag['Key'] == "profile" and tag['Value'] == env:
                    loc_id = item['LocationArn'].split(":")[5]
                    label = f" {item['LocationUri']} ({loc_id})"
                    form_data.append(option(item, label, item['LocationArn']))

def get_buckets(request, env, boto3_session, form_data):
    s3 = boto3_session.client("s3")
    buckets = s3.list_buckets()
    for b in buckets['Buckets']:
        if env.replace("_","-") in b['Name']:
            label = f"{b['Name']}"
            form_data.append(option(b, label, b['Name']))


def generate_presigned_url(request, session, env, boto3_session, form_data):
    try:
        # /api/formdata_from_aws
        #   ?type=generate_presigned_url
        #   &dataset_type=dataset_unstructured
        #   &dataset=invoices
        #   &samples=
        #   &env=igor_160_test
        #   &file_name=invoices_5148981404-MTMDODHWY_2023-02-01.pdf&cloud=aws

        file_name = request.args["file_name"] # file being uploaded
        dataset_type = request.args["dataset_type"] # dataset_unstructured, dataset_semi_structured, code
        if dataset_type == "code":
            bucket_suffix = request.args.get("bucket-suffix", "utils")
            folder1 = "code"
            object_key = f"code/{file_name}".replace(' ', '_')
        else:
            bucket_suffix = request.args.get("bucket-suffix", "ingestion")
            folder1 = "files" if dataset_type == "dataset_unstructured" else "semistructured"
            samples = request.args["samples"]
            dataset_name = request.args.get("dataset") # e.g. Unknown, invoices, medical_records
            folder2 = "rc-samples" if samples == "true" else "rc-any" if dataset_name == "Unknown" else dataset_name
            dt = datetime.today()
            partition = f"{dt.year}/{dt.month}/{dt.day}"
            if folder2 != dataset_name:
                object_key = f"{folder1}/{folder2}/{dataset_name}/{partition}/{file_name}".replace(' ', '_')
            else:
                object_key = f"{folder1}/{folder2}/{partition}/{file_name}".replace(' ', '_')

        bucket_name = env.replace('_','-') + "-" + bucket_suffix

        # check bucket CORS policy to allow upload from web application for current host_url
        update_policy = False
        try:
            cors_configuration = boto3_session.client('s3').get_bucket_cors(Bucket=bucket_name)
            logger.info(json.dumps(cors_configuration['CORSRules'][0]["AllowedOrigins"], indent=2))
            if session["host_url"] not in cors_configuration['CORSRules'][0]["AllowedOrigins"]:
                cors_configuration['CORSRules'][0]["AllowedOrigins"].append(session["host_url"])
                update_policy = True
        except ClientError as e:
            logger.warning(e)
            if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                cors_configuration = {
                    'CORSRules': [{
                            'AllowedHeaders': ["*"],
                            'AllowedMethods': ['GET', 'HEAD', 'PUT'],
                            'AllowedOrigins': [session["host_url"]],
                            'ExposeHeaders': []
                        }]
                    }
                update_policy = True
            else:
                # AllAccessDisabled error == bucket not found
                logging.error(e)
                return
        
        # update CORS policy for current host_url
        if update_policy:
            logger.info(f"updating CORS policy for {bucket_name}")
            logger.info(json.dumps(cors_configuration['CORSRules'][0]["AllowedOrigins"], indent=2))
            boto3_session.client('s3').put_bucket_cors(
                Bucket=bucket_name,
                CORSConfiguration={'CORSRules': cors_configuration['CORSRules']}
            )

        mime_type = request.args["file_type"]
        logger.info(f"generating presigned url for s3://{bucket_name}/{object_key} ({mime_type})")
        response = boto3_session.client("s3").generate_presigned_url('put_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key, 
                'ContentType': mime_type}, 
            ExpiresIn=60)

        logger.info(response)
    except ClientError as e:
        logger.error(e)
        traceback.print_exc()
        return None
    
    form_data.append({
        "presigned_url": response
    })
