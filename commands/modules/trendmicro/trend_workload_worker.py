__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import os
import boto3
from commands.modules import pause
import commands.modules.trendmicro.trend_api as trend_api
from boto3.dynamodb.conditions import Key, Attr
from tabulate import tabulate


class TrendWorkloadSecurityWorker(object):

    logger = logging.getLogger(__name__)

    def __init__(self, module):
        self.module = module
        self.args = module.args
        self.env = module.env

        self.metadata_table = self.module.get_dynamodb_resource().Table("metadata")

        self.s3_resource = module.get_boto3_session().resource('s3')
        self.ec2_client = module.get_boto3_session().client('ec2')


    def workload_create_group(self, metadata=None):
        GROUP_NAME = self.args.name.upper()
        GROUP_NAME_FULL = f"{self.env}_{GROUP_NAME}".upper()
        self.logger.info(f"Creating or updating group {GROUP_NAME_FULL}")

        # get existing group
        result = trend_api.call_api(self.env, trend_api.WORKLOAD_SECURITY, "GET", "computergroups", boto3_session=self.get_boto3_session())
        self.logger.info(json.dumps(result, indent=2, default=str))
        pause(self.args)

        root_group = None
        computer_group = None
        for group in result['computerGroups']:
            if self.env.upper() == group['name']:
                root_group = group
            elif GROUP_NAME_FULL == group['name']:
                computer_group = group
        
        self.logger.info("ROOT GROUP:")
        self.logger.info(json.dumps(root_group, indent=2, default=str))
        self.logger.info("COMPUTER GROUP:")
        self.logger.info(json.dumps(root_group, indent=2, default=str))
        pause(self.args)

        # make sure root environment group exists
        if root_group is None:
            params={
                "name": self.env.upper(),
                "description": f"{self.env.upper()} Environment Root Group",
                "parentGroupID": 0
            }
            root_group = trend_api.call_api(self.env, trend_api.WORKLOAD_SECURITY, "POST", "computergroups", params=params, boto3_session=self.get_boto3_session())
            self.logger.info("ROOT GROUP:")
            self.logger.info(json.dumps(root_group, indent=2, default=str))
            pause(self.args)

        # create group
        if computer_group is None:
            params={
                "name": GROUP_NAME_FULL,
                "description": self.args.trendmicro_description,
                "parentGroupID": root_group['ID']
            }
            computer_group = trend_api.call_api(self.env, trend_api.WORKLOAD_SECURITY, "POST", "computergroups", params=params, boto3_session=self.get_boto3_session())
            self.logger.info("COMPUTER GROUP:")
            self.logger.info(json.dumps(computer_group, indent=2, default=str))
            pause(self.args)
        
        group_id = computer_group["ID"]
        group_name = computer_group["name"].lower()
        metadata = self.get_workload_group_metadata(workload_group=group_name)[0]
        metadata["id"] = str(group_id)
        self.module.get_dynamodb_resource().Table('metadata').put_item(Item=metadata)


    def get_workload_group_metadata(self, workload_group=None):
        filters = Attr('profile').eq(self.env) & Attr('module').eq('trendmicro') & Attr('command').eq('workload_create_group')

        if workload_group:
            filters = filters & Attr('name').eq(workload_group.split('_')[-1])

        return self.module.get_dynamodb_resource().Table('metadata').scan(FilterExpression=filters)['Items']


    def get_workload_group_from_api(self, workload_group=None):
        groups = trend_api.call_api(self.env, trend_api.WORKLOAD_SECURITY, "GET", "computergroups", boto3_session=self.get_boto3_session())
        if workload_group:
            group_name_full = f"{self.env}_{workload_group.split('_')[-1]}".upper()
            for group in groups['computerGroups']:
                if group_name_full == group['name']:
                    return group
        else:
            return groups['computerGroups']


    def workload_generate_deployment_script(self, metadata=None):
        platform = self.args.trendmicro_platform
        workload_policy = self.args.trendmicro_workload_policy
        workload_group = self.args.trendmicro_workload_group
        if type(workload_group) is str and workload_group != "" and not workload_group.isdigit():
            # get group
            group_from_api = self.get_workload_group_from_api(workload_group)
            self.logger.info(json.dumps(group_from_api, indent=2, default=str))
            # group_metadata = self.get_workload_group_metadata(workload_group)
            # self.logger.info(json.dumps(group_metadata, indent=2, default=str))
            workload_group_id = group_from_api['ID']
        elif workload_group != "":
            workload_group_id = int(workload_group)
        else:
            workload_group_id = ""

        # generate deployment script
        params = {
            "platform": platform,
            "validateCertificateRequired": True,
            "validateDigitalSignatureRequired": False,
            "activationRequired": True,
            "policyID": workload_policy,
            "computerGroupID": workload_group_id
            # "relayGroupID": 0,
            # "dsmProxyID": 0,
            # "relayProxyID": 0,
        }               
 
        deployment_script = trend_api.call_api(self.env, trend_api.WORKLOAD_SECURITY, "POST", "agentdeploymentscripts", params=params, boto3_session=self.get_boto3_session())

        dir = "./scripts/trendmicro"
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_name = f"{dir}/{params['platform']}_agent_deployment_script_{workload_policy}_{workload_group}.sh"
        file = open(file_name, "w")
        n = file.write(deployment_script['scriptBody'])
        file.close()

        # upload to s3
        utils_bucket = f"{self.env}-utils".replace('_','-')
        object_key = f"scripts/trendmicro/{params['platform']}_agent_deployment_script_{workload_policy}_{workload_group}.sh"
        res = self.s3_resource.meta.client.upload_file(file_name, utils_bucket, object_key)
        self.logger.info(json.dumps(res, indent=2, default=str))


    def create_trend_workload_agent_security_group(self, env_config):
        try:
            # check if group already exists
            group_name = f"{self.env}_trend_workload_agent_sg"
            resp = self.ec2_client.describe_security_groups(
                Filters=[{'Name': 'group-name','Values': [group_name]}]
            )
            if len(resp['SecurityGroups']) > 0:
                self.logger.info(f"Security Group {group_name} already exists")
                return resp['SecurityGroups'][0]['GroupId']

            # create new security group
            tags = [{
                'ResourceType': 'security-group',
                'Tags': [
                    {'Key': 'Name','Value': group_name}, 
                    {'Key': 'profile','Value': self.env}, 
                    {'Key': 'env','Value': self.env}, 
                    {'Key': 'caller_arn','Value': self.args.user}
                ]}
            ]

            response = self.ec2_client.create_security_group(
                Description='Trend Micro Workload Security Agent',
                GroupName=group_name,
                VpcId=env_config['vpc'],
                TagSpecifications=tags,
                DryRun=False
            )
            group_id = response['GroupId']

            # revoke all outbound traffic
            response = self.ec2_client.revoke_security_group_egress(
                GroupId=group_id,
                IpPermissions=[{
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    "Ipv6Ranges": [],
                    "PrefixListIds": [],
                    "UserIdGroupPairs": []
                }],
                DryRun=False
            )            

            # authorize outbound ports
            response = self.ec2_client.authorize_security_group_egress(
                GroupId=group_id,
                IpPermissions=[
                    {
                        "FromPort": 80,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                                "Description": "Smart Protection Network Serverport"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "ToPort": 80,
                        "UserIdGroupPairs": []
                    },
                    {
                        "FromPort": 443,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                                "Description": "HTTPS"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "ToPort": 443,
                        "UserIdGroupPairs": []
                    },
                    {
                        "FromPort": 53,
                        "IpProtocol": "udp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                                "Description": "DNS server port"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "ToPort": 53,
                        "UserIdGroupPairs": []
                    },
                    {
                        "FromPort": 123,
                        "IpProtocol": "udp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                                "Description": "NTP over UDP"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "ToPort": 123,
                        "UserIdGroupPairs": []
                    }
                ],
                DryRun=False
            )

        except Exception as e:
            self.logger.warning(e)

        return group_id


    def workload_group_sync(self, metadata=None):
        not_in_metadata, not_in_trend = [], []

        groups_from_trend = self.get_workload_group_from_api()
        if self.args.verbose:
            self.logger.info(json.dumps(groups_from_trend, indent=2, default=str))
        pause(self.args)

        groups_metadata = self.get_workload_group_metadata()
        if self.args.verbose:
            self.logger.info(json.dumps(groups_metadata, indent=2, default=str))
        pause(self.args)

        # not in trend
        for trend_group in groups_from_trend:
            trend_group_name = trend_group['name']
            if self.env.upper() not in trend_group_name:
                continue
            match = False
            for group_metadata in groups_metadata:
                group_metadata_name = f"{self.env}_{group_metadata['name']}".upper()
                if trend_group_name == self.env.upper() or trend_group_name == group_metadata_name:
                    match = True
                    break
            if not match:
                not_in_metadata.append(trend_group)
        if self.args.verbose:
            self.logger.info("Not in metadata")
            self.logger.info(json.dumps(not_in_metadata, indent=2, default=str))
        pause(self.args)

        # not in metadata
        for group_metadata in groups_metadata:
            group_metadata_name = f"{self.env}_{group_metadata['name']}".upper()
            match = False
            for trend_group in groups_from_trend:
                trend_group_name = trend_group['name']
                if group_metadata_name == trend_group_name:
                    match = True
                    break
            if not match:
                not_in_trend.append(group_metadata)
        if self.args.verbose:
            self.logger.info("Not in trend")
            self.logger.info(json.dumps(not_in_trend, indent=2, default=str))
        pause(self.args)

        grid = []
        for group in not_in_trend:
            grid.append([group['name'], group['trendmicro_description'], group['trendmicro_policy']])
        headers=["name","trendmicro_description","trendmicro_policy"]
        self.logger.info("Not in trend")
        print(f"{tabulate(sorted(grid), headers)}\n")

        grid = []
        for group in not_in_metadata:
            grid.append([group['name'], group['description'], group['ID']])
        headers=["name","description","ID"]
        self.logger.info("Not in metadata")
        print(f"{tabulate(sorted(grid), headers)}\n")


    def workload_list_policies(self, metadata=None):
        resp = trend_api.call_api(self.env, trend_api.WORKLOAD_SECURITY, "GET", "policies", boto3_session=self.get_boto3_session()) 
        policies = []       
        for item in resp["policies"]:
            policy = {
                "parentID": item["parentID"] if "parentID" in item else "",
                "ID": item["ID"],
                "name": item["name"],
                "description": item["description"]
            }
            policies.append(policy)
        self.logger.info(json.dumps(policies, indent=2, default=str))
        return policies
