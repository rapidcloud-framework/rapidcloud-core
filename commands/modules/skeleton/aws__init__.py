AUTHOR_PLACEHOLDER

from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        self.boto3_session = super().get_boto3_session()

        # use boto3 clients or resources as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def COMMAND_NAME_PLACEHOLDER(self, metadata=None):
        # Step 1
        '''
        Delete existing `aws_infra` items.
        Module automation metadata is stored in your DynamoDB `aws_infra` table
        delete existing aws_infra items for your module instance
        '''
        super().delete_infra_metadata(name=self.args.name)

        # Step 2
        '''
        Construct `params` dict for each AWS resource you plan to create for this module.
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
        Create `aws_infra` item for each AWS resource you plan to automate
        '''
        # example:

        # must be a valid Terraform supported AWS resource type
        resource_type = "lambda_function"

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

        For example, enable or disable CloudWatch event rules, send SNS or SES message, 
        upload or download files to/from S3, update database records, kick-off 
        DMS jobs, start Glue workflows, etc
        '''
