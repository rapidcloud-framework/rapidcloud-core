AUTHOR_PLACEHOLDER

from commands.kc_metadata_manager.azure_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # azure sdk
        # self.boto3_session = super().get_boto3_session()

        # use azure sdk as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def COMMAND_NAME_PLACEHOLDER(self, metadata=None):
        # Step 1
        '''
        Delete existing `azure_infra` items.
        Module automation metadata is stored in your CosmosDB `azure_infra` table
        delete existing azure_infra items for your module instance
        '''
        super().delete_infra_metadata(name=self.args.name)

        # Step 2
        '''
        Construct `params` dict for each Azure resource you plan to create for this module.
        Params will be used by terraform modules to generate your infrastructure
        '''
        # example:
        params = {
            "resource_name": "some_name",
            "category": "testing",
            "size": 5
        }

        # Step 3
        '''
        Create `azure_infra` item for each Azure resource you plan to automate
        '''
        # example:

        # must be a valid Terraform supported Azure resource type
        resource_type = "some_resource_type"

        # must be a unique resource name for the specified resource_type
        resource_name = "some_name"
        # TODO uncomment if needed
        # super().add_infra_resource(resource_type, resource_name, params)

        # TODO
        '''
        Repeat steps 2 and 3 for each resource to be generated for this module
        '''

        # TODO
        '''
        Optionally and in addition to creating resources, you can run any code here 
        to support this module functionality.
        '''
