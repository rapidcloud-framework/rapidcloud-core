__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging

from google.cloud import firestore
from google.cloud.firestore_v1.document import DocumentReference, DocumentSnapshot
from google.cloud.firestore_v1.base_query import FieldFilter
# from google.cloud.firestore_v1.base_query import BaseCompositeFilter
# from google.cloud.firestore_v1.types import StructuredQuery

from commands.kc_metadata_manager.cloud_metadata import CloudMetadata
from commands.kc_metadata_manager.profile_manager import get_profile_manager
from commands import print_utils


class Metadata(CloudMetadata):

    CLOUD = "gcp"
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args, self.CLOUD)
        self.args = args
        self.setup_sdk()
        # self.save_history()


    def setup_sdk(self):
        pass # Nothing special to set up.


    def add_infra_resource(self, type: str, name: str, params: dict={}, name_separator: str="_", custom: bool=False, role_name: str=None, fqn: str=None) -> dict:
        item = super().build_infra_item(type, name, params, name_separator, custom, role_name, fqn)
        self.put_item('gcp_infra', item)
        return item


    def delete_infra_metadata(self, module: str=None, command: str=None, name: str=None) -> None:
        # raise RuntimeError("delete_infra_metadata is not implemented")
        if self.args.composite_module:
            return

        if not module:
            module = self.args.module
        if not command:
            command = self.args.command
        if not name:
            name = self.args.name

        extra_filters = {"module":f"{module}_{command}_{name}"}
        items = self.get_all_resources(extra_filters=extra_filters)
        for item in items:
            doc_id = self.get_item_primary_key(item)
            self.delete_item("gcp_infra", doc_id)


    def build_metadata_item(self, metadata: dict, metadata_table: str, name: str=None, args: dict={}, save: bool=True) -> dict:
        item = super().build_metadata_item(metadata, name, args)
        if save:
            self.logger.info(f"saving metadata item {item['fqn']}")
            self.put_item(metadata_table, item)
        return item


    def get_metadata_item(self, module: str, command: str, name: str) -> dict:
        raise RuntimeError("get_metadata_item is not implemented")
        fqn = self.get_metadata_fqn(module, command, name)
        # TODO
        # items = self.get_dynamodb_resource().Table('metadata').query(
        #     KeyConditionExpression=Key('profile').eq(self.get_env()) & Key('fqn').eq(fqn)
        # )['Items']
        # if len(items) > 0:
        #     return items[0]
        # else:
        #     return None


    # def get_modules(self, module: str = None, command: str = None, name: str = None) -> list[dict]:
    #     filters = {"profile": self.get_env()}
    #     if module:
    #         filters["module"] = module
    #         if command is not None:
    #             filters["command"] = command
    #         if name is not None:
    #             filters["name"] = name

    #     result = self.search_items("metadata", filters)
    #     return result


    def get_modules(self, module: str = None, command: str = None, name: str = None) -> list[dict]:
        doc_id = self.get_metadata_fqn(module, command, name)
        doc = self.get_doc_by_id("metadata", doc_id)

        if doc.exists:
            # The caller (commands/modules/__init__.py:exec()) only needs the 1st element of this arrary.
            # Right here, we have only 1 element anyway because we've designed GCP Firebase to use the doc_id as the Document's (unique) name.
            # But in a more general scenario (e.g., AWS DynamoDB) where the database product has a different structure,
            # there potentially could have multiple records matching the search criteria.
            result = [doc.to_dict()]
        else:
            result = []

        return result


    def get_doc_by_id(self, collection_name: str, doc_id: str) -> DocumentSnapshot:
        result = self.get_metadata_root().collection(collection_name).document(doc_id).get()
        return result


    def get_all_resources(self, table_name="gcp_infra", extra_filters=None, ignore_env_filter=False):
        filters = {}
        if extra_filters:
            filters = extra_filters

        if not ignore_env_filter and not "profile" in filters:
            filters['profile'] = self.get_env()

        return self.search_items(table_name, filters)


    def search_items(self, collection_name: str, filters: dict = None) -> list[dict]:
        col_ref = self.get_metadata_root().collection(collection_name)

        # Amazingly, it's hard to find on the internet some straight-forward sample code
        # to do a composite query, i.e., match across multiple fields with AND/OR Boolean connectors.
        #
        # I tried unsuccessfully to combine the following:
        #   - https://stackoverflow.com/questions/76110267/firestore-warning-on-filtering-with-positional-arguments-how-to-use-filter-kw
        #   - https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/firestore/cloud-client/query_filter_or.py
        #   - https://cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.base_query.BaseCompositeFilter (horrible write-up)
        #   - https://github.com/googleapis/python-firestore/blob/dd977226ef95420e22bd51e1073c7a0878a3da93/google/cloud/firestore_v1/types/query.py#L259
        #
        #         ff_list = []
        #         if filters:
        #             for each_key in filters:
        #                 val = str(filters[each_key]).lower() if type(filters[each_key]) is bool else str(filters[each_key])
        #                 ff_list.append(FieldFilter(each_key, '==', val))
        #         bcf = BaseCompositeFilter(StructuredQuery.CompositeFilter.Operator.AND, ff_list) ## This somehow doesn't filter the correct output -- see my comment about Enum at https://stackoverflow.com/questions/76110267/firestore-warning-on-filtering-with-positional-arguments-how-to-use-filter-kw
        #         col_ref.where(filter=bcf)
        #
        # Finally, this worked:
        #   - https://cloud.google.com/firestore/docs/query-data/queries#compound_and_queries
        query = col_ref
        if filters:
            for each_key in filters:
                val = str(filters[each_key]).lower() if type(filters[each_key]) is bool else str(filters[each_key])
                query = query.where(filter=FieldFilter(each_key, '==', val))

        result = []
        docs = query.stream() # https://github.com/googleapis/python-firestore/blob/dd977226ef95420e22bd51e1073c7a0878a3da93/google/cloud/firestore_v1/base_query.py#L997
        for doc in docs:
            item = doc.to_dict()
            self.logger.debug(f'search_items(): doc.id={doc.id} => {item}')
            result.append(item)

        return result


    def get_metadata_root(self) -> DocumentReference:
        # https://cloud.google.com/firestore/docs/create-database-server-client-library#initialize
        # https://cloud.google.com/firestore/docs/samples/firestore-setup-client-create-with-project-id?hl=en
        client = firestore.Client(project=get_profile_manager().get_env_project_id())
        # client = firestore.Client()
        self.logger.debug("get_metadata_root(): client.project='{client.project}'") # https://cloud.google.com/python/docs/reference/google-cloud-core/latest/config

        # A CollectionReference or DocumentReference is returned whether the underlying collection or document exists or not.
        root_doc_ref = client.collection('rapid_cloud_metadata').document('rc_metadata_collections')

        # https://stackoverflow.com/questions/51483234/how-to-know-if-document-exists-in-firestore-python
        root_doc = root_doc_ref.get()

        if not root_doc.exists:
            print_utils.info(f"RapidCloud metadata: GCP Firestore root document doesn't yet exist. Creating...")
            # Although it's not mandatory for this parent (root) document to exist in order to later create child documents,
            # it's simply nice-to-have to make it exist; otherwise, it can be confusing for a casual observer.
            # Non-existent parent document is explained at:
            #    https://cloud.google.com/firestore/docs/using-console#non-existent_ancestor_documents
            root_doc_ref.set({})

        return root_doc_ref


    # def list_metadata_tables(self):
    #     existing_tables = []
    #     db = firestore.Client()
    #
    #     # https://stackoverflow.com/questions/58224509/how-to-know-what-collections-i-have-in-firestore-using-python-api/76017187#76017187
    #     cols = db.collections()
    #     for c in cols:
    #         existing_tables.append(c.id)
    #
    #     return existing_tables


    def get_item_primary_key(self, item: dict) -> str:
        if item.get('id'):
            return item.get('id')

        if item.get('fqn'):
            return item.get('fqn')

        raise RuntimeError("Cannot build primary key for item={item}")


    def put_item(self, table: str, item: dict) -> None:
        if self.args.verbose:
            self.logger.info(table)
            self.logger.info(json.dumps(item, indent=2, default=str))

        if hasattr(self.args, 'cmd_id'):
            item['cmd_id'] = self.args.cmd_id

        doc_id = self.get_item_primary_key(item)

        # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/372cf0dc431c9efc3865a3f735fe4e01f4741eaf/firestore/cloud-client/snippets.py#L42
        response = self.get_metadata_root().collection(table).document(doc_id).set(item)
        self.logger.info(f"Updated collection '{table}' with doc_id='{doc_id}'")
        self.logger.debug(response)


    def delete_item(self, table: str, doc_id: str = None) -> None:
        assert doc_id, f"doc_id cannot be empty in delete_item() for table='{table}'"

        self.logger.info(f"Deleting Firestore doc_id='{doc_id}' in collection='{table}' ...")

        # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/372cf0dc431c9efc3865a3f735fe4e01f4741eaf/firestore/cloud-client/snippets.py#L789-L793
        response = self.get_metadata_root().collection(table).document(doc_id).delete()

        self.logger.debug(response)


    def get_role(self, resource: str) -> str:
        return None
