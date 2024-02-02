__author__ = "Sridhar K"
__license__ = "MIT"


import json
import logging
import azure.cosmos.exceptions as exceptions
import azure.cosmos.documents as documents

from dotenv import load_dotenv
from commands import colors
from commands.kc_metadata_manager.cloud_metadata import CloudMetadata
from azure.identity import DefaultAzureCredential
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from server.utils.azure_environment_utils import AzureConfigUtils

class Metadata(CloudMetadata):
    
    CLOUD = "azure"
    RESOURCE_GROUP = "rapidcloud_rg"
    COSMOSDB_ACCT_NAME = "rapidcloud-cosmos-db"
    COSMOSDB_DB_NAME = "rapidcloud"
    logger = logging.getLogger(__name__)

    azurelogger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
    azurelogger.setLevel(logging.WARNING)

    def __init__(self, args):
        super().__init__(args, self.CLOUD)
        load_dotenv(".env")
        self.args = args
        success = self.setup_sdk()
        # if success:
        #     success = self.load_profile()
        # if success:
        #     self.save_history()
        if self.get_mode() == "cli" and not self.get_env():
            print(f"You don't have a current environment. Run this command:\n{colors.OKBLUE}kc init set-env --env [your_env_name]{colors.ENDC}\n")
            return False
        # self.save_history()


    def setup_sdk(self):        
        sub = self.get_subscription()
        cosmosdb_mgmt_client = CosmosDBManagementClient(DefaultAzureCredential(),sub)

