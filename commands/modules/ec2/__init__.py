__author__ = "Abe Garcia"
__license__ = "MIT"
__email__ = "agarciaortiz"

import json
import os
import pprint
import boto3
from tabulate import tabulate
import base64
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.modules import exec_module, pause
from commands.modules.trendmicro.trend_workload_worker import TrendWorkloadSecurityWorker

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.env = super().get_env()
        self.ec2_client = super().get_ec2_client()
        self.ssm_client = super().get_ssm_client()


    def create(self, metadata=None):
        '''
        kc ec2 create --mode console --refresh_status True --name "ec2_001" --ec2_instance_type "t2.micro" --ec2_ami_id "ami-0022f774911c1d690" --ec2_key_name "theia-server" --ec2_vpc_id "vpc-05b3ddb6314da834c" --ec2_availability_zone "us-east-1a" --ec2_subnet_id "subnet-032fe17eea396ca89" --ec2_vpc_security_group_ids "sg-0e977e41bea221d0b" --ec2_volume_size "8" --ec2_enable_trend "false" --env "kc_tm_1"        
        '''
        AwsInfra(self.args).delete_aws_infra()

        params = super().get_ec2_instance_params()
        # self.logger.info(json.dumps(params, indent=2))
        if "ec2_ami_id" in metadata and metadata["ec2_ami_id"] != "":
            platform = self.get_ami_platform(metadata["ec2_ami_id"])
        else:
            platform = "linux"

        # trend micro
        if self.args.ec2_enable_trend == "true":
            try:
                # add agent to user data
                params = self.add_trend_ec2_agent_via_user_data(params, platform)

                # add trend security group with required outbound ports
                self.logger.info("ADDING TREND SEC GROUP")
                sec_group_id = TrendWorkloadSecurityWorker(self).create_trend_workload_agent_security_group(super().get_env_config())
                if params['vpc_security_group_ids'] != "":
                    if sec_group_id not in params['vpc_security_group_ids']:
                        params['vpc_security_group_ids'].append(sec_group_id)
                else:
                    params['vpc_security_group_ids'] = [sec_group_id]

                # check if instance is already in AWS or just in RC metadata
                # TODO: see if we can avoid returning terminated instances
                resp = self.ec2_client.describe_instances(
                    Filters=[{'Name': 'tag:Name', 'Values': [f'{self.env}_{self.args.name}']}])
                self.logger.info("CHECKING INSTANCE IN AWS")
                if len(resp['Reservations']) > 0 and len(resp['Reservations'][0]['Instances']) > 0:
                    self.logger.info("INSTANCE EXISTS IN AWS, USING SSM")
                    # Use SSM to install and activate Trend Workload Agent
                    ec2_instance_id = resp['Reservations'][0]['Instances'][0]['InstanceId']
                    self.logger.info(f"Instance ID: {ec2_instance_id}")
                    
                    workload_group = self.args.ec2_trend_workload_group
                    workload_policy = self.get_workload_policy(workload_group)

                    resp = self.enable_trend_ssm_ec2_instance(ec2_instance_id, platform, policy=workload_policy, group=workload_group, sec_group_id=sec_group_id)
            except Exception as e:
                self.logger.warning("Failed to enable Trend Micro Workload Security. Make sure this instance can be managed via SSM.")
                self.logger.warning(e)

        self.add_aws_resource("aws_instance", self.args.name, params, role_name=params['role_name'])
    

    def get_workload_policy(self, group_id):
        resp = self.get_dynamodb_resource().Table('metadata').scan(FilterExpression=Attr('profile').eq(self.env) & Attr('module').eq('trendmicro') & Attr('command').eq('workload_create_group') & Attr('id').eq(group_id))['Items']
        self.logger.info(f"GETTING TREND POLICY FOR {group_id}")
        self.logger.info(json.dumps(resp, indent=2))
        if len(resp) > 0:
            group = resp[0]
            if "trendmicro_policy" in group['params']:
                return int(group['params']['trendmicro_policy'])
            else:
                # Default to Base Policy -> Linux Server
                return 2


    def add_trend_ec2_agent_via_user_data(self, params={}, platform="linux"):
        workload_group = self.args.ec2_trend_workload_group
        workload_policy = self.get_workload_policy(workload_group)

        # make sure trend workload agent script exists
        dir = f"{os.getcwd()}/scripts/trendmicro"
        if not os.path.exists(dir):
            os.makedirs(dir)
        script_file = f"{dir}/{platform}_agent_deployment_script.sh"
        if not os.path.exists(script_file):
            # generate and download script
            setattr(self.args, 'trendmicro_platform', platform)
            setattr(self.args, 'trendmicro_workload_policy', workload_policy)
            setattr(self.args, 'trendmicro_workload_group', workload_group)
            exec_module(self.args, "trendmicro", "workload_generate_deployment_script")

        # set EC2 user data parameter for Terraform apply for new EC2 instance
        utils_bucket = f"{self.env}-utils".replace('_','-')
        object_key = f"scripts/trendmicro/{platform}_agent_deployment_script_{workload_policy}_{workload_group}.sh"
        if 'user_data' not in params or len(params['user_data']) == 0:
            params['user_data'] = "#!/bin/bash"
        params['user_data'] += f"""
        sudo su -
        echo "copying script to instance"
        aws s3 cp s3://{utils_bucket}/{object_key} .
        . /{platform}_agent_deployment_script_{workload_policy}_{workload_group}.sh
        """
        return params


    def list_unmanaged(self, metadata=None):
        # get all instances
        resp = self.ec2_client.describe_instances()
        reservations = resp["Reservations"]
        if 'NextToken' in resp:
            while resp['NextToken'] != "":
                resp = self.ec2_client.describe_instances(NextToken='string')
                reservations += resp['Reservations']
        
        grid = []
        result = []
        for r in reservations:
            for i in r['Instances']:
                name, env, tm_workload_enabled, trend_workload_group, trend_workload_policy = "", "", False, "", ""
                managed = False
                for tag in i['Tags']:
                    if tag['Key'] == 'author' and tag['Value'] in ['rapid-cloud', 'rapidcloud']:
                        managed = True
                        break
                    elif tag['Key'] == 'Name':
                        name = tag['Value']
                    elif tag['Key'] == 'trend_workload_group':
                        trend_workload_group = tag['Value']
                        tm_workload_enabled = True
                    elif tag['Key'] == 'trend_workload_policy':
                        trend_workload_policy = tag['Value']
                        tm_workload_enabled = True
                if not managed:
                    for sg in i['SecurityGroups']:
                        if sg['GroupName'] == 'trend-micro-workload-agent':
                            tm_workload_enabled = True
                            break

                    item = {
                        "ec2_instance_id": i['InstanceId'],
                        "ec2_instance_type": i['InstanceType'],
                        "ec2_instance_name": name,
                        "ec2_launch_time": i['LaunchTime'],
                        "ec2_enable_trend": tm_workload_enabled,
                        "trend_workload_group": trend_workload_group,
                        "trend_workload_policy": trend_workload_policy
                    }
                    result.append(item)
                    row = []
                    for v in item.values():
                        row.append(v)
                    grid.append(row)

        headers=["env","ec2_instance_id","ec2_instance_type","ec2_instance_name","ec2_launch_time","ec2_enable_trend","trend_workload_group"]
        print(f"{tabulate(sorted(grid), headers)}\n")

        return result


    def list_launch_templates(self, metadata=None):
        resp = self.ec2_client.describe_launch_templates()
        templates = resp["LaunchTemplates"]
        if 'NextToken' in resp:
            while resp['NextToken'] != "":
                resp = self.ec2_client.describe_launch_templates()
                templates += resp['LaunchTemplates']
        
        grid, result = [], []
        for lt in templates:
            env, trend_workload_group, trend_workload_policy = "", "", ""
            for tag in lt.get('Tags',[]):
                if tag['Key'] == 'profile':
                    env = tag['Value']
                elif tag['Key'] == 'trend_workload_group':
                    trend_workload_group = tag['Value']
                elif tag['Key'] == 'trend_workload_policy':
                    trend_workload_policy = tag['Value']

            item = {
                "env": env,
                "ec2_launch_template_id": lt['LaunchTemplateId'],
                "ec2_launch_template_name": lt['LaunchTemplateName'],
                "default_version": lt['DefaultVersionNumber'],
                "latest_version": lt['LatestVersionNumber'],
                "create_time": lt['CreateTime'],
                "ec2_enable_trend": True if trend_workload_group else False,
                "ec2_trend_workload_group": trend_workload_group,
                "ec2_trend_workload_policy": trend_workload_policy
            }

            result.append(item)
            row = []
            for v in item.values():
                row.append(v)
            grid.append(row)

        headers=["env","ec2_launch_template_name","ec2_launch_template_id","default_version","latest_version","create_time","ec2_trend_workload_group","ec2_trend_workload_policy"]
        print(f"{tabulate(sorted(grid), headers)}\n")

        return result


    def enable_trend(self, metadata=None):
        # TODO need to allow windows in the future
        platform = "linux"

        group = self.args.ec2_trend_workload_group
        policy = self.get_workload_policy(group)

        target = self.args.ec2_target
        self.logger.info(f"Target            : {target}")
        if target == "ec2":
            self.logger.info(f"Instance ID       : {self.args.ec2_instance_id}")
        else:
            self.logger.info(f"Launch Template   : {self.args.ec2_launch_template_id}")

        self.logger.info(f"Enable            : {self.args.ec2_enable_trend}")
        self.logger.info(f"Policy            : {policy}")
        self.logger.info(f"Group             : {group}")
        
        # create security group for trend agent outbound communications
        if self.args.ec2_enable_trend in ["yes", "true"]:
            # add trend security group with required outbound ports
            sec_group_id = TrendWorkloadSecurityWorker(self).create_trend_workload_agent_security_group(super().get_env_config())
            self.logger.info(f"sec_group_id: {sec_group_id}")

            if target == "ec2":
                resp = self.enable_trend_ssm_ec2_instance(self.args.ec2_instance_id, platform, policy, group, sec_group_id)
            else:
                resp = self.enable_trend_launch_template(self.args.ec2_launch_template_id, platform, policy, group, sec_group_id)
            return resp


    def enable_trend_ssm_ec2_instance(self, ec2_instance_id, platform, policy, group, sec_group_id=None):
        # download and install agent on the instance
        utils_bucket = f"{self.env}-utils".replace('_','-')
        script_name = f"{platform}_agent_deployment_script_{policy}_{group}.sh"
        object_key = f"scripts/trendmicro/{script_name}"
        shell = "AWS-RunShellScript" if platform == "linux" else "AWS-RunPowerShellScript"
        commands = {'commands': [
            "sudo su -",
            f"cd /home/ec2-user",
            f"aws s3 cp s3://{utils_bucket}/{object_key} . > trend_download.out",
            f". /home/ec2-user/{script_name} > trend_install.out",
            f"aws ec2 create-tags --resources {self.args.ec2_instance_id} --tags Key=trend_workload_group,Value={group}",
            f"aws ec2 create-tags --resources {self.args.ec2_instance_id} --tags Key=trend_workload_policy,Value={policy}"
        ]}
        self.logger.info(json.dumps(commands, indent=2))
        resp = self.ssm_client.send_command(
            DocumentName=shell,
            Parameters=commands,
            InstanceIds=[ec2_instance_id]
        )
        self.logger.info(json.dumps(resp, indent=2, default=str))
        return resp


    def enable_trend_launch_template(self, ec2_launch_template_id, platform, policy, group,sec_group_id):
        latest = self.ec2_client.describe_launch_templates(
            LaunchTemplateIds=[ec2_launch_template_id])['LaunchTemplates']
        if len(latest) > 0:
            self.logger.info("BEFORE:")
            self.logger.info(json.dumps(latest, indent=2, default=str))
            user_data = self.add_trend_ec2_agent_via_user_data()['user_data']
            self.logger.info(user_data)
            pause(self.args)

            # get security groups
            resp = self.ec2_client.describe_launch_template_versions(
                LaunchTemplateId=ec2_launch_template_id,
                Versions=["$Default"]
            )
            # self.logger.info(json.dumps(resp, indent=2, default=str))
            sec_groups = resp['LaunchTemplateVersions'][0]['LaunchTemplateData']['SecurityGroupIds']
            self.logger.info(json.dumps(sec_groups, indent=2, default=str))
            if sec_group_id not in sec_groups:
                sec_groups.append(sec_group_id)

            # create new version
            resp = self.ec2_client.create_launch_template_version(
                LaunchTemplateData={
                    'UserData': base64.b64encode(user_data.encode('ascii')).decode('ascii'),
                    'SecurityGroupIds': sec_groups
                },
                LaunchTemplateId=ec2_launch_template_id,
                SourceVersion=str(latest[0]['LatestVersionNumber']),
                VersionDescription='Trend Micro Workload Security Enabled'
            )
            self.logger.info(json.dumps(resp, indent=2, default=str))
            pause(self.args)

            latest = self.ec2_client.describe_launch_templates(
                LaunchTemplateIds=[ec2_launch_template_id])['LaunchTemplates']
            self.logger.info("AFTER create_launch_template_version:")
            self.logger.info(json.dumps(latest, indent=2, default=str))
            pause(self.args)

            # set default version as latest version
            resp = self.ec2_client.modify_launch_template(
                ClientToken=self.args.cmd_id,
                LaunchTemplateId=ec2_launch_template_id,
                DefaultVersion=str(latest[0]['LatestVersionNumber'])
            )            
            self.logger.info(json.dumps(resp, indent=2, default=str))

            latest = self.ec2_client.describe_launch_templates(
                LaunchTemplateIds=[ec2_launch_template_id])['LaunchTemplates']
            self.logger.info("AFTER modify_launch_template:")
            self.logger.info(json.dumps(latest, indent=2, default=str))
            pause(self.args)

            # add tags
            tags = latest[0].get("Tags", [])
            tags.append({'Key': 'profile','Value': self.env})
            tags.append({'Key': 'env','Value': self.env})
            tags.append({'Key': 'Name','Value': latest[0]['LaunchTemplateName']})
            tags.append({'Key': 'caller_arn','Value': self.args.user})
            tags.append({'Key': 'trend_platform','Value': platform})
            tags.append({'Key': 'trend_workload_policy','Value': str(policy)})
            tags.append({'Key': 'trend_workload_group','Value': str(group)})
            resp = self.ec2_client.create_tags(
                Resources=[ec2_launch_template_id],
                Tags=tags
            )
            self.logger.info(json.dumps(resp, indent=2, default=str))

            return latest

        else:
            self.logger.error(f"Launch Template {ec2_launch_template_id} is not found")
            return None


    def get_ami_platform(self, image_id):
        resp = self.ec2_client.describe_images(Filters=[{
            'Name': 'image-id',
            'Values': [image_id]
        }])

        if len(resp['Images']) > 0:
            platform_details = resp['Images'][0]["PlatformDetails"]
            if platform_details == "Linux/UNIX":
                return "linux"
            elif platform_details == "Windows":
                return "windows"
