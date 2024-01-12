__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import pprint
import random
import shutil
import string
from distutils.dir_util import copy_tree

import boto3
from boto3.dynamodb.conditions import Attr, Key
from commands import boto3_utils
from commands.cli_worker.license_worker import LicenseWorker
from commands.colors import colors
from commands.kc_metadata_manager.cloud_metadata import CloudMetadata


class Metadata(CloudMetadata):

    CLOUD = "aws"
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args, self.CLOUD)
        self.args = args
        success = self.setup_sdk()
        if success:
            success = self.load_profile()
        if success:
            self.save_history()
        if not self.env:
            print(f"You don't have a current environment. Run this command:\n{colors.OKBLUE}kc init set-env --env [your_env_name]{colors.ENDC}\n")
            # return False


    def setup_sdk(self):
        try:
            self.logger.info(f"setup_sdk (get_boto_cession): region={self.region_name}, aws_profile={self.aws_profile}, x_acct_role_arn={self.x_acct_role_arn}")
            self.session = boto3_utils.get_boto_session(region=self.region_name, aws_profile=self.aws_profile, x_acct_role_arn=self.x_acct_role_arn)
            return True

        except Exception as e:
            self.logger.error(f"{colors.FAIL}{e}{colors.ENDC}")
            if self.aws_profile:
                self.logger.error(f"{colors.FAIL}Make sure your `{self.aws_profile}` AWS profile is properly configured{colors.ENDC}")
            return False


    def load_profile(self):
        if self.env and self.args.feature not in ('init', 'activate') and self.args.command != 'promote':
            self.logger.info(f"env={self.env}")
            try:
                self.profile = self.get_dynamodb_resource().Table('profile').get_item(Key={'name': self.env})['Item']
                setattr(self.args, 'env', self.env)
                setattr(self.args, 'datalake', self.profile['datalake'])
                setattr(self.args, 'data_lake_fqn', self.profile['datalake'])
                setattr(self.args, 'output_folder_path', './src/')
                setattr(self.args, 'aws_region', self.profile['region'])
                setattr(self.args, 'aws_profile', self.aws_profile)
                return True
            except Exception as e:
                self.logger.error(e)
                return False


    def save_history(self):
        if self.env:
            item = super().build_history_item()
            if item is not None:
                self.get_dynamodb_resource().Table('command_history').put_item(
                    Item=item
                )
                setattr(self.args, 'command_history_saved', 'true')
                if self.args.cmd_id:
                    setattr(self.args, 'arg_cmd_id', self.args.cmd_id)
                setattr(self.args, 'cmd_id', item['id'])
                cmd = "kc " + item["phase"]
                if "command" in item and item["command"] is not None:
                    cmd = cmd + " " + item["command"]
                self.logger.info(f"command: `{cmd}` ({item['id']})")


    def get_profile(self):
        return self.profile

    def get_boto3_session(self):
        return self.session

    def get_dynamodb_resource(self):
        return self.session.resource('dynamodb')

    def get_dynamodb_client(self):
        return self.session.client('dynamodb')

    def get_secrets_client(self):
        return self.session.client('secretsmanager')

    def get_dms_client(self):
        return self.session.client('dms')

    def get_s3_resource(self):
        return self.session.resource('s3')

    def get_s3_client(self):
        return self.session.client('s3')

    def get_kinesis_client(self):
        return self.session.client('kinesis')

    def get_firehose_client(self):
        return self.session.client('firehose')

    def get_events_client(self):
        return self.session.client('events')

    def get_resourcegroupstaggingapi_client(self):
        return self.session.client('resourcegroupstaggingapi')

    def get_glue_client(self):
        return self.session.client('glue')

    def get_lambda_clinet(self):
        return self.session.client('lambda')

    def get_pricing_client(self):
        return self.session.client('pricing')

    def get_sns_client(self):
        return self.session.client('sns')

    def get_iam_client(self):
        return self.session.client('iam')

    def get_ec2_client(self):
        return self.session.client('ec2')

    def get_ssm_client(self):
        return self.session.client('ssm')


    def delete_infra_metadata(self, module=None, command=None, name=None):
        if self.args.composite_module:
            return

        if not module:
            module = self.args.module
        if not command:
            command = self.args.command
        if not name:
            name = self.args.name

        self.logger.info(f"deleting aws_infra items for {module}_{command}_{name}")
        extra_filters = Attr('module').eq(f"{module}_{command}_{name}")
        items = self.get_all_resources(extra_filters=extra_filters)
        with self.get_dynamodb_resource().Table("aws_infra").batch_writer() as batch:
            for item in items:
                batch.delete_item(
                    Key={
                        'fqn': item['fqn']
                    }
                )


    def get_metadata_item(self, module, command, name):
        fqn = f"{self.get_env()}_{module}_{command}_{name}"
        items = self.get_dynamodb_resource().Table('metadata').query(
            KeyConditionExpression=Key('profile').eq(self.get_env()) & Key('fqn').eq(fqn)
        )['Items']
        if len(items) > 0:
            return items[0]
        else:
            return None


    def get_modules(self, module=None, command=None, name=None):
        table = self.get_dynamodb_resource().Table('metadata')
        filters = Key('profile').eq(self.get_env())
        if module:
            filters = filters & Attr('module').eq(module)
            if command is not None:
                filters = filters & Attr('command').eq(command)
            if name is not None:
                filters = filters & Attr('name').eq(name)
            items = table.scan(FilterExpression=filters)['Items']
        else:
            items = table.query(KeyConditionExpression=filters)['Items']
        return items


    def build_metadata_item(self, metadata, metadata_table, name=None, args={}, save=True):
        item = super().build_metadata_item(metadata, name, args)
        if save:
            self.logger.info(f"saving metadata item {item['fqn']}")
            response = self.get_dynamodb_resource().Table(metadata_table).put_item(Item=item)
        return item


    def put_item(self, table, item):
        if self.args.verbose:
            self.logger.info(table)
            self.logger.info(json.dumps(item, indent=2, default=str))
        if hasattr(self.args, 'cmd_id'):
            item['cmd_id'] = self.args.cmd_id
        response = self.get_dynamodb_resource().Table(table).put_item(Item=item)
        self.logger.debug(f"updated metadata [{table}]")
        self.logger.debug(json.dumps(response, indent=2))


    def get_item(self, table, pk_name, pk_value):
        response = self.get_dynamodb_resource().Table(table).get_item(Key={pk_name: pk_value})
        if 'Item' in response:
            return response['Item']
        else:
            return None


    def get_role(self, resource):
        # roles by <resource type>:<feature>:<phase>
        # handle_s3_event_" + bucket
        roles = {
            "glue_job:analytics": "analysis",
            "glue_job:transform": "analysis",
            "glue_job:publish": "publishing",
            "glue_job:aws": "publishing",

            "lambda_function:api:ingestion": "ingestion-raw",
            "lambda_function:api:analysis": "analysis",
            "lambda_function:api:publishing": "publishing",

            "lambda_function:init:ingestion": "ingestion-raw",
            "lambda_function:init:raw": "ingestion-raw",
            "lambda_function:init:analysis": "analysis",

            "lambda_function:ingest": "ingestion-raw",
            "lambda_function:transform": "analysis",
            "lambda_function:publish": "publishing",
            "lambda_function:aws": "ingestion-raw",

            "lambda_function": "service"

            # "aws_instance": "ec2"
        }

        resource_type = resource['resource_type']
        feature = resource['phase']
        suffix_idx = resource['resource_name'].rfind('_') + 1
        suffix = resource['resource_name'][suffix_idx:]
        phase = resource['phase'] if suffix not in ['ingestion','raw','analysis'] else suffix

        if f"{resource_type}:{feature}" in roles:
            return roles[f"{resource_type}:{feature}"]
        elif f"{resource_type}:{feature}:{phase}" in roles:
            return roles[f"{resource_type}:{feature}:{phase}"]
        elif resource_type in roles:
            return roles[resource_type]
        else:
            return ''

    def get_profile_info(self, profile):
        try:
            response = self.get_dynamodb_resource().Table('profile').get_item(Key={'name': profile})
            return response['Item']
        except Exception as e:
            print(e.response['Error']['Message'])
            self.logger.error(f"{colors.FAIL}{e}{colors.ENDC}")

    def get_all_resources(self, table_name="aws_infra", extra_filters=None, ignore_env_filter=False):
        if not ignore_env_filter:
            filters = Attr('profile').eq(self.get_env())
        if extra_filters:
            if filters:
                filters = filters & extra_filters
            else:
                filters = extra_filters

        self.logger.info("getting all resources")
        response = self.get_dynamodb_resource().Table(table_name).scan(
            FilterExpression=filters
        )
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = self.get_dynamodb_resource().Table(table_name).scan(
                FilterExpression=filters,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        print('\nfound {} environment resources to template\n'.format(len(response["Items"])))
        return data


    def scan_table(self, table, filters=None):
        response = table.scan(FilterExpression=filters)
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=filters,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data


    def get_aws_infra_for_command(self, cmd_id):
        filterExpression = Attr('profile').eq(self.get_env()) & Attr('cmd_id').eq(cmd_id)
        response = self.get_dynamodb_resource().Table("aws_infra").scan(
            FilterExpression=filterExpression
        )
        aws_infra_items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = self.get_dynamodb_resource().Table("aws_infra").scan(
                FilterExpression=filterExpression,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            aws_infra_items.extend(response['Items'])

        return aws_infra_items


    def add_infra_resource(self, type, name, params={}, name_separator="_", custom=False, role_name=None, fqn=None):
        self.add_aws_resource(type, name, params, name_separator, custom, role_name, fqn)


    def add_aws_resource(self, type, name, params={}, name_separator="_", custom=False, role_name=None, fqn=None):
        item = super().build_infra_item(type, name, params, name_separator, custom, role_name, fqn)
        response = self.get_dynamodb_resource().Table('aws_infra').put_item(
            Item=item
        )
        self.logger.info(f"saved {type}:{name.replace('_',name_separator)} in aws_infra, role={role_name}")
        return item


    def get_secret(self, secret_id):
        return self.get_secrets_client().get_secret_value(SecretId=secret_id)['SecretString']


    def save_secret(self, profile, resource_type, resource_name, secret_value='', use_env_prefix=True):
        tags=[
                {
                    'Key': 'env',
                    'Value': profile
                },
                {
                    'Key': 'resource_type',
                    'Value': resource_type
                },
                {
                    'Key': 'resource_name',
                    'Value': resource_name
                },
                {
                    'Key': 'caller_arn',
                    'Value': self.args.user
                }
            ]

        if use_env_prefix:
            secret_name = f"{profile}/{resource_type}/{resource_name}"
        else:
            secret_name = f"{resource_type}/{resource_name}"

        # print(secret_name)
        secrets = self.get_secrets_client().list_secrets(MaxResults=100, Filters=[{'Key': 'name','Values': [secret_name]}])
        exists = False
        for secret in secrets['SecretList']:
            if secret['Name'] == secret_name:
                exists = True
                break
        # self.logger.info(json.dumps(secrets, indent=2, default=str))

        if not exists:
            self.logger.info(f"creating secret [{secret_name}]")
            self.get_secrets_client().create_secret(
                Name=secret_name,
                SecretString=secret_value,
                Tags=tags
            )
        else:
            if secret_name != secret_value:
                self.logger.info(f"updating secret [{secret_name}]")
                self.get_secrets_client().put_secret_value(
                    SecretId=secret_name,
                    SecretString=secret_value
                )
            else:
                self.logger.info(f"secret has not been changed [{secret_name}]")

        return secret_name


    def save_password(self, profile, resource_type, resource_name, password=''):
        if password == '':
            password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(21)))

        return self.save_secret(profile, resource_type, resource_name, password)


    def get_property(self,key):
        items = self.get_dynamodb_resource().Table('property').query(
            KeyConditionExpression=Key('profile').eq(self.get_env()) & Key('name').eq(key)
        )['Items']
        if len(items) > 0:
            return items[0]['value']
        else:
            return None


    def get_properties(self,key_suffix,values_only=False):
        items = self.get_dynamodb_resource().Table('property').scan(
            FilterExpression=Attr('profile').eq(self.get_env()) & Attr('name').begins_with(key_suffix)
        )['Items']
        props = []
        for item in items:
            if values_only:
                props.append(item['value'])
            else:
                props.append({item['name']: item['value']})
        return props

    # copies entire directory
    def create_from_template(self, template_dir, new_dir):
        copy_tree(template_dir, new_dir)

    # copies single file
    def create_from_template_file(self, src_file, dest_path, dest_file):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        result = shutil.copy(src_file, f"{dest_path}/{dest_file}")
        self.logger.info(result)


    # ------------------------------------------------------------------------------------
    # Construct parameters for `aws_infra` table
    # ------------------------------------------------------------------------------------

    def get_asg_params(self):
        launch_template_version = self.args.asg_launch_template_version
        return {
            "launch_template_name": self.args.asg_launch_template_name,
            "instance_type": self.args.asg_instance_type,
            "ami_id": self.args.asg_ami_id,
            "launch_template_version": "$latest" if launch_template_version in ["", None] else launch_template_version,
            "placement_group_name": self.args.asg_placement_group_name,
            "placement_group_strategy": self.args.asg_placement_group_strategy,
            "vpc_zone_identifier": self.args.asg_vpc_zone_identifier.replace(" ","").split(","),
            "desired_capacity": self.args.asg_desired_capacity,
            "max_size": self.args.asg_max_size,
            "min_size": self.args.asg_min_size
        }

    def get_ebs_volume_params(self):
        return {
            "volume_size": self.args.ebs_volume_size,
            "availability_zone": self.args.ebs_availability_zone
        }

    def get_s3_bucket_notification_params(self, bucket, lambda_name):
            # "params": {
            #     "bucket": "kinect-atlas-dev-analysis",
            #     "lambda_function": {
            #     "events": [
            #         "s3:ObjectCreated:*"
            #     ],
            #     "filter_prefix": "logs/",
            #     "filter_suffix": ".log",
            #     "lambda_function_arn": "handle_s3_event_analysis"
            #     }
            # },
        return {
                "bucket": (self.get_env() + '-' + bucket).replace('_','-'),
                "lambda_function": {
                    "lambda_function_arn": lambda_name,
                    "events": ["s3:ObjectCreated:*"]
                }
            }

    def get_cloudfront_params(self):
        return {
            "bucket_name": self.args.cloudfront_bucket_name,
            "bucket_regional_domain_name": self.args.cloudfront_bucket_regional_domain_name,
            "origin_id": self.args.cloudfront_origin_id,
            "waf_name" : self.args.cloudfront_waf_name
        }

    def get_waf_params(self):
        return {
            "waf_name": self.args.waf_name,
            "allow_requests_by_default": self.args.waf_allow_requests_by_default,
            "cf_associated": self.args.waf_cf_associated,
            "associated_apigw_list": self.args.waf_associated_apigw_list,
            "associated_alb_list": self.args.waf_associated_alb_list
        }
    def get_datasync_params(self):
        return {
            "datasync_name": self.args.datasync_name,
            "ip_address": self.args.datasync_ip_address,
            "agent_name": self.args.datasync_agent_name,
            "nfs_location_name": self.args.datasync_nfs_location_name,
            "server_hostname": self.args.datasync_server_hostname,
            "nfs_subdirectory": self.args.datasync_nfs_subdirectory,
            "s3_bucket_name": self.args.datasync_s3_bucket_name,
            "s3_object_prefix": self.args.datasync_s3_object_prefix,
            "bucket_access_role_name": self.args.datasync_bucket_access_role_name,
            "endpoint_security_group_ids": self.args.datasync_endpoint_security_group_ids,
            "endpoint_subnet_ids": self.args.datasync_endpoint_subnet_ids,
            "agent_security_groups_ids": self.args.datasync_agent_security_groups_ids,
            "agent_subnet_ids": self.args.datasync_agent_subnet_ids,
            "endpoint_vpc_id": self.args.datasync_endpoint_vpc_id
        }

    def get_datasync_task_params(self):
        return {
            "name": self.args.datasync_name,
            "dst_datasync_name": self.args.datasync_dst_datasync_name,
            "ds_task_name": self.args.datasync_ds_task_name,
            "dst_exclude_value": self.args.datasync_dst_exclude_value,
            "dst_include_value": self.args.datasync_dst_include_value,
            "dst_schedule_expression": self.args.datasync_dst_schedule_expression
        }

    def get_fsx_params(self):
        return {
            "ad_service_name": self.args.fsx_ad_service_name,
            "ad_admin_password": self.args.fsx_ad_admin_password,
            "storage_capacity": self.args.fsx_storage_capacity,
            "throughput_capacity": self.args.fsx_throughput_capacity
        }

    def get_acm_params(self):
        return {
            "cert_domain_name": self.args.acm_cert_domain_name,
            "cert_validation_method": self.args.acm_cert_validation_method,
            "r53_zone_name": self.args.acm_r53_zone_name
        }


    def get_glue_conn_params(self, secret_name):
        host = self.args.server
        port = self.args.port

        if self.args.engine == 'mssql':
            # jdbc:sqlserver://host:port;databaseName=db_name
            db_name = self.args.db
            conn = f"jdbc:sqlserver://{host}:{port};databaseName={db_name}"
        elif self.args.engine == 'mysql':
            # jdbc:mysql://host:port/databasename
            db_name = self.args.db
            conn = f"jdbc:mysql://{host}:{port}/{db_name}"
        elif self.args.engine == 'oracle':
            # jdbc:oracle:thin://@host:port/service_name
            db_name = self.args.sid
            conn = f"jdbc:oracle:thin://@{host}:{port}/{db_name}"
        elif self.args.engine == 'postgres':
            # jdbc:postgresql://host:port/database
            db_name = self.args.db
            conn = f"jdbc:postgresql://{host}:{port}/{db_name}"

        return {
            "password": secret_name,
            "jdbc_connection": conn,
            "username": self.args.user
        }


    def get_efs_params(self):
        return {
            "encrypted": "true" if self.args.efs_encrypted.lower() in ["yes", "true"] else "false",
        }


    def get_trend_workload_agent_ports(self):
        return {
            "required": {
                "53": "DNS server port",
                "80": "HTTP Smart Protection Network Serverport",
                "123": "NTP over UDP"
            }
        }



    def get_ec2_instance_params(self):
        params = {
            "instance_type": self.args.ec2_instance_type,
            "ami_id": self.args.ec2_ami_id if self.args.ec2_ami_id else self.args.ec2_ami_id_selected,
            "key_name": self.args.ec2_key_name,
            "vpc_security_group_ids": self.args.ec2_vpc_security_group_ids.replace(" ","").split(","),
            "subnet_id": self.args.ec2_subnet_id,
            "role_name": self.args.ec2_role_name,
            "availability_zone": self.args.ec2_availability_zone,
            "volume_size": self.args.ec2_volume_size,
            "device_name": "/dev/sdh",
            "user_data": self.args.ec2_user_data,
        }

        return params


    def get_ecr_params(self):
        return {
            "image_tag_mutability": self.args.ecr_image_tag_mutability.upper(),
            "scan_on_push": "true" if self.args.ecr_scan_on_push.lower() in ["yes", "true"] else "false",
            "encryption_type": self.args.ecr_encryption_type.upper(),
            "kms_key": self.args.ecr_kms_key
        }


    def get_ecs_params(self):
        env_vars = "["
        if self.args.ecs_environment_variables.replace(" ","") == "":
            env_vars_list = []
        else:
            env_vars_list = self.args.ecs_environment_variables.replace(" ","").split(",")
        for idx, env_var in enumerate(env_vars_list):
            (key, val) = env_var.split("=")
            new_env_var = f"name = \"{key}\", value = \"{val}\""
            env_vars += ("{" + new_env_var + "}")
            if idx != len(env_vars_list)-1:
                env_vars += ","
        env_vars += "]"
        return {
            "image_url": self.args.ecs_image_url,
            "image_tag": self.args.ecs_image_tag,
            "task_cpu_units": self.args.ecs_task_cpu_units,
            "task_memory": self.args.ecs_task_memory,
            "container_cpu_units": self.args.ecs_container_cpu_units,
            "container_memory": self.args.ecs_container_memory,
            "open_ports": self.args.ecs_open_ports.replace(" ","").split(","),
            "desired_count": self.args.ecs_desired_count,
            "task_role_arn": self.args.ecs_task_role_arn,
            "assign_public_ip": "true" if self.args.ecs_assign_public_ip.lower() == "yes" else "false",
            "subnet_ids": self.args.ecs_subnet_ids.replace(" ","").split(","),
            "security_groups": self.args.ecs_security_groups.replace(" ","").split(","),
            "environment_variables": env_vars
        }


    def get_dms_source_endpoint_params(self, secret_name):
        extra_connection_attributes = "useLogMinerReader=N;useBfile=Y;parallelASMThreads=6;readAheadBlocks=150000;exposeViews=true;"
        return {
            "database_name": self.args.db,
            "engine_name": 'sqlserver' if self.args.engine == 'mssql' else self.args.engine,
            "extra_connection_attributes": extra_connection_attributes,
            "password": secret_name,
            "port": self.args.port,
            "server_name": self.args.server,
            "db_user": self.args.db_user
        }


    def get_dms_target_endpoint_params(self):
        extra_connection_attributes = "cdcPath=undefined;compressionType=NONE;dataFormat=parquet;parquetTimestampInMillisecond=true"
        return {
            "extra_connection_attributes": extra_connection_attributes,
            "s3_bucket_folder": f"databases/{self.args.name}",
            "s3_bucket_name_suffix": "ingestion"
        }


    def get_dms_task_params(self, max_roc, roc):
        if int(roc) > int(max_roc):
            migration_type = "full-load"
        else:
            migration_type = "full-load-and-cdc"

        return {
            "replication_instance": "main",
            "source_endpoint": self.args.name + "-source",
            "target_endpoint": self.args.name + "-target",
            "migration_type": migration_type
        }


    def get_lambda_layer_params(self, name):
        return {
            "filename": name
        }

    def add_trend_lambda_layer(self, params):
        trend_app_security_group = self.args.lambda_trend_app_security_group
        region = self.get_region()
        language = params['runtime'] # python, nodejs10_x, nodejs12_x, nodejs14_x
        if "python" in language:
            language = "python"
        version = 1

        secret_id = f"{self.env}/trendmicro_app_security_group_secret/{trend_app_security_group.upper()}"
        self.logger.info(f"getting secret {secret_id}")
        trend_secret = json.loads(self.get_secret(secret_id))

        params['env_vars'].update({
            "AWS_LAMBDA_EXEC_WRAPPER": "/opt/trend_app_protect",
            "TREND_GROUP": f"{self.get_env()}_{trend_app_security_group}".upper(),
            "TREND_AP_KEY": trend_secret['key'],
            "TREND_AP_SECRET": trend_secret['secret'],
            "TREND_AP_READY_TIMEOUT": 30,
            "TREND_AP_TRANSACTION_FINISH_TIMEOUT": 10,
            "TREND_AP_MIN_REPORT_SIZE": 1,
            "TREND_AP_INITIAL_DELAY_MS": 1,
            "TREND_AP_MAX_DELAY_MS": 100,
            "TREND_AP_HTTP_TIMEOUT": 5,
            "TREND_AP_PREFORK_MODE": False,
            "TREND_AP_CACHE_DIR": "/tmp/trend_cache",
            "TREND_AP_LOG_FILE": "STDERR",
            "TREND_AP_LOG_LEVEL": "INFO"
        })

        layer_arn = f"arn:aws:lambda:{region}:800880067056:layer:CloudOne-ApplicationSecurity-{language}:{version}"

        params['layers']["arn"] = layer_arn


    def get_lambda_function_params(self, env_vars={}, layers={}, default_layers=True):
        env_vars['PROFILE'] = self.get_env()

        if default_layers:
            layers["10"]  = f"{self.get_env()}_lambda_layer_awswrangler"
            layers["100"] = f"{self.get_env()}_lambda_layer_kc_common"
            layers["300"] = f"{self.get_env()}_lambda_layer_psycopg2"

        if self.args.lambda_runtime:
            lambda_runtime = self.args.lambda_runtime
        else:
            lambda_runtime = self.get_property('lambda_runtime')

        params = {
            "runtime": lambda_runtime,
            "env_vars": env_vars,
            "layers": layers,
            "timeout": 900,
            "immutable": "false"
        }

        # print(self.args.lambda_trend_app_security_group)
        if hasattr(self.args, "lambda_enable_trend") and self.args.lambda_enable_trend == "true":
            self.add_trend_lambda_layer(params)

        return params


    def get_lambda_event_source_params(self, function_name, event_source_arn, batch_size=100):
        return {
            "function_name": function_name,
            "event_source_arn": event_source_arn
        }


    def get_lb_params(self):
        return {
            "is_internal": "true" if self.args.lb_is_internal.lower() in ["yes", "true"] else "false",
            "type": self.args.lb_type,
            "subnets": self.args.lb_subnets.replace(" ","").split(","),
            "security_group_ids": self.args.lb_security_group_ids.replace(" ","").split(",")
        }


    def get_kinesis_firehose_params(self):
        return {
            "destination_bucket_name": f"{self.get_env()}-ingestion".replace('_','-'),
            # "kinesis_stream_name": f"{self.get_env()}_main",
            "s3_error_event_prefix": "event-errors/",
            "s3_prefix": "events/",
            "buffer_interval": self.get_property(f"kinesis_firehose_s3_delivery_stream_buffer_interval")
        }


    def get_redshift_params(self):
        # TODO detrermine based on data size
        node_count = self.get_property('redshift_node_count')

        # TODO detrermine based on data size and use cases
        node_type = self.get_property('redshift_node_type')

        return {
            "database_name": self.args.name,
            "master_password": self.get_env() + "/redshift_cluster/" + self.args.name,
            "master_username": "root",
            "node_count": node_count,
            "node_type": node_type,
            "parameters": {
                "require_ssl": "true"
            }
        }


    def get_dms_replication_instance_params(self):
        allocated_storage = self.get_property('dms_allocated_storage') # TODO calculate based on SourceDatabase metadata
        engine_version = self.get_property('dms_engine_version') # default to 3.1.4. Allow to change via cli
        preferred_maintenance_window = self.get_property('dms_preferred_maintenance_window') # default to mon:07:08-mon:07:38. Allow to change via cli
        replication_instance_class = self.get_property('dms_replication_instance_class') # TODO assign based on SourceDatabase metadata
        multi_az = self.get_property('dms_multi_az')
        return {
            "allocated_storage": allocated_storage,
            "engine_version": engine_version,
            "preferred_maintenance_window": preferred_maintenance_window,
            "replication_instance_class": replication_instance_class,
            "multi_az": multi_az
        }


    def get_db_params(self, dbtype, engine, resource_type, multi_az, instance_name, database_name="main"):
        allocated_storage = self.get_property(f"{dbtype}_{engine}_allocated_storage") # TODO calculate based on source db size
        instance_class = self.get_property(f"{dbtype}_{engine}_instance_class") # TODO decide based on source db size
        engine_version = self.get_property(f"{dbtype}_{engine}_engine_version")
        param_group_family = self.get_property(f"{dbtype}_{engine}_param_group_family")

        params = {
            "database_name": database_name,
            "allowed_ips": "0.0.0.0/0,10.0.0.1/32",
            "database_password": f"{self.get_env()}/{resource_type}/{instance_name}",
            "database_username": "dbadmin",
            "engine": engine,
            "engine_version": engine_version,
            "instance_class": instance_class,
            "param_group_family": param_group_family
        }

        if dbtype == 'rds':
            params["allocated_storage"] = allocated_storage
            params["multi_az"] = "true" if multi_az else "false"
            if engine == 'postgres':
                params['max_allocated_storage'] = 0
                params["parameters"] = {
                    "log_connections": 1
                }
            elif engine == 'mysql':
                params["parameters"] = {
                    "log_error_verbosity": 1
                }
        else: # aurora
            params["instance_count"] = "2"

        return params


    def get_kinesis_stream_params(self):
        retention_period = self.get_property('kinesis_stream_retention_period') # default to 48. Change via cli
        shard_count = self.get_property('kinesis_stream_shard_count') # TODO calculate
        return {
            "retention_period": retention_period,
            "shard_count": shard_count,
            "shard_level_metrics": [
                "IncomingBytes",
                "OutgoingBytes"
            ]
        }


    def get_dms_event_subscription_params(self):
        return {
            "enabled": "True",
            "name": "all_tasks",
            "source_type": "replication-task"
        }

    def get_glue_job_params(self, job_name, job_type, dataset=None, base_datasets=[], db_connection=None):
        command = {
            "name": job_type,
            "python_version": 3,
            "script_location": f"s3://{self.get_env().replace('_','-')}-glue-scripts/{job_name}.py"
        }

        utils_bucket = f"{self.get_env().replace('_','-')}-utils"
        awswrangler_egg = self.get_kc_config()['eggs']['awswrangler']
        # pyathena_egg = self.get_kc_config()['eggs']['PyAthena']
        modules_egg = self.get_kc_config()['eggs']['modules']

        params = {
            "command": command,
            "default_arguments": {
                "--job_name": job_name,
                "--env": self.get_env(),
                "--job-bookmark-option": "job-bookmark-disable",
                "--job-language": "python",
                "--generated_by": "theia",
                "--region": self.get_profile()['region'],
                "--dataset": "tbd",
                "--base_datasets": ",".join(base_datasets),
                "--extra-arg-1": "tbd",
                "--extra-arg-2": "tbd",
                "--extra-arg-3": "tbd",
                "--extra-py-files": f"s3://{utils_bucket}/etl_modules/{awswrangler_egg},s3://{utils_bucket}/etl_modules/{modules_egg}"
                # "--extra-py-files": f"s3://{utils_bucket}/etl_modules/{awswrangler_egg},s3://{utils_bucket}/egg_distributions/{pyathena_egg},s3://{utils_bucket}/etl_modules/{modules_egg}"
            }
        }

        if self.args.feature == 'transform' or self.args.feature == 'analytics':
            params['default_arguments'].update({
                "--source_bucket": f"{self.get_env().replace('_','-')}-raw",
                "--target_bucket": f"{self.get_env().replace('_','-')}-analysis",
                "--source_glue_database": f"{self.get_env()}_rawdb",
                "--target_glue_database": f"{self.get_env()}_analysisdb",
                "--transform_name": f"{self.get_env()}_generic"
            })
        elif self.args.feature == 'publish':
            params['default_arguments'].update({
                "--db_type": self.args.type,
                "--db_engine": self.args.engine,
                "--db_name": self.args.name,
                "--db_schema": self.args.schema,
                "--table": self.args.table_name,
                "--target_replace_key": self.args.replace_key,
                "--source_bucket": f"{self.get_env().replace('_','-')}-analysis"
            })

        if dataset is not None:
            params["default_arguments"]['--dataset'] = dataset

        if job_type == 'pythonshell':
            params['max_capacity'] = self.get_property('glue_job_pythonshell_max_capacity')

        if db_connection:
            params["connection"] = db_connection

        # print(params)
        return params


    def get_glue_trigger_params(self, trigger_type, job_name, condition_job_name='', schedule=''):
        if trigger_type == 'ON_DEMAND':
            predicate = {}
        else:
            predicate = {
                "conditions": {
                    "job_name": self.get_env() + '_' + condition_job_name,
                    "state": "SUCCEEDED"
                }
            }

        params = {
            "actions": {
                "job_name": self.get_env() + '_' + job_name
                # "arguments": {
                #     "--env": self.get_env(),
                #     "--env_prefix": self.get_profile()['env'],
                #     "--job-bookmark-option": "job-bookmark-disable",
                #     "--region": self.get_profile()['region'],
                #     "--source_database": self.get_env() + '_rawdb',
                #     "--target_database": self.get_env() + '_analysisdb'
                # }
            },
            "type": trigger_type,
            "predicate": predicate
        }

        if trigger_type == 'SCHEDULED':
            params['schedule'] = schedule

        return params


    def get_csv_classifier_params(self):
        return {
            "allow_single_column": False,
            "contains_header": "PRESENT",
            "delimiter": ",",
            "disable_value_trimming": False,
            "qoute_symbol": '\\"',
            "type": "csv"
        }


    def get_json_classifier_params(self):
        return {
            "json_path": "json_fire.json",
            "type": "json"
        }


    def get_glue_crawler_params(self, phase, folder, datasets, classifiers=None):
        bucket = f"{self.get_env()}-{phase}".replace('_','-')

        paths = []
        if len(datasets) == 0:
            paths.append(f"s3://{bucket}/{folder}")
        else:
            for dataset in datasets:
                if folder:
                    paths.append(f"s3://{bucket}/{folder}/{dataset['name']}")
                else:
                    paths.append(f"s3://{bucket}/{dataset['name']}")

        s3_targets = {
            "path": paths
        }

        name = f"{phase}-{folder}" if folder else phase

        if classifiers is not None:
            return {
                "classifiers": classifiers,
                "database_name": f"{self.get_env()}_{phase}db",
                "name": name,
                "s3_target": s3_targets
            }
        else:
            return {
                "database_name": f"{self.get_env()}_{phase}db",
                "name": name,
                "s3_target": s3_targets
            }



    def get_emr_cluster_params(self):
        params = {
            "applications": "Spark,Zeppelin,Hive",
            "configuration_json_file_name": "spark_hive_metastore.json",
            "core_instance_count": self.get_property('emr_core_instance_count'), # TODO calculate
            "core_instance_size": self.get_property('emr_core_instance_size'), # TODO calculate
            "master_instance_size": self.get_property('emr_master_instance_size'), # TODO calculate
            "release_label": self.get_property('emr_release_label'),
            "ssh_pub_key": self.get_profile()['ssh_pub_key'],
        }

        if self.get_profile()['vpn_only'] == 'no':
            params["access_type"] = "public"
            allowed_cidrs = []
            if 'ips_for_ssh' in self.get_profile():
                for ip_addr in self.get_profile()['ips_for_ssh']:
                    allowed_cidrs.append(f"22:22:tcp:{ip_addr}/32")
                    allowed_cidrs.append(f"8443:8443:tcp:{ip_addr}/32")
                params["allowed_cidrs"] = allowed_cidrs
        else:
            params["access_type"] = "private"

        return params


    def get_opensearch_params(self):
        return {
            "name": self.args.opensearch_name,
            "instance_type": self.args.opensearch_instance_type,
            "autotune": self.args.opensearch_autotune,
            "high_availability": self.args.opensearch_high_availability,
            "nodes": self.args.opensearch_nodes,
            "ebs_storage_size": self.args.opensearch_ebs_storage_size,
            "storage_capacity": self.args.opensearch_storage_capacity,
            "iops": self.args.opensearch_iops,
            "throughput": self.args.opensearch_throughput,
            "subnet_ids": self.args.opensearch_subnet_ids.replace(" ","").split(","),
            "security_group_ids": self.args.opensearch_security_group_ids.replace(" ","").split(",")
        }


    def get_route53_params(self):
        return {
            "record_name": self.args.route53_record_name,
            "record_type": self.args.route53_record_type,
            "zone_id": self.args.route53_zone_id,
            "ttl": self.args.route53_ttl,
            "record_list": self.args.route53_record_list.replace(" ","").split(",")
        }


    def get_s3_object_params(self, bucket, key, source):
        return {
            "bucket": bucket,
            "key": key,
            "source": source
        }


    def get_sns_topic_subscription_params(self, sns_topic_name, lambda_function_name):
        return {
            "topic_name": sns_topic_name,
            "function_name": lambda_function_name
        }


    def get_json_file(self, json_file):
        with open(json_file, 'r') as f:
                filesize = os.path.getsize(json_file)
                if filesize > 0:
                    return json.load(f)
        return {}


    def prompt(self, msg):
        if self.args.no_prompt or self.args.mode == 'console':
            return "yes"
        else:
            return input(f"{colors.OKBLUE}{msg} [curent env: {self.get_env()}] (yes|no):{colors.ENDC} ")


    def print_json(self, data):
        self.logger.info(f"\n{json.dumps(data, indent=2, default=self.json_converter)}")