#if not exists
        #cosmosdbresource = cosmosdb_mgmt_client.database_accounts.begin_create_or_update(self.RESOURCE_GROUP, self.COSMOSDB_ACCT_NAME, DatabaseAccountCreateUpdateParameters(locations=['eastus'],enable_free_tier=True))
        database_account = cosmosdb_mgmt_client.database_accounts.begin_create_or_update(
            self.RESOURCE_GROUP,
            self.COSMOSDB_ACCT_NAME,
            {
                "location": self.get_region(),
                "database_account_offer_type": "Standard",
                "enable_automatic_failover": False,
                "capacity": {
                    "total_throughput_limit": 1000
                },
                "enable_free_tier": True
            }
        ).result()
        database_account_keys = cosmosdb_mgmt_client.database_accounts.list_keys(
            self.RESOURCE_GROUP,
            self.COSMOSDB_ACCT_NAME
        )
        self.cosmosdb_uri = database_account.document_endpoint
        self.cosmosdb_key = database_account_keys.primary_master_key
        
        #print(f"Cosmos DB URI: {self.cosmosdb_uri}")
        #print(f"Cosmos DB Key: {self.cosmosdb_key}")
        self.cosmosdb_client = self.get_cosmos_client()
   
    def get_subscription(self):
        if not self.args is None and hasattr(self.args, "subscription") and not self.args.subscription is None:
            return self.args.subscription
        else:
            profile = AzureConfigUtils.get_azure_profile()
            return profile["subscription"]

    def get_cosmos_client(self):
        client = CosmosClient(self.cosmosdb_uri, {'masterKey': self.cosmosdb_key})
        return client

    def create_resource_group(self, rg_name=None):
        if rg_name is None:
            rg_name = self.RESOURCE_GROUP
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, self.get_subscription())

        resource_client.resource_groups.create_or_update(rg_name, { "location": self.get_region() })

    def create_storage_account(self, storage_name, container, throw_if_exists=False):
        credential = DefaultAzureCredential()
        storage_client = StorageManagementClient(credential, self.get_subscription())

        availability_result = storage_client.storage_accounts.check_name_availability(
            { "name": storage_name }
        )

        if not availability_result.name_available:
            if throw_if_exists:
                raise Exception(f"Storage name {storage_name} is already in use.")
            print(f"Storage name {storage_name} is already in use. Skipping creation...")
        else:
            # The name is available, so provision the account
            poller = storage_client.storage_accounts.begin_create(self.RESOURCE_GROUP, storage_name,
                {
                    "location" : self.get_region(),
                    "kind": "StorageV2",
                    "sku": {"name": "Standard_LRS"}
                }
            )
            account_result = poller.result()

        storage_client.blob_containers.create(self.RESOURCE_GROUP, storage_name, container, {})


    def create_or_get_rc_database(self):
        try:
            db = self.cosmosdb_client.create_database_if_not_exists(id=self.COSMOSDB_DB_NAME, offer_throughput=1000)
            return db
        except exceptions.CosmosResourceExistsError:
            self.logger.error(f'A database with id \'{self.COSMOSDB_DB_NAME}\' read or creation failed')

    def read_database(self, id):
        try:
            database = self.cosmosdb_client.get_database_client(id)
            #database.read()
            return database

        except exceptions.CosmosResourceNotFoundError:
            self.logger.error('A database with id \'{0}\' does not exist'.format(id))

    def create_or_get_metadata_container(self, db, id, pk, sk):
        try:
            if str(sk or ''):
                container_definition = {
                    "id": id,
                    "indexingPolicy": {
                        'includedPaths': [
                            {
                                'path': '/{0}/?'.format(sk),
                                'indexes': [
                                    {
                                        'kind': documents.IndexKind.Range,
                                        'dataType': documents.DataType.String,
                                        'precision': -1
                                    }
                                ]
                            },
                            {
                                'path': '/*'
                            }
                        ]
                    }
                }
                container = db.create_container(
                    id=container_definition['id'],
                    partition_key=PartitionKey(path=f"/{pk}"),
                    indexing_policy=container_definition['indexingPolicy']
                )
            else:
                container = db.create_container(
                id=id,
                partition_key=PartitionKey(path=f"/{pk}")
            )
            self.logger.debug(container)
            properties = container.read()
            self.logger.debug('Container with id \'{0}\' created'.format(container.id))
            self.logger.debug('IndexPolicy Mode - \'{0}\''.format(properties['indexingPolicy']['indexingMode']))
            self.logger.debug('IndexPolicy Automatic - \'{0}\''.format(properties['indexingPolicy']['automatic']))

            return container        
        except exceptions.CosmosResourceExistsError:
            return db.get_container_client(id)
        except exceptions.CosmosHttpResponseError:
            raise

    def list_metadata_containers(self, db):
        containers = list(db.list_containers())

        if not containers:
            return []
        return containers

    def put_item(self, table, item):
        if self.args.verbose:
            self.logger.info(table)
            self.logger.info(json.dumps(item, indent=2, default=str))
        if hasattr(self.args, 'cmd_id'):
            item['cmd_id'] = self.args.cmd_id
        
        response = self.get_container(table).upsert_item(body=item)
        self.logger.debug(f"updated metadata [{table}]")
        self.logger.debug(json.dumps(response, indent=2))

    def get_container(self, id):
        try:
            db = self.read_database(self.COSMOSDB_DB_NAME)
            container = db.get_container_client(id)
            container.read()
            #self.logger.debug('Container with id \'{0}\' was found, it\'s link is {1}'.format(container.id, container.container_link))
            return container

        except exceptions.CosmosResourceNotFoundError:
            self.logger.error('A container with id \'{0}\' does not exist'.format(id))
            return False

    def get_container_item(self, storage_account, container, item):
        account_url = f"https://{storage_account}.blob.core.windows.net"
        blob_service_client = BlobServiceClient(account_url, credential=DefaultAzureCredential())
        blob_client = blob_service_client.get_blob_client(container=container, blob=item)

        streamdownloader = blob_client.download_blob()
        item_json = json.loads(streamdownloader.readall())
        return item_json

    def get_item_by_key(self, table, key):
        try:
            container = self.get_container(table)
            response = container.read_item(item=key, partition_key=key)
            return response
        
        except exceptions.CosmosResourceNotFoundError:
            self.logger.error(f'A item with key \'{key}\' does not exist in table {table}')
            return None

    def search_items(self, table, and_filters=None, or_filters=None):
        query = f"SELECT * FROM {table} s"
        self.logger.info(f"query (before filters): {query}")
        self.logger.info(f"and_filters: {and_filters}")
        self.logger.info(f"or_filters: {or_filters}")

        if and_filters:
            query += " where " + " and ".join(
                "s." + str(each_key) + ("=" + str(and_filters[each_key]).lower() if type(and_filters[each_key]) is bool else "='" + str(and_filters[each_key]) + "'")
                for each_key in and_filters
            )

        if or_filters:
            if and_filters: query += " and ((" 
            else: query += " where (("
            j = 0
            for dict in or_filters:
                if j > 0: 
                    query += ") or ("
                query += " and ".join(
                    "s." + str(each_key) + ("=" + str(dict[each_key]).lower() if type(dict[each_key]) is bool else "='" + str(dict[each_key]) + "'")
                    for each_key in dict
                )
                j = j+1
            query += "))"

        self.logger.info(f"query: {query}")

        container = self.get_container(table)
        items = container.query_items(query=query, enable_cross_partition_query=True)

        return list(items)

    def delete_item(self, table, id, partitionkey):
        container = self.get_container(table)
        container.delete_item(item=id, partition_key=partitionkey)

