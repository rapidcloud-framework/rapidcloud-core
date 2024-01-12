__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import requests

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-5s %(name)-39s:  %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV = os.environ.get('PROFILE')
FSS_URL = "https://filestorage.us-1.cloudone.trendmicro.com/api"

session = boto3.Session()
dynamodb_resource = session.resource('dynamodb')
secret_client = session.client('secretsmanager')
sns_client = session.client('sns')
lambda_client = session.client('lambda')


def call_api(method, action, params={}):
    api_key = secret_client.get_secret_value(SecretId="trendmicro/api_key")['SecretString'] 

    # Authentication header
    headers = { 
        "Authorization" : f"ApiKey {api_key}",
        "Api-Version": "v1"
    }

    url = f"{FSS_URL}/{action}"
    req = {
        "provider": "aws"
    }
    req.update(params)

    if method == "POST":
        logger.debug(json.dumps(req, indent=2, default=str))
        result = requests.post(url, data = json.dumps(req), headers=headers).json()
    elif method == "GET":
        url += "?"
        for param,value in req.items():
            url += f"{param}={value}&"
        logger.debug(url)
        result = requests.get(url, headers=headers).json()

    return result


def deploy_filestorage_stack(stack_name, stack):
    stack_metadata_list = get_stack_metadata(stack)
    logger.info(json.dumps(stack_metadata_list, indent=2, default=str))
    arns = {
        "scanner": "ScannerStackManagementRoleARN",
        "storage": "StorageStackManagementRoleARN"
    }
    for stack_metadata in stack_metadata_list:
        logger.info(f"processing {stack_metadata['fqn']} ...")
        for stack_type, role_arn_key in arns.items():
            
            if 'stackID' in stack_metadata['params']:
                logger.info(f"{stack_metadata['params']['trendmicro_stack_type']} stack: {stack_name}: {stack_metadata['params']['stackID']}")
                break
                
            if stack_type == stack_metadata['params']['trendmicro_stack_type'] and role_arn_key in stack['parsed']['outputs']: 
                logger.info(f"{stack_metadata['params']['trendmicro_stack_type']} stack: {stack_name}: None")

                role_arn_value = stack['parsed']['outputs'][role_arn_key]
                logger.info(f"saving {role_arn_key}: {role_arn_value} for {stack_name}")

                # update TM stack via API
                logger.info(f"updating stack in trend micro")
                result = create_stack_in_tm(stack_metadata, role_arn_value)
                # logger.info(json.dumps(result, indent=2, default=str))

                # update RapidCloud stack metadata
                stack_metadata['cf_stack'] = stack['parsed']
                stack_metadata['cf_stack']['stack_name'] = stack_name
                stack_metadata['params'][role_arn_key] = role_arn_value
                stack_metadata['params']['stackID'] = result['stackID']
                if stack_metadata['params']['trendmicro_stack_type'] == "scanner":
                    stack_metadata['params']['trendmicro_bucket'] == ""
                logger.info(f"updating stack metadata")
                result = dynamodb_resource.Table("metadata").put_item(Item=stack_metadata)
                # logger.info(json.dumps(stack_metadata, indent=2, default=str))

                # Subscribe custom post-scan Lambda to the SNS topic
                subscribe_to_scan_sns_topic(stack)



def get_stack_metadata(stack):
    stacks_metadata = []
    if 'scanner' in stack['parsed']['tags']:
        fqn = stack['parsed']['tags']['scanner']
        logger.info(f"getting stack metadata: {ENV} -> {fqn}")
        stacks_metadata.append(dynamodb_resource.Table('metadata').query(
            KeyConditionExpression=Key('profile').eq(ENV) & Key('fqn').eq(fqn)
        )['Items'][0])

    if 'storage' in stack['parsed']['tags']:
        fqn = stack['parsed']['tags']['storage']
        logger.info(f"getting stack metadata: {ENV} -> {fqn}")
        stacks_metadata.append(dynamodb_resource.Table('metadata').query(
            KeyConditionExpression=Key('profile').eq(ENV) & Key('fqn').eq(fqn)
        )['Items'][0])

    return stacks_metadata


def create_stack_in_tm(stack_metadata, role_arn_value):
    stacks = call_api("GET", "stacks")
    stack_type = stack_metadata['params']['trendmicro_stack_type']
    params = {
        "type": stack_type,
        "details": {
            "managementRole": role_arn_value
        }
    }
    if stack_type == "storage":
        # find scanner stack
        for stack in stacks["stacks"]:
            if stack['type'] == 'scanner':
                params['scannerStack'] = stack['stackID']
                logger.info(f"scannerStack: {stack['stackID']}")

    result = call_api("POST", "stacks", params)
    logger.info(json.dumps(result, indent=2, default=str))
    return result 


def subscribe_to_scan_sns_topic(stack):
    if 'ScanResultTopicARN' in stack['parsed']['outputs']:
        # get Lambda function ARN
        function_name = f"{ENV}_trendmicro_post_scan"
        response = lambda_client.get_function(
            FunctionName=function_name
        )
        logger.info(json.dumps(response, indent=2, default=str))
        if 'Configuration' in response:
            lambda_arn = response['Configuration']['FunctionArn']
            topic_arn = stack['parsed']['outputs']['ScanResultTopicARN']       
            response = sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='lambda',
                Endpoint=lambda_arn
            )
            logger.info(json.dumps(response, indent=2, default=str))

            # allow SNS to invoke lambda
            response = lambda_client.add_permission(
                Action='lambda:InvokeFunction',
                FunctionName=function_name,
                Principal='sns.amazonaws.com',
                SourceArn=topic_arn,
                StatementId="AllowSubscriptionToSNS"
            )


