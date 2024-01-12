__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import csv
import json
import logging
import os
import subprocess
import sys
import traceback

import pandas as pd
from arnparse import arnparse
from boto3.dynamodb.conditions import Attr, Key
from commands.colors import colors
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_profile import Profile
from commands.kc_metadata_manager.command_history import CommandHistory
from commands.kc_metadata_manager.schedule import Schedule
from data_scripts.kc_load_data_type_translation import DataTypeTranslation
from progress.bar import Bar
from tabulate import tabulate
from terraform.bin import kctf


class AwsInfra(Metadata):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    class Table:
        def __init__(self, name="", pkey="", skey="", cleanup="", promote=True, create_index_by_profile=False) :
            self.name = name
            self.pkey = pkey
            self.skey = skey
            self.cleanup = cleanup
            self.promote = promote
            self.create_index_by_profile = create_index_by_profile

    metadata_tables = [
      # [name, pk, sk, cleanup, promote]
        ["kc_activation","email","",False,True],
        ["command_history","timestamp","",False,False],
        ["command","profile","step",True,True],
        ["profile","name","",False,False],
        ["log","profile","timestamp",True,False],
        ["api_endpoint","endpoint","dataset",True,True],
        ["aws_infra","fqn","",True,True],
        ["cdc_tracker","dms_task_arn","task_status",True,False],
        ["data_type_translation","engine","cast_from",False,False],
        ["datalake","fqn","",False,False],
        ["dataset","fqn","",True,True],
        ["dataset_unstructured","fqn","",True,True],
        ["dataset_semi_structured","fqn","",True,True],
        ["datawarehouse","fqn","",True,True],
        ["event","fqn","",True,True],
        ["publishing","fqn","",True,True],
        ["role","fqn","",True,True],
        ["format","fqn","",True,True],
        ["rule","fqn","",True,True],
        ["schedule","task","",True,True],
        ["source_column","table","column",True,True],
        ["source_database","fqn","",True,True],
        ["source_table","fqn","",True,True],
        ["stream","fqn","",True,True],
        ["target_database","fqn","",True,True],
        ["transformation","fqn","",True,True],
        ["analytics","fqn","",True,True],
        ["file","fqn","",True,True],
        ["property","profile","name",False,False],
        ["deployment","profile","step",True,False],
        ["cdc_log","fqn","",True,False],
        ["transform_log","fqn","",True,False],
        ["publish_log","fqn","",True,False],
        ["pricing","resource_type","",True,False],
        ["metadata","profile","fqn",True,True],
        ["resources","profile","resource_type",True,False],
    ]


    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def json_converter(self, obj):
        return str(obj)


    def prompt(self, step, msg):
        if self.args.no_prompt or self.args.mode == 'console':
            return "yes"
        else:
            return input(f" {colors.OKBLUE}{step}. {msg}... (yes|no):{colors.ENDC} ")

    # ------------------------------------------------------------------------------------
    # this is done once as part of `tf <action>` to execute terraform commands
    # ------------------------------------------------------------------------------------

    def exec_tf_action(self, action, subscription_tier, no_prompt):
        os.environ['AWS_PROFILE'] = self.get_aws_profile()
        os.environ['AWS_REGION'] = self.get_region()
        os.environ['terraform_dir'] = os.getcwd() + "/terraform/"
        self.logger.info(f"AWS_PROFILE={os.environ['AWS_PROFILE']}")

        items = self.get_all_resources()
        profile = self.get_profile_info(self.env)
        profile['name_dashed'] = profile['name'].replace('_', '-')
        profile['arn_prefix'] = "arn:aws"
        if "gov" in profile['region']:
            profile['arn_prefix'] = "arn:aws-us-gov"

        kctf.main(self.args, profile, items, self.env, action, subscription_tier, no_prompt=no_prompt)

    # ------------------------------------------------------------------------------------
    # this is done once as part of `kc activate` to generate metadata DynamoDB tables
    # ------------------------------------------------------------------------------------
    def create_metadata_tables(self):
        # self.logger.info(f"create_metadata_table: {self.args.x_acct_role_arn}")
        response = super().get_dynamodb_client().list_tables()
        existing_tables = response['TableNames']
        while 'LastEvaluatedTableName' in response:
            response = super().get_dynamodb_client().list_tables(
                ExclusiveStartTableName=response['LastEvaluatedTableName'])
            existing_tables.extend(response['TableNames'])

        self.logger.debug(f"{len(existing_tables)} tables")
        self.logger.debug(json.dumps(existing_tables, indent=2))

        # Create metadata tables if they don't exist
        for table in self.metadata_tables:
            if table[0] not in existing_tables:
                self.logger.info("Creating " + str(table) + "...")
                self.create_metadata_table(table)


    # ------------------------------------------------------------------------------------
    # this is done once as part of `kc init create-env` to generate rdbms mappings
    # ------------------------------------------------------------------------------------
    def load_data_type_mappings(self):
        # existing_tables = super().get_dynamodb_client().list_tables()['TableNames']
        # if 'data_type_translation' not in existing_tables:
        setattr(self.args, 'aws_region', super().get_region())
        setattr(self.args, 'profile', super().get_env())
        setattr(self.args, 'aws_profile', super().get_aws_profile())
        self.logger.info(" loading data type mappings into `data_type_translation` table...")
        DataTypeTranslation().main(self.args)


    # ------------------------------------------------------------------------------------
    # this is done once as part of `kc init create-env` to generate Terraform state info
    # ------------------------------------------------------------------------------------
    def create_tf_state(self):
        # TF state bucket and table
        tf_state = f"{super().get_env()}_kc_big_data_tf_state"
        self.metadata_tables.append([tf_state, "LockID", "", True, False])
        self.logger.info(f"creating S3 bucket {tf_state.replace('_','-')}")

        try:
            if super().get_region() != 'us-east-1':
                super().get_s3_client().create_bucket(Bucket=tf_state.replace('_','-'), CreateBucketConfiguration={'LocationConstraint': super().get_region()})
            else:
                super().get_s3_client().create_bucket(Bucket=tf_state.replace('_','-'))
        except Exception as e:
            self.logger.info(e)

        try:
            # Create TF state table
            tf_table = (super().get_env() + '-kc-big-data-tf-state').replace('-','_')
            self.create_metadata_table([tf_table, "LockID", "", False])
        except Exception as e:
            self.logger.info(e)


    # ------------------------------------------------------------------------------------
    # delete metadata to reverse specified command or remove all metadata for the environment
    # ------------------------------------------------------------------------------------
    def delete_metadata(self, cmd_id='all', table='all'):
        for table_arr in self.metadata_tables:
            table = self.Table(table_arr[0], table_arr[1], table_arr[2], table_arr[3])
            if table.cleanup:
                metadata_table = super().get_dynamodb_resource().Table(table.name)
                try:
                    extra_filters = None
                    if cmd_id != 'all':
                        extra_filters = Attr('cmd_id').eq(cmd_id)
                    items = super().get_all_resources(table.name, extra_filters)
                    if len(items) > 0:
                        progress = Bar(f"    Deleting metadata [{table.name}], profile [{super().get_env()}]", max=len(items))
                        for item in items:
                            key = {table.pkey: item[table.pkey]}
                            if table.skey != '':
                                key[table.skey] = item[table.skey]
                            metadata_table.delete_item(Key=key)
                            progress.next()
                        progress.finish()

                except Exception as e:
                    self.logger.info("")


    # ------------------------------------------------------------------------------------
    # get metadata for specified environment
    # ------------------------------------------------------------------------------------
    def get_metadata(self, source_profile):
        metadata = {}
        self.logger.info(f" Getting metadata for [{source_profile['name']}]")
        for table_arr in self.metadata_tables:
            table = self.Table(table_arr[0], table_arr[1], table_arr[2], table_arr[3], table_arr[4])
            if table.promote:
                items = super().get_all_resources(table_name=table.name)
                if len(items) > 0:
                    self.logger.info(f" [{table.name}] {len(items)}")
                    metadata[table.name] = {
                        "items": items
                    }
        return metadata


    # ------------------------------------------------------------------------------------
    # get resource definitions for specified resource_type (e.g. `glue_crawler`) and name
    # ------------------------------------------------------------------------------------
    def get_resources(self, resource_type, resource_name=None):
        filter_expr = Attr('profile').eq(super().get_env()) & Attr('resource_type').eq(resource_type)
        if resource_name:
            filter_expr = filter_expr &  Attr('resource_name').eq(resource_name)
        return super().get_dynamodb_resource().Table("aws_infra").scan(
            FilterExpression=filter_expr)['Items']


    # ------------------------------------------------------------------------------------
    # delete aws_infra items for specific module instance
    # ------------------------------------------------------------------------------------
    def delete_aws_infra(self, module=None, command=None, name=None):
        super().delete_infra_metadata(module, command, name)

    # ------------------------------------------------------------------------------------
    # export, import, promote metadata to another environment
    # ------------------------------------------------------------------------------------
    def export_metadata(self):
        source_env = super().get_env()
        source_profile = Profile(self.args).get_profile(source_env)
        source_metadata = AwsInfra(self.args).get_metadata(source_profile)
        with open(f"./config/environments/{source_env}_metadata.json", 'w') as f:
            json.dump(source_metadata, f, indent=2, default=self.json_converter)


    def import_metadata(self, source_env, target_env):
        # get source environment metadata
        metadata_file = f"./config/environments/{source_env}_metadata.json"
        with open(metadata_file, 'r') as f:
            filesize = os.path.getsize(metadata_file)
            if filesize == 0:
                self.logger.error()
                return

            metadata = json.load(f)

            # delete target env metadata
            self.delete_metadata(cmd_id='all')

            # go through each metadata table
            for table, data in metadata.items():
                if table == "property":
                    continue

                items = data['items']
                progress = Bar(f"    Importing {table} with {len(items)} items", max=len(items))

                for item in items:
                    try:
                        if 'cmd_id' in item:
                            item['cmd_id'] = f"{item['cmd_id']}_import"

                        # get metadata item as str
                        item_str = json.dumps(item, default=str)

                        # replace source env name with target env name
                        item_str = item_str.replace(source_env, target_env).replace(source_env.replace('_','-'), target_env.replace('_','-'))

                        # convert updated item str back to json
                        item = json.loads(item_str)

                        if table == 'aws_infra':
                            # remove empty arguments
                            c_args = {}
                            for k,v in item['command_arguments'].items():
                                if v is not None or v:
                                    c_args[k] = v
                            item['command_arguments'] = c_args
                        super().get_dynamodb_resource().Table(table).put_item(Item=item)

                        progress.next()

                    except Exception as e:

                        self.logger.error(e)
                        raise e

                progress.finish()

            # creating secrets (if applicable)
            secrets = super().get_secrets_client().list_secrets(
                MaxResults=100,
                Filters=[
                    {'Key': 'tag-key','Values': ['env']},
                    {'Key': 'tag-value','Values': [source_env]},
                ])
            # self.logger.info(json.dumps(secrets, indent=2, default=str))
            n = len(secrets['SecretList'])
            if secrets['SecretList']:
                progress = Bar(f"    Saving {n} secrets ", max=n)
                for secret in secrets['SecretList']:
                    env, resource_type, resource_name = secret['Name'].split('/')
                    super().save_password(target_env, resource_type, resource_name, '')
                    progress.next()
                progress.finish()

            return metadata


    # ------------------------------------------------------------------------------------
    # undo and redo command
    # ------------------------------------------------------------------------------------
    def undo_command(self):
        if self.args.id:
            ids = self.args.id
        elif self.args.arg_cmd_id:
            ids = self.args.arg_cmd_id

        for id in ids.split(","):
            id1 = id
            id = id.replace("_import","")
            self.logger.info(f"cmd_id: {id}")
            if id:
                timestamp = f"{id[0:4]}-{id[4:6]}-{id[6:8]} {id[8:10]}:{id[10:12]}:{id[12:14]}.{id[14:]}"
                self.logger.info(f"timestamp: {timestamp}")
                history = CommandHistory(self.args)
                cmd = history.get_command(timestamp)
                # self.logger.info(cmd)
                self.logger.info(f"Command to undo:\n{history.construct_command(cmd)['cmd']}\n")
                self.delete_metadata(cmd_id=id1)


    # ------------------------------------------------------------------------------------
    # undo and redo command
    # ------------------------------------------------------------------------------------
    def delete_metadata_tables(self):
        for table in self.metadata_tables:
            self.logger.info("deleting " + str(table) + "...")
            # self.create_metadata_table(table)


    # ------------------------------------------------------------------------------------
    # show aws_infra generated for command
    # ------------------------------------------------------------------------------------
    def get_aws_infra_for_command(self):
        if hasattr(self.args, 'id'):
            id = self.args.id
            timestamp = f"{id[0:4]}-{id[4:6]}-{id[6:8]} {id[8:10]}:{id[10:12]}:{id[12:14]}.{id[14:]}"
            history = CommandHistory(self.args)
            cmd = history.get_command(timestamp)
            self.logger.info("Command:")
            self.logger.info(history.construct_command(cmd)['cmd'])
            self.logger.info("")
            response = super().get_dynamodb_resource().Table('aws_infra').scan(FilterExpression=Attr('profile').eq(super().get_env()) & Attr('cmd_id').eq(id))['Items']
            for item in response:
                item.pop('command_arguments')
                self.logger.info(json.dumps(item, indent=2, default=self.json_converter))


    # ------------------------------------------------------------------------------------
    # aws resources
    # ------------------------------------------------------------------------------------
    def parse_arn(self, arn, res):
        arn = arnparse(arn)
        res['service'] = arn.service
        res['region'] = arn.region
        res['account_id'] = arn.account_id
        res['resource_type'] = arn.resource_type
        res['resource_name'] = arn.resource
        return res


    def get_tagged_resources(self, env_tag=None, managed_only=True):
        self.logger.info(f"getting tagged resources...: env_tag={env_tag}")
        if env_tag:
            tag_filters = [{'Key': 'env','Values': [env_tag]}]
        else:
            tag_filters = []

        resources = []
        pagination_token = ''
        while True:
            response = super().get_resourcegroupstaggingapi_client().get_resources(
                PaginationToken=pagination_token,
                TagFilters=tag_filters,
                ResourcesPerPage=100,
            )
            resources.extend(response['ResourceTagMappingList'])
            pagination_token = response['PaginationToken']
            if response['PaginationToken'] == '':
                break

        tagged_resources = []
        for res in resources:
            self.parse_arn(res['ResourceARN'], res)
            for tag in res['Tags']:
                res[f"tag.{tag['Key']}"] = tag['Value']
                if tag['Key'] == "Name":
                    res["resource_name"] = tag['Value']
            if not env_tag and managed_only:
                if 'tag.profile' in res and res['tag.profile'] == self.env or 'resource_name' in res and (self.env in res['resource_name'] or self.env.replace('_','-') in res['resource_name']):
                    res[f"tag.profile"] = self.env
                    del res['Tags']
                    tagged_resources.append(res)

        return tagged_resources


    def get_untagged_resources(self, managed_only=True):
        self.logger.info("getting untagged resources...")
        untagged = [
            # format: (resource_type, service, method, data_element, name, depth, arn)
            ("glue_catalog_database","glue","get_databases","DatabaseList","Name",0,None),
            ("lambda_layer","lambda","list_layers","Layers","LayerName",0,"LayerArn"),
            ("glue_crawler","glue","list_crawlers","CrawlerNames",None,0,None),
            ("glue_classifier","glue","get_classifiers","Classifiers","Name",1,None),
            ("kinesis_firehose_s3_delivery_stream","firehose","list_delivery_streams","DeliveryStreamNames",None,0,None),
            ("sns_topic","sns","list_topics","Topics",None,0,"TopicArn"),
            ("sns_topic_subscription","sns","list_subscriptions","Subscriptions",None,0,"SubscriptionArn")
        ]
        untagged_resources = []
        for resource_type, service, method, data, name, depth, arn in untagged:
            if self.args.x_acct_role_arn:
                boto3_client = super().get_boto3_session(x_acct_role_arn=self.args.x_acct_role_arn).client(service)
            else:
                boto3_client = super().get_boto3_session().client(service)
            # self.logger.info(f"{service}_client.{method}()")
            result = getattr(boto3_client, method)()
            # print(json.dumps(result,indent=2,default=str))
            for item in result[data]:
                if depth == 1:
                    item = list(item.values())[0]
                resource_name = item[name] if name is not None else None
                if resource_name is None and type(item) == str:
                    resource_name = item
                res = {
                    "service": service,
                    "resource_type": resource_type,
                    "resource_name": resource_name
                }
                resource_arn = item[arn] if arn is not None else None
                if resource_arn:
                    res["ResourceARN"] = resource_arn
                    self.parse_arn(res['ResourceARN'], res)

                if managed_only:
                    if res['resource_name'] and (super().get_env() in res['resource_name'] or super().get_env().replace('_','-') in res['resource_name']):
                        untagged_resources.append(res)

        return untagged_resources


    def get_aws_resources(self, env_tag=None, managed_only=True, result_as_dataframe=True):
        tagged = self.get_tagged_resources(env_tag, managed_only)
        untagged = self.get_untagged_resources(managed_only)
        all = tagged + untagged

        if self.args.verbose:
            res = []
            headers=["service","resource_type","resource_name","tag.profile"]
            all.sort(key=lambda x: x["service"])
            for item in all:
                item1 = []
                for col in headers:
                    item1.append(item[col] if col in item else "")
                res.append(item1)
            self.logger.info(tabulate(res, headers))

        if result_as_dataframe:
            return pd.DataFrame.from_dict(all)
        else:
            return all


    def get_existing_resources(self):
        env = self.env
        bucket = f"{env.replace('_','-')}-kc-big-data-tf-state"
        key = f"{env}/terraform.tfstate"
        existing_resources = {}

        try:
            obj = super().get_s3_resource().Bucket(bucket).Object(key=key).get()
            tf_state = json.loads(obj['Body'].read().decode('utf-8'))
        except Exception as e:
            self.logger.warn("terraform actions have not been executed yet for this env")
            tf_state = {"resources": []}

        # use this mapping for resources without ARN in "attributes"
        name_attrs = {
            "aws_dms_replication_instance": "replication_instance_id",
            "aws_dms_endpoint": "endpoint_id",
            "aws_autoscaling_group": "module"
        }

        # strip name suffix
        strip_suffix = {
            "aws_ecs_cluster": "-cluster"
        }

        for res in tf_state["resources"]:
            if res['type'] not in existing_resources:
                existing_resources[res['type']] = {}
                if self.args.verbose:
                    print(f"{res['type']}: {res['module'] if 'module' in res else ''}")

            # get name from tf "module" name
            if res['type'] in name_attrs and name_attrs[res['type']] == "module":
                name = name.replace("module.","").replace("_" + res['type'],"")
                existing_resources[res['type']][name] = {}

            elif "instances" in res:
                for inst in res["instances"]:
                    name = None
                    if "attributes" in inst:

                        if "tags" in inst["attributes"] and inst["attributes"]["tags"]:
                            # get name from "Name" tag
                            if inst["attributes"]["tags"] and "Name" in inst["attributes"]["tags"]:
                                name = inst["attributes"]["tags"]["Name"]

                        elif res['type'] in name_attrs:
                            # get name from custom mapping
                            name = inst["attributes"][name_attrs[res['type']]]

                        elif "arn" in inst["attributes"]:
                            # get name from arn
                            arn_parsed = self.parse_arn(inst["attributes"]["arn"], {})
                            name = arn_parsed['resource_name'].split(":")[0]

                        else:
                            # get name from "name"
                            name = res['name']

                    if name:
                        if res['type'] in strip_suffix:
                            name = name.replace(strip_suffix[res['type']], "")
                        existing_resources[res['type']][name] = {}
                        if "arn" in inst["attributes"]:
                            existing_resources[res['type']][name]['arn'] = inst["attributes"]["arn"]

        if self.args.verbose:
            with open(f"./testing/tf/terraform_state.json", 'w') as f:
                f.write(json.dumps(tf_state, indent=2, default=str))
            with open(f"./testing/tf/existing_resources.json", 'w') as f:
                f.write(json.dumps(existing_resources, indent=2, default=str))

        return existing_resources


    def show_status(self):
        if not self.env:
            return

        self.logger.info(f"refreshing status for {self.args.env}")
        env = self.env
        env_hyphen = env.replace('_','-')

        self.logger.info(f"aws_infra get existing resources")
        existing_resources = self.get_existing_resources()

        # use this for mapping RC resource type to TF resource type
        mapping = {
            "kms_key": "aws_kms_alias",
            "aurora_postgresql_instance": "aws_rds_cluster",
            "aurora_mysql_instance": "aws_rds_cluster",
            "rds_postgresql_instance": "aws_db_instance",
            "rds_mysql_instance": "aws_db_instance",
            "dms_s3_target_endpoint": "aws_dms_endpoint",
            "dms_source_endpoint": "aws_dms_endpoint",
            "kinesis_firehose_s3_delivery_stream": "aws_kinesis_firehose_delivery_stream",
            "lambda_layer": "aws_lambda_layer_version",
            "aws_ecs": "aws_ecs_cluster"
        }

        table = []
        with open(f"config/environments/{super().get_env()}_status.csv", 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Created","AWS Resource Type","Resource Name","Phase","Command", "ID"])

            # go through each aws_infra item
            for aws_infra_item in super().get_all_resources():
                # self.logger.info("show_status, get_all_resources")
                exists  = "no"
                res_type = aws_infra_item['resource_type']
                orig_type = res_type
                name = aws_infra_item['resource_name']

                # res_for_type will contain all resources for that type
                res_for_type = {}
                if res_type in mapping:
                    res_type = mapping[res_type]
                if "aws_" + res_type in existing_resources:
                    res_for_type = existing_resources["aws_" + res_type]
                elif res_type in existing_resources:
                    res_for_type = existing_resources[res_type]

                if res_for_type:
                    # "kc_100_qa_pause-resume-test-cluster"
                    names = [
                        name,
                        name.replace('_','-'),
                        env,
                        env + "_" + name,
                        env + "-" + name,
                        env_hyphen + "-" + name,
                        (env + "_" + name).replace('_','-'),
                        env_hyphen + "_" + name,
                        env_hyphen + "_" + name.replace('_','-'),
                        env + "_" + orig_type + "_" + name,
                        (env + "_" + orig_type + "_" + name).replace('_','-'),
                        env_hyphen + "_" + orig_type + "_" + name,
                        env_hyphen + "_" + orig_type + "_" + name.replace('_','-'),
                        env + "-" + name + "-" + orig_type,
                        (env + "-" + name + "-" + orig_type).replace('_','-'),
                        env + "_" + name + "_" + orig_type
                    ]
                    for name_ in names:
                        if name_ in res_for_type:
                            exists = "yes"

                            break
                if self.args.verbose:
                    print(f"{exists}: {orig_type}::{name}")

                phase = aws_infra_item['phase'] if 'phase' in aws_infra_item else ''
                command = aws_infra_item['command'] if 'command' in aws_infra_item else ''
                cmd_id = aws_infra_item['cmd_id']
                table.append([exists, orig_type, name, f"kc {phase} {command}", cmd_id])
                csv_writer.writerow([exists, orig_type, name, phase, command, cmd_id])

            if not self.args.quiet:
                print(f"\n\n{colors.OKBLUE}Following resources are currently part of your environment architecture.\n`Created` column indicates whether resource was created in your AWS account.{colors.ENDC}\n")
                headers=["In AWS","Resource Type","Resource Name","Command","ID"]
                print(f"{tabulate(sorted(table), headers)}\n")

    # ------------------------------------------------------------------------------------
    # create metadata table as part of `kc init create-env`
    # ------------------------------------------------------------------------------------
    def create_metadata_table(self, table):
        # [name,pk,sk,create]
        # ex: ["source_column","table","column",True]
        # ex: ["rule","fqn","",True],
        table_name = table[0]

        pk = table[1]
        if table[2] != "":
            sk = table[2]
            key_schema = [
                {'AttributeName': pk,'KeyType': 'HASH'},
                {'AttributeName': sk,'KeyType': 'RANGE'}
            ]
            attr_defs = [
                {'AttributeName': pk,'AttributeType': 'S'},
                {'AttributeName': sk,'AttributeType': 'S'},
            ]
        else:
            key_schema = [
                {'AttributeName': pk,'KeyType': 'HASH'}
            ]
            attr_defs = [
                {'AttributeName': pk,'AttributeType': 'S'}
            ]

        try:
            response = super().get_dynamodb_resource().create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attr_defs,
                BillingMode='PAY_PER_REQUEST'
                # ProvisionedThroughput={'ReadCapacityUnits': 1,'WriteCapacityUnits': 1}
                # DeletionProtectionEnabled=True
            )
            self.logger.debug(response)
        except Exception as e:
            self.logger.debug(table_name + " already exists")


    def enable_cloudwatch_event_rules(self):
        schedules = Schedule(self.args).get_all_schedules()
        for schedule in schedules:
            event_rule_name = schedule['task'] + '_cloudwatch_event_rule'
            print(f"\tactivating {event_rule_name}")
            response = super().get_events_client().enable_rule(
                Name=event_rule_name
            )
            self.logger.debug(response)


    # ------------------------------------------------------------------------------------
    # add custom resources directly to aws_infra
    # ------------------------------------------------------------------------------------
    def add_glue_job(self, name=None):
        if name is None:
            name = self.args.name
        params = super().get_glue_job_params(name, self.args.job_type)
        item = super().add_aws_resource('glue_job', name, params)
        item['module'] = "aws"
        super().build_metadata_item(item, "metadata", name)

        # upload Glue job template to S3
        template = "./data_scripts/job_templates/kc_custom_glue_job_template.py"
        bucket = f"{self.get_env().replace('_','-')}-glue-scripts"
        key = f"{name}.py"

        self.logger.info(f"uploading Glue script to {params['command']['script_location']}")
        super().get_s3_client().upload_file(template, bucket, key)


    def add_kinesis_stream(self, name=None):
        if name is None:
            name = self.args.name
        super().add_aws_resource('kinesis_stream', name, {})


    def add_msk_cluster(self, name=None):
        if name is None:
            name = self.args.name
        super().add_aws_resource('msk_cluster', name, {})


    def create_ingestion_folder(self, dataset):
        bucket = f"{dataset['profile'].replace('_','-')}-ingestion"
        folder = f"semistructured/{dataset['name']}"
        results = super().get_s3_client().list_objects(Bucket=bucket, Prefix=folder)
        if "Contents" not in results:
            self.logger.info(f"Creating S3 folder: s3://{bucket}/{folder}")
            super().get_s3_client().put_object(Bucket=bucket, Key=(folder + '/empty_file'))
        else:
            self.logger.info(f"S3 folder already exists: s3://{bucket}/{folder}")


    def upload_glue_code(self, job_name, local_script):
        bucket = f"{super().get_env().replace('_','-')}-glue-scripts"
        s3_key = f"{job_name}.py"
        self.logger.info(f"deploying Glue job script: s3://{bucket}/{s3_key}")
        super().get_s3_client().upload_file(local_script, bucket, s3_key)