### ---------- PROFILE ---------- ###

    # def load_profile(self):
    #     if self.env and self.args.feature not in ('init', 'activate') and self.args.command != 'promote':
    #         self.logger.info(f"env={self.env}")
    #         try:
    #             self.profile = self.get_dynamodb_resource().Table('profile').get_item(Key={'name': self.env})['Item']
    #             setattr(self.args, 'env', self.env)
    #             setattr(self.args, 'datalake', self.profile['datalake'])
    #             setattr(self.args, 'data_lake_fqn', self.profile['datalake'])
    #             setattr(self.args, 'output_folder_path', './src/')
    #             setattr(self.args, 'aws_region', self.profile['region'])
    #             setattr(self.args, 'aws_profile', self.aws_profile)
    #             return True
    #         except Exception as e:
    #             self.logger.error(e)
    #             return False


### ---------- AZURE_INFRA ---------- ###

    def add_infra_resource(self, type, name, params={}, name_separator="_", custom=False, role_name=None, fqn=None):
        return self.add_azure_resource(type, name, params, name_separator, custom, role_name, fqn) 

    def add_azure_resource(self, type, name, params={}, name_separator="_", custom=False, role_name=None, fqn=None):
        item = super().build_infra_item(type, name, params, name_separator, custom, role_name, fqn)
        self.put_item('azure_infra', item)
        
        self.logger.info(f"saved {type}:{name.replace('_',name_separator)} in azure_infra, role={role_name}")
        return item 

    def get_azure_infra_for_command(self, cmd_id):
        pass

    def get_role(self, resource):
        pass

    def get_all_resources(self, table_name="azure_infra", extra_filters=None, ignore_env_filter=False):
        filters = {}
        if extra_filters:
            filters = extra_filters

        if not ignore_env_filter and not "profile" in filters:
            filters['profile'] = self.get_env()
        
        return self.search_items(table_name, filters)

    def delete_infra_metadata(self, module=None, command=None, name=None):
        if self.args.composite_module:
            return
            
        if not module:
            module = self.args.module
        if not command:
            command = self.args.command
        if not name:
            name = self.args.name
        
        self.logger.info(f"deleting azure_infra items for {module}_{command}_{name}")
        extra_filters = {"module":f"{module}_{command}_{name}"}
        items = self.get_all_resources(extra_filters=extra_filters)
        for item in items:
            self.delete_item("azure_infra", item.get("id"), item.get("fqn"))


    def build_metadata_item(self, metadata, metadata_table, name=None, args={}, save=True):
        item = super().build_metadata_item(metadata, name, args)
        if save:
            self.logger.info(f"saving metadata item {item['fqn']}")
            self.put_item(metadata_table, item)
        return item


    def get_metadata_item(self, module, command, name):
        fqn = f"{self.get_env()}_{module}_{command}_{name}"
        extra_filters = {"profile":self.get_env(), "fqn":fqn}
        return self.search_items("metadata", extra_filters)


    def get_modules(self, module=None, command=None, name=None):
        filters = {"profile": self.get_env()}
        if module:
            filters["module"] = module
            if command is not None:
                filters["command"] = command
            if name is not None:
                filters["name"] = name

        return self.search_items("metadata", filters)


    def set_default_properties(self):
        pass
