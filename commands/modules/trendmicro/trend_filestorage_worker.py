__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import copy
import json
import logging
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

from commands import json_utils, print_utils
from commands.colors import colors
from commands.modules import exec_module
from commands.modules import pause
import commands.modules.trendmicro.trend_api as trend_api


CF_TEMPLATES = {
    "scanner": "https://file-storage-security.s3.amazonaws.com/latest/templates/FSS-Scanner-Stack.template",
    "storage": "https://file-storage-security.s3.amazonaws.com/latest/templates/FSS-Storage-Stack.template",
    "all-in-one": "https://file-storage-security.s3.amazonaws.com/latest/templates/FSS-All-In-One.template"
}


class TrendFilestorageSecurityWorker(object):

    logger = logging.getLogger(__name__)

    def __init__(self, module):
        self.module = module
        self.args = module.args
        self.env = module.env
        self.API_KEY = None
        self.cloudformation_client = module.get_boto3_session().client('cloudformation')
        self.kms_client = module.get_boto3_session().client('kms')
        self.sts_client = module.get_boto3_session().client('sts')
        self.lambda_client = module.get_boto3_session().client('lambda')
        self.metadata_table = module.get_dynamodb_resource().Table("metadata")


    def get_stack_name(self, stack_type, bucket=None):
        if stack_type != "scanner":
            stack_name = f"{self.env}-TM-FSS-{stack_type}-{bucket}-Stack"
        else:
            stack_name = f"{self.env}-TM-FSS-Scanner-Stack"
        return stack_name.replace('_','-')


    def get_scanner_metadata(self):
        result = self.module.get_dynamodb_resource().Table('metadata').scan(
        FilterExpression=Attr('profile').eq(self.env) & Attr('module').eq('trendmicro') & Attr('command').eq('filestorage_create_stack') & Attr('params.trendmicro_stack_type').eq('scanner'))['Items']
        if len(result) > 0:
            return result[0]
        return None


    def filestorage_create_stack(self, metadata=None):
        stack_metadata = metadata
        self.logger.info(json.dumps(stack_metadata, indent=2, default=str))
        pause(self.args)

        # make sure datalake was created already, if not, create it
        if self.module.get_item("aws_infra", "fqn", f"{self.env}_s3_bucket_ingestion"):
            self.logger.info("Current environment already has a datalake")
        else:
            exec_module(self.args, "datalake", "create")

        env = self.env
        stack_type = self.args.trendmicro_stack_type
        stack_name = self.get_stack_name(stack_type, self.args.trendmicro_bucket)
        self.logger.info(f"stack_name: {stack_name}")

        # get existing stacks
        result = trend_api.call_api(self.env, trend_api.FILE_STORAGE_SECURITY, "GET", "stacks", boto3_session=self.get_boto3_session())
        result = json_utils.flatten(result['stacks'], 'details')
        tm_stacks = {}
        new_tm_stack = True
        tm_scanner_stack = None
        for stack in result:
            if 'name' in stack and env.replace('_','-') in stack['name']:
                if stack_name in stack['name']:
                    new_tm_stack = False
                if stack['type'] == "scanner":
                    tm_scanner_stack = stack
                tm_stacks[stack['name']] = stack
        # self.logger.info(json.dumps(result, indent=2, default=str))
        print_utils.print_grid_from_json(result, cols=['name','type','region','stackID','status'], title="Existing Trend Micro Stacks from API call")
        pause(self.args)

        # ensure one scanner stack per environment
        scanner_metadata = self.get_scanner_metadata()
        self.logger.info("scanner_metadata:")
        self.logger.info(json.dumps(scanner_metadata, indent=2, default=str))
        if stack_type != "storage" and scanner_metadata and tm_scanner_stack:
            self.logger.warning("You already have scanner stack for this environment")
            self.metadata_table.delete_item(Key={"profile": env, "fqn": stack_metadata['fqn']})
            return

        # split all-in-one into two metadata items, scanner and storage
        storage_metadata = None
        if "all-in-one" == stack_type == stack_metadata['params']['trendmicro_stack_type']:
            for value in ['scanner', 'storage']:
                metadata_copy = copy.deepcopy(stack_metadata)
                metadata_copy['fqn'] = metadata_copy['fqn'] + f"_{value}"
                if value == 'scanner':
                    metadata_copy['params']['bucket'] = ""
                    metadata_copy['params']['trendmicro_bucket'] = ""
                    scanner_metadata = metadata_copy
                else:
                    storage_metadata = metadata_copy
                
                metadata_copy['name'] = f"{metadata_copy['name']}_all-in-one_{value}"
                metadata_copy['params']['trendmicro_stack_type'] = value
                self.logger.info(f"{value} metadata_copy")
                self.logger.info(json.dumps(metadata_copy, indent=2, default=str))
                self.metadata_table.put_item(Item=metadata_copy)
                pause(self.args)

            # delete original all-in-one metadata
            self.metadata_table.delete_item(Key={"profile": env, "fqn": stack_metadata['fqn']})
        
        elif "scanner" == stack_type:
            scanner_metadata = stack_metadata

        elif "storage" == stack_type:
            storage_metadata = stack_metadata

        # do not proceed if stack already exists or in process of being created
        if not new_tm_stack:
            self.logger.warning(f"FSS Stack {stack_name} has already been added")
            return

        # create s3 buckets if needed
        buckets = {}
        if stack_type in ["storage", "all-in-one"]:
            buckets = self.create_s3_buckets(stack_type, env)
            pause(self.args)

        # make sure cloudformation stack doesn't exist yet
        pause(self.args)
        cf_stack = self.get_cf_stack(stack_name)
        if cf_stack is not None:
            self.logger.warning(f"Cloudformation Stack {stack_name} is in {cf_stack['StackStatus']} state")
            if cf_stack['StackStatus'] == "CREATE_COMPLETE":
                # make sure stack(s) properly created in tren micro
                # invoke generic_event_handler
                lambda_payload = json.dumps({
                    "rapidcloud_action": "rc_trendmicro.deploy_filestorage_stack",
                    "stack_name": stack_name,
                    "cf_stack": cf_stack
                }, default=str)
                self.logger.info("invoking generic_event_handler")
                pause(self.args)
                resp = self.lambda_client.invoke(FunctionName=f"{env}_generic_event_handler", 
                     InvocationType='Event',
                     Payload=lambda_payload) 
                self.logger.info(json.dumps(resp, indent=2, default=str))               
            return cf_stack

        # create cloudformation stack
        pause(self.args)
        cf_stack = self.create_cf_stack(stack_name, stack_type, scanner_metadata, storage_metadata)

        # generate Customized Post-scan Lambda
        self.create_post_scan_lambda(storage_metadata)


    def create_s3_buckets(self, stack_type, env):
        buckets = {
            self.args.bucket: f"{env.replace('_','-')}-{self.args.bucket}",
            "quarantine": f"{env.replace('_','-')}-quarantine"
        }
        # create scan and quarantine buckets if don't exist
        s3_client = self.module.get_s3_client()
        for k, bucket in buckets.items():
            try:
                s3_client.get_bucket_location(Bucket=bucket)
                self.logger.warning(f"bucket {bucket} already exists")
            except botocore.exceptions.ClientError as e:
                self.module.add_aws_resource('s3_bucket', k, {})
                s3_client.create_bucket(ACL='private',Bucket=bucket)
                self.logger.info(f"created bucket: {bucket}")
        return buckets

    
    def filestorage_list_stacks(self, metadata=None, quiet=False):
        rc_stacks = []
        for stack in self.module.get_modules(module="trendmicro"):
            if stack['command'] == "filestorage_create_stack":
                stack.update(stack["params"])
                rc_stacks.append(stack)

        if not quiet:
            print_utils.print_grid_from_json(rc_stacks, cols=['module','command','name','trendmicro_stack_type','trendmicro_bucket','trendmicro_role_arn'], title="RapidCLoud Managed File Storage Security Stacks")

        tm_stacks = trend_api.call_api(self.env, trend_api.FILE_STORAGE_SECURITY, "GET", "stacks", boto3_session=self.get_boto3_session())
        if not quiet:
            self.logger.info(json.dumps(tm_stacks, indent=2, default=str))
        
        return rc_stacks, tm_stacks


    def get_cf_stack(self, stack_name):
        try:
            self.logger.info(f"getting CF stack {stack_name}")
            result = self.cloudformation_client.describe_stacks(StackName=stack_name)
            if "Stacks" in result and len(result['Stacks']) > 0:
                cf_stack = result['Stacks'][0]
                cf_stack['parsed'] = {
                    "status": cf_stack['StackStatus'],
                    "params": {},
                    "outputs": {},
                    "tags": {}
                }

                for param in cf_stack['Parameters']:
                    cf_stack['parsed']['params'][param['ParameterKey']] = param['ParameterValue']

                for output in cf_stack['Outputs']:
                    cf_stack['parsed']['outputs'][output['OutputKey']] = output['OutputValue']

                for tag in cf_stack['Tags']:
                    cf_stack['parsed']['tags'][tag['Key']] = tag['Value']

                del cf_stack['Parameters']
                del cf_stack['Outputs']
                del cf_stack['Tags']
                self.logger.info(f"{stack_name} status -> {cf_stack['StackStatus']}")
                # self.logger.info(json.dumps(cf_stack, indent=2, default=str))

                return cf_stack
        except Exception as e:
            self.logger.info(e)
            return None


    def create_cf_stack(self, stack_name, stack_type, scanner_metadata, storage_metadata):
        env = self.env

        # get KMS Key ARN
        for alias in self.kms_client.list_aliases(Limit=1000)['Aliases']:
            if alias['AliasName'] == f"alias/{env}":
                key_id = alias['TargetKeyId']
                kms_key_arn = self.kms_client.describe_key(KeyId=key_id)['KeyMetadata']['Arn']
                break
        
        # CF Template Parameters
        params = {
            # "KMSKeyARNForQueueSSE": env,
            # "KMSKeyARNsForTopicSSE": env,
            "FSSBucketName": "file-storage-security",
            "FSSKeyPrefix": "latest/",
            "TrendMicroManagementAccount": "415485722356",
            "CloudOneRegion": "us-1",
            "ExternalID": "112040658709"
        }
        
        if stack_type == "scanner":
            params.update({
                "ScannerEphemeralStorage": "512"
            })
        elif stack_type == "storage":
            params.update({
                "ScannerAWSAccount": self.sts_client.get_caller_identity()['Account'],
                "ScannerSQSURL": scanner_metadata['cf_stack']['outputs']['ScannerQueueURL'],
                "S3BucketToScan": f"{env.replace('_','-')}-{self.args.bucket}",
                "ObjectFilterPrefix": "",
                "KMSKeyARNForBucketSSE": kms_key_arn,
                "IAMRolePrefix": f"{env}-",
                "IAMPolicyPrefix": env.replace('_','') + '-',
                "LambdaFunctionPrefix": f"{env}-",
                # "LambdaLayerPrefix": f"{env}-",
                # "SQSQueuePrefix": f"{env}_",
                "SNSTopicPrefix": env.replace('_','') + '-',
            })
        elif stack_type == "all-in-one":
            params.update({
                "S3BucketToScan": f"{env.replace('_','-')}-{self.args.bucket}",
                "ObjectFilterPrefix": "",
                "KMSKeyARNForBucketSSE": kms_key_arn,
                "ScannerEphemeralStorage": "512",
                "TriggerWithObjectCreatedEvent": "true",
                "ReportObjectKey": "false",
                "ScanOnGetObject": "false"
            })

        parameters = []
        for param, value in params.items():
            parameters.append({'ParameterKey': param, 'ParameterValue': value})
        self.logger.info(json.dumps(parameters, indent=2, default=str))
        
        tags = [
            {'Key': 'env','Value': env}, 
            {'Key': 'caller_arn','Value': self.args.user}
        ]
        if scanner_metadata:
            tags.append({'Key': 'scanner','Value': scanner_metadata['fqn']})
        if storage_metadata:
            tags.append({'Key': 'storage','Value': storage_metadata['fqn']})
        self.logger.info(json.dumps(tags, indent=2, default=str))

        # create CF stack
        pause(self.args)
        result = self.cloudformation_client.create_stack(
            StackName=stack_name,
            TemplateURL=CF_TEMPLATES[stack_type],
            Parameters=parameters,
            DisableRollback=False,
            Capabilities=['CAPABILITY_NAMED_IAM','CAPABILITY_IAM',],
            Tags=tags,
            EnableTerminationProtection=False
            # TimeoutInMinutes=123,
            # NotificationARNs=[
            #     'string',
            # ],
            # 'CAPABILITY_IAM'|'CAPABILITY_NAMED_IAM'|'CAPABILITY_AUTO_EXPAND',
            # ResourceTypes=[
            #     'string',
            # ],
            # RoleARN='string',
            # OnFailure='DO_NOTHING'|'ROLLBACK'|'DELETE',
            # StackPolicyBody='string',
            # StackPolicyURL='string',
            # ClientRequestToken='string',
        )
        self.logger.info(json.dumps(result, indent=2, default=str))
        pause(self.args)

        cf_stack = self.get_cf_stack(stack_name) 
        return cf_stack


    def create_post_scan_lambda(self, storage_metadata):
        if storage_metadata is None:
            self.logger.warning("Post Scan Lambda can only be created for `storage` stack")
            return 

        bucket_to_scan = storage_metadata['params']['trendmicro_bucket']
        self.logger.info(f"bucket_to_scan: {bucket_to_scan}")
        self.logger.info(json.dumps(storage_metadata, indent=2, default=str))
        pause(self.args)

        env = self.env
        account_id = self.sts_client.get_caller_identity()['Account']
        
        # policy
        policy_name = f"{env}-scan-ingestion-lambda".replace('_','-')
        policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
        try:
            result = self.module.get_iam_client().get_policy(PolicyArn=policy_arn)
            policy_version = result['Policy']['DefaultVersionId']
            policy_version_number = int(policy_version.replace('v', ''))
            self.logger.info(f"policy_version {policy_version}:")
            policy = self.module.get_iam_client().get_policy_version(PolicyArn=policy_arn,VersionId=policy_version)['PolicyVersion']['Document']
            self.logger.info(json.dumps(policy, indent=2, default=str))
            try:
                if policy_version_number > 1:
                    response = self.module.get_iam_client().delete_policy_version(PolicyArn=policy_arn,VersionId=f"v{policy_version_number - 1}")
                    self.logger.info(json.dumps(response, indent=2, default=str))
            except Exception as e:
                self.logger.warning(e)
        except:
            pass
        
        allow_post_scan_res = None
        for res in policy['Statement']:
            if res['Sid'] == 'AllowPostScan':
                allow_post_scan_res = res
                break
        
        if allow_post_scan_res is None:
            allow_post_scan_res = {
                "Sid": "AllowPostScan",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:DeleteObject",
                    "s3:GetObjectTagging"
                ],
                "Resource": []
            }

        scan_res = f"arn:aws:s3:::{self.env.replace('_','-')}-{bucket_to_scan}"
        if scan_res not in res['Resource']:
            res['Resource'].append(scan_res + "/*")
            res['Resource'].append(scan_res)

        self.logger.info("policy:")
        self.logger.info(json.dumps(policy, indent=2, default=str))
        pause(self.args)

        # update policy by creating new version and setting as default
        response = self.module.get_iam_client().create_policy_version(
            PolicyArn=policy_arn,
            PolicyDocument=json.dumps(policy),
            SetAsDefault=True
        )
        self.logger.info(json.dumps(response, indent=2, default=str))

        # add Lambda function to aws_infra
        pause(self.args)
        lambda_name = "trendmicro_post_scan"
        params = self.module.get_lambda_function_params(default_layers=False)
        params['source_path'] = lambda_name
        params['memory_size'] = 512
        self.module.add_aws_resource('lambda_function', lambda_name, params, role_name="scan-ingestion")

        pause(self.args)
        LINE = "--------------------------------------------------------------------------------------\n"
        self.logger.info(f"\n\n{colors.FAIL}{LINE}IMPORTANT:\n{LINE}{colors.ENDC}Run {colors.OKBLUE}`kc tf apply`{colors.ENDC} to deploy post-scan custom lambda function if you didn't do so already.\n{colors.FAIL}{LINE}{colors.ENDC}\n\n")


    def filestorage_delete_stack(self):
        response = self.module.prompt(msg="\nAre you sure you want to remove this stack? This will delete CloudFormation Stack in your AWS account and corresponding File Storage Security stack in your Trend Micro Cloud One account")

        if response != 'yes':
            self.logger.warning("delete_fss_stack command cancelled")
            return

        fqn = self.args.trendmicro_fqn
        self.logger.info(f"deleting stack {fqn}")
        stack_metadata = self.metadata_table.query(
            KeyConditionExpression=Key('profile').eq(self.env) & Key('fqn').eq(fqn)
        )['Items']
        self.logger.info(json.dumps(stack_metadata, indent=2, default=str))
        if len(stack_metadata) > 0:
            stack_metadata = stack_metadata[0]
        else:
            self.logger.warning(f"stack_metadata fqn: {fqn} is not found")
            return
        pause(self.args)

        # delete cloudformation stack
        try:
            stack_name = stack_metadata['cf_stack']['stack_name']
            cf_stack = self.get_cf_stack(stack_name)
            self.logger.info(json.dumps(cf_stack, indent=2, default=str))
            pause(self.args)

            result = self.cloudformation_client.delete_stack(StackName=stack_name)
            self.logger.info(json.dumps(result, indent=2, default=str))
            pause(self.args)
        except Exception as e:
            self.logger.warning(e)

        # delete TM-FSS stack
        try:
            tm_stack_id = stack_metadata['params']['stackID']
            result = trend_api.call_api(self.env, trend_api.FILE_STORAGE_SECURITY, "DELETE", "stacks", params={"id": tm_stack_id}, boto3_session=self.get_boto3_session())
            self.logger.info(json.dumps(result, indent=2, default=str))
            pause(self.args)
        except Exception as e:
            self.logger.warning(e)

        # delete metadata
        result = self.metadata_table.delete_item(Key={"profile": self.env, "fqn": fqn})
        self.logger.info(json.dumps(result, indent=2, default=str))
