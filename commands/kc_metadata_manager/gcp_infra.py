
import json
import logging
import os

from google.cloud import storage

from commands.kc_metadata_manager.gcp_metadata import Metadata
from commands.kc_metadata_manager.gcp_profile import Profile
from commands.kc_metadata_manager.profile_manager import get_profile_manager
from commands import print_utils

from terraform.bin import kctf

class GcpInfra(Metadata):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)

    # metadata_tables = [
    #     ["kc_activation","email","",False,True],
    #     ["command_history","timestamp","",False,False],
    #     ["command","profile","step",True,True],
    #     ["profile","name","",False,False],
    #     ["log","profile","timestamp",True,False],
    #     ["property","profile","name",False,False],
    #     ["azure_infra","fqn","",True,True],
    #     ["metadata","profile","fqn",True,True],
    # ]

    def setup_sdk(self):
        pass

    # For GCP, this method is unnecessary (and therefore shouldn't be called) because:
    #  -  GCP Firestore isn't like AWS DynamoDB or RDBMS. Firestore doesn't need a table (i.e., collection)
    #     to be created in advance before a record (i.e., document) can be inserted into it.
    #     In Firestore, inserting a (sub)document (even if an empty document like "{}") or a subcollection
    #     automatically causes all parent collections/documents to be created (if they don't currently exist.)
    def create_metadata_tables(self):
        raise RuntimeError("This method shouldn't have been called.")

        # root_doc_ref = super().get_metadata_root();

        # # We insert a dummy marker for now in order to create the nested data structure in Firestore.
        # # This isn't actually necessary but serves to at least verify that we have WRITE permission in Firestore.
        # # Individual subcollection and subdocs will be created in "lazy initialization" fashion later
        # # because Firestore doesn't need an empty (sub)collection to be created before inserting documents into it.
        # # Inserting a (sub)document (even if an empty document like "{}") or a subcollection automatically causes all
        # # parent collections/documents to be created (if they don't currently exist.) Think of it as
        # # the Linux command "mkdir -p ...".
        # # This is unlike a relational database or AWS DynamoDB where an empty table needs to be created
        # # in advance before rows/items can be inserted into it.
        # #
        # # Also, because we're passing the 'merge=True' flag below, we wouldn't need to test for 'root_doc.exists';
        # # The entire if-else branching logic becomes unnecessary; however, we keep it for readability for
        # # those who're not familiar with Firestore programming.
        # root_doc_ref.set({}, merge=True) # https://cloud.google.com/firestore/docs/manage-data/add-data#set_a_document


        # root_collection.document('my-rc-doc-1').set({
        #     "name": "John Smith",
        #     "tel": "1-416-222-3333",
        #     "postal_code": "M2L 3C3"
        # })

        # print_utils.info(f"result: {result}")

        # self.logger.debug(f"{len(existing_tables)} existing tables: ")
        # self.logger.debug(' '.join(existing_tables))

        # for table in self.metadata_tables:
        #     if table[0] not in existing_tables:
        #         self.logger.info("Creating " + str(table) + "...")
        #         self.create_metadata_table(table)

    # ------------------------------------------------------------------------------------
    # this is done once as part of `kc init create-env` to generate Terraform state info
    # ------------------------------------------------------------------------------------
    def create_tf_state(self) -> storage.Bucket:
        # For some reason, it's unnecessary to enable the "storage-api.googleapis.com" API (or any "storage*.googleapis.com" API)
        # before creating a bucket.

        # Unlike storing terraform state in AWS where the S3 bucket needs to be paired with
        # a DynamoDB table for locking, in GCP we only need a bucket (without a corresponding locking table.)
        bucket_name = f"{super().get_env()}-kc-tf-state".replace('_','-')

        # https://cloud.google.com/storage/docs/locations
        bucket_location = super().get_region()

        self.logger.info(f"Environment '{bucket_location}': GCP project '{self.args.account}': region '{bucket_location}': Creating storage bucket '{bucket_name}' ...")

        # https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_create_bucket_class_location.py
        storage_client = storage.Client(project=get_profile_manager().get_env_project_id())
        bucket = storage_client.bucket(bucket_name)
        new_bucket = storage_client.create_bucket(bucket, location=bucket_location)

        # https://github.com/googleapis/python-storage/blob/5965400e0fb655246a1456fbb413623891930b22/samples/snippets/storage_enable_versioning.py#L30-L31
        new_bucket.versioning_enabled = True # https://github.com/googleapis/python-storage/blob/5965400e0fb655246a1456fbb413623891930b22/google/cloud/storage/bucket.py#L2610
        new_bucket.patch()

        print_utils.info(f"Created bucket '{new_bucket.name}' in region '{bucket_location}' for Environment '{super().get_env()}', GCP project '{self.args.account}'")
        return new_bucket


    # ------------------------------------------------------------------------------------
    # this is done once as part of `tf <action>` to execute terraform commands
    # ------------------------------------------------------------------------------------
    def exec_tf_action(self, action, subscription_tier, no_prompt):
        os.environ['terraform_dir'] = os.getcwd() + "/terraform/"

        items = self.get_all_resources()
        profile = Profile(self.args).get_profile(self.env)
        profile['name_dashed'] = profile['name'].replace('_', '-')

        kctf.main(self.args, profile, items, self.env, action, subscription_tier, no_prompt=no_prompt)

