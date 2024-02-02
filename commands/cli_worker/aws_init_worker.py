#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
import json
import logging
import os
from datetime import datetime
from os.path import exists

import boto3
from commands import boto3_utils, general_utils
from commands.cli_worker.init_worker import InitWorker
from commands.cli_worker.license_worker import LicenseWorker
from commands.colors import colors
from commands.kc_metadata_manager.activation import AwsActivator
from commands.kc_metadata_manager.aws_infra import AwsInfra
from commands.kc_metadata_manager.aws_profile import Profile
from commands.kc_metadata_manager.property import Property


class AwsInitWorker(InitWorker):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        # self.logger.info("AwsInitWorker __init__")
        super().__init__(args)
        self.env = super().get_env()
        # self.logger.info(f"AwsInitWorker {self.env}")
        if not hasattr(self.args, 'x_acct_role_arn'):
            try:
                saas_params = {
                    "action": "get_tenant",
                    "email": self.args.current_session_email
                }
                tenant = LicenseWorker(self.args).contact_lic_server("saas", params=saas_params)
                x_acct_roles = tenant.get('x-acct-roles', None)

                if x_acct_roles is not None:
                    self.logger.info(f"AwsInitWorker found x_acct_roles in tenant for the following envs: {','.join(x_acct_roles.keys())}")
                    self.args.x_acct_role_arn = x_acct_roles[self.env]['role']
                    self.args.region = x_acct_roles[self.env]['region']
                self.logger.info(f"AwsInitWorker set x_acct_role_arn to {self.args.x_acct_role_arn}")
            except Exception as e:
                self.args.x_acct_role_arn = None

        try:
            self.logger.info("-----------------------------------")
            self.logger.info(f"AwsInitWorker email {self.args.current_session_email}")
            self.logger.info(f"AwsInitWorker profile {self.args.profile}")
            self.logger.info(f"AwsInitWorker x_acct_role_arn {self.args.x_acct_role_arn}")
            self.logger.info("-----------------------------------")
        except Exception as e:
            pass


    def get_dynamodb_client(self, args):
        # self.logger.info("AwsInitWorker get dynamodb client")
        if args.x_acct_role_arn is not None and args.x_acct_role_arn != "":
            # self.logger.info(f"AwsInitWorker get_dynamodb_client setting boto session to x_acct_role_arn: {args.x_acct_role_arn}")
            session = boto3_utils.get_boto_session(x_acct_role_arn=args.x_acct_role_arn)
        else:
            # self.logger.info(f"AwsInitWorker get_dynamodb_client setting boto_session to aws_profile: {args.aws_profile}, args.region: {args.region}")
            session = boto3_utils.get_boto_session(region=args.region, aws_profile=args.aws_profile)
        return session.client('dynamodb')

    def get_dynamodb_resource(self, args):
        # self.logger.info("AwsInitWorker get dynamodb resource")
        if args.x_acct_role_arn is not None and args.x_acct_role_arn != "":
            # self.logger.info(f"AwsInitWorker get_dynamodb_resource setting boto session to x_acct_role_arn: {args.x_acct_role_arn}")
            session = boto3_utils.get_boto_session(x_acct_role_arn=args.x_acct_role_arn)
        else:
            # self.logger.info(f"AwsInitWorker get_dynamodb_resource setting boto_session to aws_profile: {args.aws_profile}, args.region: {args.region}")
            session = boto3_utils.get_boto_session(region=args.region, aws_profile=args.aws_profile)
        return session.resource('dynamodb')

    def grant_tenant_x_acct_sts(self):
        '''
        when a customer creates a new cross account role,we need to grant
        the tenant instance sts asssume role access to the cross account
        this function will call the saas action in licensing.py and
        trigger the "grant_tenant_sts_access" action
        on the saas/licensing lambda, this action will add an iam policy
        named "sts-<x_acct_role_name>" and attach it to the tenant instance
        iam role
        '''
        sts_client = boto3.client('sts')
        src_caller_identity = sts_client.get_caller_identity()
        src_acct_id = src_caller_identity["Account"]
        src_role_arn = src_caller_identity["Arn"]
        external_id=f"{src_acct_id}-{str(src_acct_id)[::-1]}"
        try:
            cust_acct = sts_client.assume_role(
                RoleArn = self.args.x_acct_role_arn,
                RoleSessionName="rapidcloud-x-acct-role",
                ExternalId=external_id
            )
            self.logger.info(f"tested and assumed role to {self.args.x_acct_role_arn}")
            return True
        except Exception as e:
            self.logger.info(f"assume role to {self.args.x_acct_role_arn} failed, will trigger saas/grant_tenant_sts_access")

            saas_params = {
                "action": "grant_tenant_sts_access",
                "x_acct_role_arn": self.args.x_acct_role_arn,
                "tenant_instance_role_arn": src_role_arn,
                "email": self.args.current_session_email
            }

            self.logger.info(f"grant_tenant_x_acct_sts params: {saas_params}")
            created = LicenseWorker(self.args).contact_lic_server("saas", params=saas_params)

            self.logger.info(f"created grant_tenant_x_acct_sts: {created}")
            return created

    def save_tenant_x_acct_role_and_region(self, env):
        '''
        to preserve state beteen tenant instance
        we register the cross account role/region in the rapidcloud_tenant dynamodb table
        we use x_acct_role_arn, x_acct_role_env, x_acct_role_region to ensure its not messing
        with other session vars
        '''
        try:
            saas_params = {
                "action": "save_tenant_x_acct_role_and_region",
                "x_acct_role_arn": self.args.x_acct_role_arn,
                "x_acct_role_env": env,
                "x_acct_role_region": self.args.region,
                "email": self.args.current_session_email
            }

            self.logger.info(f"saving x_acct_role/region for env: {saas_params}")
            created = LicenseWorker(self.args).contact_lic_server("saas", params=saas_params)

            self.logger.info(f"saved x_acct_role/region for env: {created}")
            return created
        except Exception as e:
            self.logger.info("saving x_acct_role/region failed")
            return False

    def create_env(self):
        # make sure we set to assume role policy if this is a first run
        if self.args.x_acct_role_arn is not None and self.args.x_acct_role_arn != "":
            self.grant_tenant_x_acct_sts()

        if self.args.command == 'create-env':
            delattr(self.args, 'env') # in case `env` was passed in by mistake

        print("\nYou're creating or updating a RapidCloud environment for AWS\n")

        cloud_config = general_utils.load_json_file('config/aws_profile.json')
        env_config = general_utils.load_json_file(f"./config/environments/{self.env}_config.json")

        prompts = {
            # [name, description, prompt, required, force naming]
            'client': [
                'client','Company Name Abbreviation', 'Enter your company name abbreviation (letters and numbers only)', env_config.get('client',''), True, True],
            'workload': [
                'workload','Workload', 'Enter your workload name (letters and numbers only)', env_config.get('workload',''), True, True],
            'env_suffix': [
                'env_suffix','Environment', 'Enter environment (e.g dev|qa|prod)', env_config.get('env_suffix',''), True, True],
            'shared': [
                'shared','Shared', 'Is this environment shared with other engineers? (yes|no)', env_config.get('shared',''), True, True],
            'aws_profile': [
                'aws_profile','AWS Profile', 'Enter AWS_PROFILE to connect to your AWS Account', env_config.get('aws_profile',''), False, False],
            'x_acct_role_arn': [
                'x_acct_role_arn','Cross-Account Role ARN', 'Enter Cross-Account Role ARN to allow RapidCloud access to your Account', env_config.get('x_acct_role_arn',''), False, False],
            'vpc': [
                'vpc','AWS VPC', 'Enter AWS VPC ID', env_config.get('vpc',''), True, False],
            'region': [
                'region','AWS Region', 'Enter AWS Region (e.g. us-east-1)', env_config.get('region',''), True, False],
            'ssh_pub_key': [
                'ssh_pub_key','SSH Public Key', 'For EMR Only: Enter existing SSH Public Key if you require EMR nodes access', env_config.get('ssh_pub_key',''), False, False],
            'ips_for_ssh': [
                'ips_for_ssh','List of IP Addresses', 'For EMR Only: IP Addresses to be allowed SSH Access to EMR Cluster', env_config.get('ips_for_ssh',''), False, False],
            'vpn_only': [
                'vpn_only','VPN Only', 'Are you using VPN to connect to AWS? (yes|no)', env_config.get('vpn_only',''), True, False],
        }

        cmd = "kc init create-env --cloud aws"
        for key, prompt in prompts.items():
            value = super().get_user_input(prompt)
            setattr(self.args, key, value)
            env_config[key] = value
            if value != '':
                cmd += f" --{key} {value}"
        cmd += " --no-prompt"
        print(f"\n\n{cmd}\n\n")

        env = f"{self.args.client}_{self.args.workload}_{self.args.env_suffix}".lower()
        self.logger.info(f"create_env: `args.env` {env}")
        setattr(self.args, 'env', env)

        # resolve AWS account from aws_profile
        if self.args.aws_profile:
            aws_acct_id = boto3_utils.get_aws_account_from_profile(self.args.aws_profile)
            setattr(self.args, "account", aws_acct_id)
            env_config["account"] = aws_acct_id

        if self.args.x_acct_role_arn:
            aws_acct_id = boto3_utils.get_aws_account_from_x_acct_role(self.args.x_acct_role_arn)
            setattr(self.args, "account", aws_acct_id)
            env_config["account"] = aws_acct_id
            self.save_tenant_x_acct_role_and_region(env)

        # change environment context in "cli" mode
        if self.args.mode == 'cli':
            with open('config/aws_profile.json', 'w') as f:
                cloud_config['aws_profile'] = self.args.aws_profile
                cloud_config['x_acct_role_arn'] = self.args.x_acct_role_arn
                cloud_config['default_region'] = self.args.region
                cloud_config['env'] = env
                json.dump(cloud_config, f, indent=2)

        with open(f"config/environments/{self.args.env}_config.json", 'w') as f:
            env_config['timestamp'] = str(datetime.now())
            json.dump(env_config, f, indent=2)

        # check if target account already has RapidCloud environments, if not, generate dynamodb metadata tables
        try:
            self.logger.info("checking for metadata tables")
            resp = self.get_dynamodb_client(self.args).describe_table(TableName='profile')
            self.logger.info("metadata tables already exist")
        except Exception as e:
            # This is an expected exception when 'kc init create-env' is first executed each time a new environment is being created.
            self.logger.info(f"metadata tables DO NOT exist, using {self.args.x_acct_role_arn} if exists")
            self.logger.warning(e)
            if "ResourceNotFoundException" in str(e):
                self.logger.info("calling bootstrap")
                AwsActivator(self.args).bootstrap()

        profile_obj = Profile(self.args)
        profile = profile_obj.get_profile(env)
        new_profile = profile is None
        if profile is None:
            AwsInfra(self.args).create_tf_state()
            Property(self.args).set_default_properties()

        # save profile and all the necessary aws_infra items
        profile = profile_obj.save_profile(profile)
        self.save_aws_profile_info(profile)

        # set account permissions
        LicenseWorker(self.args).set_account_permissions()

        if new_profile:
            print(f"\n{colors.OKGREEN}You've successfully created RapidCloud environment [{self.args.env}]!{colors.ENDC}")
        else:
            print(f"\n{colors.OKGREEN}You've successfully updated RapidCloud environment [{self.args.env}]!{colors.ENDC}")

        print(f"\nTo show environment details run:\n{colors.FAIL}kc init show-env\n")

        print(f"\nTo see current state of your environment run:\n{colors.FAIL}kc status{colors.ENDC}\n")


    def save_aws_profile_info(self, profile):
        # self.logger.info(f"AwsInitWorker save profile {profile}")
        all_aws_profiles = {}
        if os.path.exists("./config/all_aws_profiles.json"):
            with open("./config/all_aws_profiles.json", 'r') as f:
                all_aws_profiles = json.load(f)

        if profile.get("aws_profile") is not None:
            all_aws_profiles[profile["aws_profile"]] = profile["region"]
        elif profile.get("x_acct_role_arn") is not None:
            all_aws_profiles[profile["x_acct_role_arn"]] = profile["region"]

        with open("./config/all_aws_profiles.json", 'w') as f:
            json.dump(all_aws_profiles, f, indent=2)

        self.logger.info(f"save_aws_profile_info: {json.dumps(all_aws_profiles, indent=2)}")


    def set_env(self, profile=None, show_status=False):
        # self.logger.info(f"AwsInitWorker set env")
        if self.args.x_acct_role_arn is None and profile is None:
            profile = self.find_env(self.args.env)
            if profile is None:
                return

        env_config_file = f"config/environments/{self.args.env}_config.json"
        if not exists(env_config_file):
            super().create_missing_env_config(profile)

        if exists(env_config_file) and self.args.mode == 'cli':
            with open('config/aws_profile.json') as f:
                aws_profile_json = json.load(f)

            with open(env_config_file) as f:
                env_config = json.load(f)
                aws_profile_json['env'] = self.args.env
                for attr in ["aws_profile", "x_acct_role_arn"]:
                    if profile.get(attr) is not None:
                        env_config[attr] = profile[attr]
                        aws_profile_json[attr] = profile[attr]
                    elif env_config.get(attr) is not None:
                        aws_profile_json[attr] = env_config[attr]

            with open('config/aws_profile.json', 'w') as f:
                json.dump(aws_profile_json, f, indent=2)

            with open(env_config_file, 'w') as f:
                json.dump(env_config, f, indent=2)

            self.save_aws_profile_info(env_config)

        if show_status:
            self.show_kc_status()


    def update_env(self):
        # self.logger.info(f"AwsInitWorker update_env")
        profile_obj = Profile(self.args)
        profile = profile_obj.get_profile(self.env)
        self.logger.info(f"update_env: {self.env}, profile: {profile}")
        if profile is None:
            AwsInfra(self.args).create_tf_state()
        Property(self.args).set_default_properties()
        Profile(self.args).save_profile(profile)

        print(f"\n{colors.OKGREEN}You've successfully updated RapidCloud environment [{self.env}]!{colors.ENDC}")


    def find_env(self, env):
        # self.logger.info(f"AwsInitWorker find env {env}")
        profile = {}
        try:
            if self.args.x_acct_role_arn is not None and self.args.x_acct_role_arn != "":
                profile = self.get_dynamodb_resource(self.args).Table('profile').get_item(Key={'name': env})
                if profile and 'Item' in profile:
                    self.logger.info(f"AwsInitWorker find_env returns {profile['Item']} using x_acct_role_arn")
                    self.logger.info(f"AwsInitWorker find_env returns {json.dumps(profile['Item'], indent=2)}")
                    return profile['Item']
        except Exception as e:
            self.logger.info(f"AwsInitWorker find_env failed to use x_acct_role_arn\n{e}")

        # if self.args.x_acct_role_arn is not None and self.args.x_acct_role_arn != "":
        #     profile = self.get_dynamodb_resource(self.args).Table('profile').get_item(Key={'name': env})
        #     if profile and 'Item' in profile:
        #         self.logger.info(f"AwsInitWorker find_env returns {json.dumps(profile['Item'], indent=2)}")
        #         return profile['Item']

        if hasattr(self, "dynamodb_resource"):
            # self.logger.info("AwsInitWorker find_env has dynamodb_resource attr")
            profile = self.dynamodb_resource.Table('profile').get_item(Key={'name': env})
            # self.logger.info(f"AwsInitWorker find_env profile {profile['Item']}")
            if profile and 'Item' in profile:
                # self.logger.info(f"AwsInitWorker find_env returns {profile['Item']} using dynamodb resource")
                return profile['Item']

        if not os.path.exists("./config/all_aws_profiles.json"):
            # print("find_env creating ./config/all_aws_profiles.json")
            with open("./config/aws_profile.json") as f:
                aws_profile = json.load(f)
                self.save_aws_profile_info(aws_profile)

        with open("./config/all_aws_profiles.json") as f:
            all_profiles = json.load(f)
            self.logger.info("AwsInitWorker find_env loading profiles from ./config/all_aws_profiles.json")
            for aws_profile_or_role, region in all_profiles.items():
                # self.logger.info(f"AwsInitWorker find_env: aws_profile_or_role/region: {aws_profile_or_role}/{region}")
                if 'arn:aws:iam::' in aws_profile_or_role:
                    self.logger.info("AwsInitWorker find_env session using x_acct_role_arn")
                    boto_session = boto3_utils.get_boto_session(region=region, x_acct_role_arn=aws_profile_or_role)
                else:
                    self.logger.info("AwsInitWorker find_env session using profile")
                    boto_session = boto3_utils.get_boto_session(region=region, aws_profile=aws_profile_or_role)
                self.logger.info(f"AwsInitWorker find_env session {boto_session}")
                if boto_session:
                    table = boto_session.resource('dynamodb').Table("profile")
                    try:
                        profile = table.get_item(Key={'name': env})
                        # self.logger.info(f"AwsInitWorker find_env returning profile items {profile['Item']}")
                        if 'Item' in profile:
                            return profile['Item']
                    except Exception as e:
                        return {}

        self.logger.warning(f"AwsInitWorker environment {env} was not found")
        return {}