def create_workload_computer(instance):
    logger.info("creating workload computer ...")
    logger.info(json.dumps(instance, indent=2, default=str))
    instance_example = {
        "Reservations": [
            {
                "Groups": [],
                "Instances": [
                    {
                        "AmiLaunchIndex": 0,
                        "ImageId": "ami-05fa00d4c63e32376",
                        "InstanceId": "i-065b2d707e06fe16b",
                        "InstanceType": "t2.micro",
                        "KeyName": "theia-server",
                        "LaunchTime": "2022-09-06T18:28:56+00:00",
                        "Monitoring": {
                            "State": "disabled"
                        },
                        "Placement": {
                            "AvailabilityZone": "us-east-1a",
                            "GroupName": "",
                            "Tenancy": "default"
                        },
                        "PrivateDnsName": "ip-172-27-29-107.ec2.internal",
                        "PrivateIpAddress": "172.27.29.107",
                        "ProductCodes": [],
                        "PublicDnsName": "ec2-34-205-81-149.compute-1.amazonaws.com",
                        "PublicIpAddress": "34.205.81.149",
                        "State": {
                            "Code": 16,
                            "Name": "running"
                        },
                        "StateTransitionReason": "",
                        "SubnetId": "subnet-032fe17eea396ca89",
                        "VpcId": "vpc-05b3ddb6314da834c",
                        "Architecture": "x86_64",
                        "BlockDeviceMappings": [
                            {
                                "DeviceName": "/dev/xvda",
                                "Ebs": {
                                    "AttachTime": "2022-09-06T17:59:20+00:00",
                                    "DeleteOnTermination": True,
                                    "Status": "attached",
                                    "VolumeId": "vol-07385d0fd89f8e5f2"
                                }
                            }
                        ],
                        "ClientToken": "",
                        "EbsOptimized": False,
                        "EnaSupport": True,
                        "Hypervisor": "xen",
                        "IamInstanceProfile": {
                            "Arn": "arn:aws:iam::247654790127:instance-profile/theia-server-role",
                            "Id": "AIPATTKLAGPXTU3ASUOQA"
                        },
                        "NetworkInterfaces": [
                            {
                                "Association": {
                                    "IpOwnerId": "amazon",
                                    "PublicDnsName": "ec2-34-205-81-149.compute-1.amazonaws.com",
                                    "PublicIp": "34.205.81.149"
                                },
                                "Attachment": {
                                    "AttachTime": "2022-09-06T17:59:19+00:00",
                                    "AttachmentId": "eni-attach-028c05080c0dae425",
                                    "DeleteOnTermination": True,
                                    "DeviceIndex": 0,
                                    "Status": "attached",
                                    "NetworkCardIndex": 0
                                },
                                "Description": "",
                                "Groups": [
                                    {
                                        "GroupName": "theia-server-sg",
                                        "GroupId": "sg-0a171f7f1e679734c"
                                    },
                                    {
                                        "GroupName": "trend-micro-workload-agent",
                                        "GroupId": "sg-049ef747f0cf604db"
                                    }
                                ],
                                "Ipv6Addresses": [],
                                "MacAddress": "02:b0:1f:a7:e1:c7",
                                "NetworkInterfaceId": "eni-055fadf047aa7e253",
                                "OwnerId": "247654790127",
                                "PrivateDnsName": "ip-172-27-29-107.ec2.internal",
                                "PrivateIpAddress": "172.27.29.107",
                                "PrivateIpAddresses": [
                                    {
                                        "Association": {
                                            "IpOwnerId": "amazon",
                                            "PublicDnsName": "ec2-34-205-81-149.compute-1.amazonaws.com",
                                            "PublicIp": "34.205.81.149"
                                        },
                                        "Primary": True,
                                        "PrivateDnsName": "ip-172-27-29-107.ec2.internal",
                                        "PrivateIpAddress": "172.27.29.107"
                                    }
                                ],
                                "SourceDestCheck": True,
                                "Status": "in-use",
                                "SubnetId": "subnet-032fe17eea396ca89",
                                "VpcId": "vpc-05b3ddb6314da834c",
                                "InterfaceType": "interface"
                            }
                        ],
                        "RootDeviceName": "/dev/xvda",
                        "RootDeviceType": "ebs",
                        "SecurityGroups": [
                            {
                                "GroupName": "theia-server-sg",
                                "GroupId": "sg-0a171f7f1e679734c"
                            },
                            {
                                "GroupName": "trend-micro-workload-agent",
                                "GroupId": "sg-049ef747f0cf604db"
                            }
                        ],
                        "SourceDestCheck": True,
                        "Tags": [
                            {
                                "Key": "Name",
                                "Value": "trendmicro-test-igor-1"
                            }
                        ],
                        "VirtualizationType": "hvm",
                        "CpuOptions": {
                            "CoreCount": 1,
                            "ThreadsPerCore": 1
                        },
                        "CapacityReservationSpecification": {
                            "CapacityReservationPreference": "open"
                        },
                        "HibernationOptions": {
                            "Configured": False
                        },
                        "MetadataOptions": {
                            "State": "applied",
                            "HttpTokens": "optional",
                            "HttpPutResponseHopLimit": 1,
                            "HttpEndpoint": "enabled"
                        },
                        "EnclaveOptions": {
                            "Enabled": False
                        }
                    }
                ],
                "OwnerId": "247654790127",
                "ReservationId": "r-054ec3f5672130da0"
            }
        ]
    }
