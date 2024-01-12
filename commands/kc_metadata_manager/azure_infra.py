
import csv
import json
import logging
import os
from commands.colors import colors
from tabulate import tabulate

from commands.kc_metadata_manager.azure_metadata import Metadata
from server.utils.azure_environment_utils import AzureConfigUtils
from terraform.bin import kctf


class AzureInfra(Metadata):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)

    metadata_tables = [
        ["kc_activation","email","",False,True],
        ["command_history","timestamp","",False,False],
        ["command","profile","step",True,True],
        ["profile","name","",False,False],
        ["log","profile","timestamp",True,False],
        ["property","profile","name",False,False],
        ["azure_infra","fqn","",True,True],
        ["metadata","profile","fqn",True,True],
    ]

    # ------------------------------------------------------------------------------------
    # this is done once as part of `kc activate` to generate metadata tables
    # ------------------------------------------------------------------------------------
    def create_metadata_tables(self):
        db = super().create_or_get_rc_database()
        containers = super().list_metadata_containers(db)

        self.logger.debug(f"{len(containers)} tables")
        self.logger.debug(json.dumps(containers, indent=2))

        existing_tables = []
        for container in containers:
            existing_tables.append(container['id'])

        # Create metadata tables if they don't exist
        for table in self.metadata_tables:
            if table[0] not in existing_tables:
                self.logger.info("Creating " + str(table) + "...")
                super().create_or_get_metadata_container(db, table[0], table[1], table[2])

    def create_tf_state(self):
        # TF state bucket and table
        tf_state = f"tfstate_{super().get_env().replace('-','_')}"
        self.metadata_tables.append([tf_state, "LockID", "", True, False])
        self.logger.info(f"creating storage account - tfstate")

        try:
            tfstorage = f'kcrcaztfstate{super().get_args().env_suffix}'
            super().create_storage_account(tfstorage, super().get_env().replace('_','-'))
        except Exception as e:
            self.logger.info(e)

        try:
            # Create TF state table
            db = super().create_or_get_rc_database()
            self.create_or_get_metadata_container(db, tf_state, "LockID", "")
        except Exception as e:
            self.logger.info(e)
        
    def exec_tf_action(self, action, subscription_tier, no_prompt):
        env = self.get_env()
        creds = AzureConfigUtils.get_azure_creds(env)
        os.environ['ARM_CLIENT_ID'] = creds["client_id"] 
        os.environ['ARM_CLIENT_SECRET'] = creds["client_secret"]
        os.environ['ARM_TENANT_ID'] = creds["tenant_id"] 
        os.environ['ARM_SUBSCRIPTION_ID'] = creds["subscription_id"] 
        os.environ['terraform_dir'] = os.getcwd() + "/terraform/"
        self.logger.info(f"ARM_SUBSCRIPTION_ID={os.environ['ARM_SUBSCRIPTION_ID']}")
        
        items = self.get_all_resources()

        profile_details = self.get_item_by_key("profile", env)
        profile_details['name_dashed'] = profile_details['name'].replace('_', '-')
        kctf.main(self.args, profile_details, items, env, action, subscription_tier, no_prompt)

    def get_existing_resources(self):
        env = super().get_env()
        config = AzureConfigUtils.get_azure_environment_config(env)
        tf_storage_account = f"kcrcaztfstate{config.get('env_suffix')}"
        container = env.replace('_','-')
        key = "terraform.tfstate"
        existing_resources = {}

        try:
            tf_state = self.get_container_item(tf_storage_account, container, key)
        except Exception as e:
            print (e)
            self.logger.warn("terraform actions have not been executed yet for this env")
            tf_state = {"resources": []}

        # use this mapping for resources without ARN in "attributes"
        name_attrs = {
        }

        # strip name suffix
        strip_suffix = {
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

                        elif "name" in inst["attributes"]:
                            # get name from arn
                            name = inst["attributes"]["name"]

                        else:
                            # get name from "name"
                            name = res['name']

                    if name:
                        if res['type'] in strip_suffix:
                            name = name.replace(strip_suffix[res['type']], "")
                        existing_resources[res['type']][name] = {}

        if self.args.verbose:
            with open(f"./testing/tf/terraform_state.json", 'w') as f:
                f.write(json.dumps(tf_state, indent=2, default=str))
            with open(f"./testing/tf/existing_resources.json", 'w') as f:
                f.write(json.dumps(existing_resources, indent=2, default=str))

        return existing_resources


    def show_status(self):
        if not self.env:
            return

        self.logger.info(f"refreshing status for azure environment {self.args.env}")
        env = self.env
        env_hyphen = env.replace('_','-')

        existing_resources = self.get_existing_resources()

        # use this for mapping RC resource type to TF resource type
        mapping = {
            "aks_cluster": "azurerm_kubernetes_cluster",
            "aks_node_pool": "azurerm_kubernetes_cluster_node_pool",
            "container_app_cert": "azurerm_container_app_environment_certificate",
            "container_app_env": "azurerm_container_app_environment",
            "az_file_share": "azurerm_storage_share",
            "az_blob_container": "azurerm_storage_container"
        }

        table = []
        with open(f"config/environments/{super().get_env()}_status.csv", 'w', newline='') as file:
            csv_writer = csv.writer(file)
            headers=["In Azure","Resource Type","Resource Name","Module","Command","ID"]
            csv_writer.writerow(headers)

            # go through each azure_infra item
            for azure_infra_item in self.get_all_resources():
                exists  = "no"
                res_type = azure_infra_item['resource_type']
                orig_type = res_type
                name = azure_infra_item['resource_name']

                # res_for_type will contain all resources for that type
                res_for_type = {}
                if res_type in mapping:
                    res_type = mapping[res_type]
                if "azurerm_" + res_type in existing_resources:
                    res_for_type = existing_resources["azurerm_" + res_type]
                elif res_type.replace("az_", "azurerm_") in existing_resources:
                    res_for_type = existing_resources[res_type.replace("az_", "azurerm_")]
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

                phase = azure_infra_item['phase'] if 'phase' in azure_infra_item else ''
                command = azure_infra_item['command'] if 'command' in azure_infra_item else ''
                cmd_id = azure_infra_item['cmd_id']
                table.append([exists, orig_type, name, f"kc {phase} {command}", cmd_id])
                csv_writer.writerow([exists, orig_type, name, phase, command, cmd_id])

            if not self.args.quiet:
                print(f"\n\n{colors.OKBLUE}Following resources are currently part of your environment architecture.\n`In Azure` column indicates whether resource was created in your Azure subscription.{colors.ENDC}\n")
                headers=["In Azure","Resource Type","Resource Name","Module","Command","ID"]
                print(f"{tabulate(sorted(table), headers)}\n")

