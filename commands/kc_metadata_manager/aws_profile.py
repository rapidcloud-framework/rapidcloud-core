__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import random
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr
from commands import boto3_utils, print_utils
from commands.cli_worker.license_worker import LicenseWorker
from commands.kc_metadata_manager.aws import Aws
from commands.kc_metadata_manager.aws_metadata import Metadata


class Profile(Metadata):

    TABLE_NAME = 'profile'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def save_profile(self, profile_to_update=None):
        tf_bucket = (super().get_env() + '-kc-big-data-tf-state').replace('_','-')
        # new profile only
        if profile_to_update is None:
            self.logger.info("\n\ncreating new environment ...\n\n")
        else:
            self.logger.info("\n\nupdating environment ...\n\n")

        # new profiles or moving existing profile to another account
        if profile_to_update is None or self.args.account and profile_to_update['account'] != self.args.account:
            item={
                'name': super().get_env(),
                'enabled': True,
                'env_id': ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)]),
                'client': self.args.client,
                'workload': self.args.workload,
                'env': self.args.env_suffix,
                'shared': self.args.shared.lower() in ["yes", "true", True],
                'shared_with': self.args.shared_with.split(",") if self.args.shared_with else "all",
                'aws_profile': self.args.aws_profile,
                "x_acct_role_arn": self.args.x_acct_role_arn,
                'account': self.args.account,
                'vpc': self.args.vpc,
                'region': self.args.region,
                'vpn_only': self.args.vpn_only.lower() in ["yes", "true", True],
                'ssh_pub_key': self.args.ssh_pub_key,
                "ips_for_ssh": self.args.ips_for_ssh.split(",") if self.args.ips_for_ssh else "",
                'datalake': f"{self.args.client}_{self.args.env_suffix}",
                'state_bucket': tf_bucket,
                'state_lock_table': tf_bucket.replace('-','_'),
                'infra_enabled': False,
                'created_timestamp': str(datetime.now()),
                'created_by': self.args.current_session_email,
                'timestamp': str(datetime.now()),
                'updated_by': self.args.current_session_email
            }

        # updating existing profile
        else:
            item = profile_to_update
            item.update({
                'shared': self.args.shared.lower() in ["yes", "true", True],
                'shared_with': self.args.shared_with.split(",") if self.args.shared_with else "all",
                'aws_profile': self.args.aws_profile,
                "x_acct_role_arn": self.args.x_acct_role_arn,
                'vpc': self.args.vpc,
                'vpn_only': self.args.vpn_only.lower() in ["yes", "true", True],
                'ssh_pub_key': self.args.ssh_pub_key,
                "ips_for_ssh": self.args.ips_for_ssh.split(",") if self.args.ips_for_ssh else "",
                'timestamp': str(datetime.now()),
                'created_by': profile_to_update['updated_by'] if 'created_by' not in profile_to_update else profile_to_update['created_by'],
                'updated_by': self.args.current_session_email
            })

        super().put_item(self.TABLE_NAME, item)

        super().add_aws_resource('kms_key', super().get_env(), {})
        super().add_aws_resource('s3_bucket', "utils", {})
        super().add_aws_resource('sns_topic', 'general_notifications')

        # generic event handler lambda function
        params = super().get_lambda_function_params(default_layers=True)
        params['source_path'] = "generic_event_handler"
        params['memory_size'] = 128
        super().add_aws_resource('lambda_function', "generic_event_handler", params)

        # CloudFormation Stack Status Change event
        params ={
            "event_pattern": {
                "source": "aws.cloudformation",
                "detail-type": "CloudFormation Stack Status Change"
            },
            "target_type": "lambda_function",
            "target": "generic_event_handler"
        }
        self.add_aws_resource('cloudwatch_event_rule', "cf_events", params)

        # EC2 Instance State-change Notification
        params ={
            "event_pattern": {
                "source": "aws.ec2",
                "detail-type": "EC2 Instance State-change Notification"
            },
            "target_type": "lambda_function",
            "target": "generic_event_handler"
        }
        self.add_aws_resource('cloudwatch_event_rule', "ec2_events", params)

        # create lambda layer for kc_common code
        kc_common_layer = super().get_kc_config()['lambda_layers']['kc_common']
        params = super().get_lambda_layer_params(kc_common_layer)
        super().add_aws_resource('lambda_layer', "kc_common", params)

        # create lambda layer for kc_textract code
        kc_textract_layer = super().get_kc_config()['lambda_layers']['kc_textract']
        params = super().get_lambda_layer_params(kc_textract_layer)
        super().add_aws_resource('lambda_layer', "kc_textract", params)

        # create lambda layer for psycopg2
        psycopg2_layer = super().get_kc_config()['lambda_layers']['psycopg2']
        params = super().get_lambda_layer_params(psycopg2_layer)
        super().add_aws_resource('lambda_layer', "psycopg2", params)

        # create awswrangler lambda layer
        awswrangler_layer = super().get_kc_config()['lambda_layers']['awswrangler']
        params = super().get_lambda_layer_params(awswrangler_layer)
        super().add_aws_resource('lambda_layer', "awswrangler", params)

        # create lambda layer for Okta
        okta_layer = super().get_kc_config()['lambda_layers']['okta']
        params = super().get_lambda_layer_params(okta_layer)
        super().add_aws_resource('lambda_layer', "okta", params)

        if profile_to_update is None:
            # create terraform state bucket
            Aws(self.args).create_terraform_bucket(tf_bucket, self.args.region)

        return item


    def add_ip_addr(self):
        profile_table = super().get_dynamodb_resource().Table('profile')
        profile = profile_table.get_item(Key={'name': self.env})['Item']
        ips_for_ssh = profile['ips_for_ssh'] if 'ips_for_ssh' in profile else []
        ip_addr = self.args.ip_addr
        self.logger.info(f"ips_for_ssh: {ips_for_ssh}")
        if ip_addr not in ips_for_ssh:
            self.logger.info(f"Adding IP Address: {ip_addr}")
            ips_for_ssh.append(ip_addr)
            response = profile_table.update_item(Key={'name': super().get_env()},
                UpdateExpression="set ips_for_ssh = :p",
                ExpressionAttributeValues={':p': ips_for_ssh}
            )
            self.logger.debug(response)


    def get_profile(self, env) -> dict:
        self.logger.info(f"getting {self.args.cloud} profile [{env}]")
        # TODO handle cloud specific
        if self.args.cloud == "aws":
            try:
                profile = super().get_dynamodb_resource().Table('profile').get_item(Key={'name': env})
                # self.logger.info(json.dumps(profile, indent=2, default=str))
                if 'Item' in profile:
                    return profile['Item']
                else:
                    return None
            except Exception as e:
                return None
        return {} # azure and gcp for now


    def get_all_profiles(self):
        '''
        with saas we store every env we create in `x-acct-roles`
        this is done to save state, and we first pull this and
        use those profiles, we then merge those with anything on the file system
        '''

        filters = Attr('enabled').eq(True)
        accts = []
        data = []

        all_profiles = {}
        tenant_stored_profiles = {}
        fs_profiles = {}

        # get profiles from tenant table
        saas_params = {
            "action": "get_tenant",
            "email": self.args.current_session_email
        }

        tenant = LicenseWorker(self.args).contact_lic_server("saas", params=saas_params)
        if 'x-acct-roles' in tenant.keys():
            for k, v  in tenant['x-acct-roles'].items():
                tenant_stored_profiles[v['role']] = v['region']

        # get profiles from file system
        if os.path.exists("./config/all_aws_profiles.json"):
            with open("./config/all_aws_profiles.json", 'r') as f:
                fs_profiles = json.load(f)


        self.logger.info(f"get_all_profiles -> tenant_stored {tenant_stored_profiles}")
        # merge all profiles
        for role, region in tenant_stored_profiles.items():
            all_profiles[role] = region

        self.logger.info(f"get_all_profiles -> fs_stored {fs_profiles}")
        for role, region in fs_profiles.items():
            all_profiles[role] = region

        self.logger.info(f"get_all_profiles -> all {all_profiles}")
        for aws_profile_or_role, region in all_profiles.items():
            self.logger.info(f"aws_profile -> get_all_profiles {aws_profile_or_role}/{region}")
            try:
                if 'arn:aws:iam' in aws_profile_or_role:
                    acct_id = boto3_utils.get_aws_account_from_x_acct_role(aws_profile_or_role)
                    if acct_id is not None and acct_id not in accts:
                        accts.append(acct_id)
                        table = boto3_utils.get_boto_session(x_acct_role_arn=aws_profile_or_role).resource('dynamodb').Table("profile")
                    else:
                        continue
                else:
                    acct_id = boto3_utils.get_aws_account_from_profile(aws_profile_or_role)
                    if acct_id is not None and acct_id not in accts:
                        accts.append(acct_id)
                        table = boto3_utils.get_boto_session(region=region, aws_profile=aws_profile_or_role).resource('dynamodb').Table("profile")
                    else:
                        continue

                acct_profiles = self.scan_table(table, filters)
                data.extend(acct_profiles)
                self.logger.info(f"{aws_profile_or_role} has {len(acct_profiles)} environments")
            except Exception as e:
                self.logger.warn(f"{aws_profile_or_role} has no environments")

        for e in data:
            if e["account"] is  None:
                e['account'] = "UNKNOWN"
        data.sort(key=lambda x: (x["account"],x["name"]))
        self.logger.info(f"get_all_profiles -> accts: {accts}")
        for k in data:
            self.logger.info(f"get_all_profiles -> data: {k}")
        return data
