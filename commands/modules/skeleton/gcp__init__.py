AUTHOR_PLACEHOLDER

from commands.kc_metadata_manager.gcp_metadata import Metadata
from server.utils.gcp_metadata_utils import enable_gcp_service_apis

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def COMMAND_NAME_PLACEHOLDER(self, metadata: dict=None) -> None:
        # Step 1
        '''
        Delete existing `gcp_infra` items.
        There can potentically be multiple records in `gcp_infra` for a single record in `metadata` table.
        If we don't delete all corresponding records in `gcp_infra` first, a newly updated `metadata` record
        may map to fewer `gcp_infra` records than before and therefore leaves garbage there.
        Module automation metadata is stored in your GCP Firestore `gcp_infra` table.
        '''
        super().delete_infra_metadata(name=self.args.name)

        # Step 2
        '''
        Construct `params` dict for each GCP resource you plan to create for this module.
        Params will be used by terraform modules to generate your infrastructure
        '''
        # example:
        # params = {
        #     "resource_name": metadata['params']['name'],
        #     "vpc_name":      metadata['params']['gcp_storage_vpc_name'],
        #     "capacity_gb":   metadata['params']['gcp_storage_capacity_gb'],
        # }

        # Step 3
        '''
        Create `gcp_infra` item for each GCP resource you plan to automate
        '''
        # Must be a valid Terraform supported GCP resource type,
        # e.g.,
        #   resource_type = "google_redis_instance"
        #   with a corresponding file .../terraform/templates/google_redis_instance.j2
        resource_type = "some_resource_type"

        # must be a unique resource name for the specified resource_type
        resource_name = params["resource_name"]

        # TODO uncomment if needed
        # super().add_infra_resource(resource_type, resource_name, params)

        # TODO
        '''
        Repeat steps 2 and 3 for each resource to be generated for this module
        '''

        # Step 4
        '''
        Optionally and in addition to creating resources, you can run any code here
        to support this module functionality.
        E.g.,
            enable_gcp_service_apis(["logging.googleapis.com", "pubsub.googleapis.com"])
        '''
