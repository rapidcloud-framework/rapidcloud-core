__author__ = "agarciaortiz@kinect-consulting.com"

import traceback
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra
import json

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        self.boto3_session = super().get_boto3_session()

        # use boto3 clients or resources as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def create(self, metadata=None):
        # Step 1
        '''
        Delete existing `aws_infra` items.
        Module automation metadata is stored in your DynamoDB `aws_infra` table
        delete existing aws_infra items for your module instance
        '''
        AwsInfra(self.args).delete_aws_infra(self.args.module, self.args.name)
        
        # Step 2
        #[{"path_part": "/", "parent_resource_id": "root", "lambda_integrations": [{"http_method": "GET", "uri": "test-lambda"}]}]
        '''
        Construct `params` dict for each AWS resource you plan to create for this module.
        Params will be used by terraform modules to generate your infrastructure
        '''
        # example:
        params = {
            "name": self.args.name,
            "disable_execute_api_endpoint": "true" if self.args.api_disable_execute_api_endpoint.lower() in ["y", "true"] else "false",
            "endpoint_type": self.args.api_endpoint_type.upper()
        }


        super().add_aws_resource("aws_api_gateway_rest_api", self.args.name, params)

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

    def add_lambda_integration(self, metadata=None):
        # 1. check if resource already exists
        fqn = f"{self.env}_aws_api_gateway_resource_{self.args.api_rest_api_name}_{self.args.api_parent_resource_name}_{self.args.name}"
        existing_resource = self.get_item("aws_infra", "fqn", fqn)
        if existing_resource is None:
            existing_resource = {}
        AwsInfra(self.args).delete_aws_infra(self.args.module, self.args.name)
        # 2. if yes, add entry into that resource's lambda integrations and save
        # 3. if not, add new resource and add lambda integrations object with one entry, save
        lambda_integrations = existing_resource.get("params", {}).get("lambda_integrations", [])
        
        lambda_integrations = [
            i for i in lambda_integrations 
                if not (i["http_method"] == self.args.api_http_method 
                and i["lambda_name"] == self.args.api_lambda_name)
            ]

        lambda_integrations.append(
            {
                "http_method": self.args.api_http_method, 
                "lambda_name": self.args.api_lambda_name
            }
        )

        params = {
            "rest_api_name": self.args.api_rest_api_name,
            "name": self.args.name,
            "parent_resource_name": self.args.api_parent_resource_name,
            "lambda_integrations": lambda_integrations
        }

        super().add_aws_resource("aws_api_gateway_resource", self.args.name, params, fqn=fqn)
        self.add_trigger_to_deployment(self.args.api_rest_api_name, self.args.api_parent_resource_name, self.args.name)
    
    def add_trigger_to_deployment(self, rest_api_name, parent_resource_name, resource_name):
        existing_deployment = self.get_item("aws_infra", "fqn", f"{self.env}_aws_api_gateway_stage_{rest_api_name}-{self.env}")
        if existing_deployment is None:
            existing_deployment = {}
            
        AwsInfra(self.args).delete_aws_infra(self.args.module, f"{rest_api_name}-{super().get_env()}")
        triggers = existing_deployment.get("params", {}).get("triggers", [])
        
        triggers = [
            t for t in triggers 
                if not (t["parent_resource_name"] == parent_resource_name
                and t["resource_name"] == resource_name)
            ]

        triggers.append(
            {
                "parent_resource_name": parent_resource_name, 
                "resource_name": resource_name
            }
        )

        params = {
            "rest_api_name": rest_api_name,
            "triggers": triggers
        }
        super().add_aws_resource("aws_api_gateway_stage", f"{rest_api_name}-{super().get_env()}", params)

    def remove_lambda_integration(self, metadata=None):
        fqn = f"{self.env}_aws_api_gateway_resource_{self.args.api_rest_api_name}_{self.args.api_parent_resource_name}_{self.args.name}"
        existing_resource = self.get_item("aws_infra", "fqn", fqn)

        self.get_dynamodb_resource().Table("aws_infra").delete_item(Key={"fqn": fqn})
        
        self.get_dynamodb_resource().Table("metadata").delete_item(Key={"profile": self.env , "fqn": f"{self.env}_{self.args.module}_{self.args.name}_{self.args.api_http_method}_{self.args.api_parent_resource_name}_{self.args.api_rest_api_name}"})
        
        if existing_resource is None:
            return
            
        lambda_integrations = existing_resource.get("params", {}).get("lambda_integrations", [])
        
        lambda_integrations = [ i for i in lambda_integrations if i["http_method"] != self.args.api_http_method ]

        if not lambda_integrations:
            self.remove_trigger_from_deployment(self.args.api_rest_api_name, self.args.api_parent_resource_name, self.args.name)
            return

        params = {
            "rest_api_name": self.args.api_rest_api_name,
            "name": self.args.name,
            "parent_resource_name": self.args.api_parent_resource_name,
            "lambda_integrations": lambda_integrations
        }

        super().add_aws_resource("aws_api_gateway_resource", self.args.name, params, fqn=fqn)

    def remove_trigger_from_deployment(self, rest_api_name, parent_resource_name, resource_name):
        existing_deployment = self.get_item("aws_infra", "fqn", f"{self.env}_aws_api_gateway_stage_{rest_api_name}-{self.env}")
        if existing_deployment is None:
            existing_deployment = {}
            
        self.get_dynamodb_resource().Table("aws_infra").delete_item(Key={"fqn": f"{self.env}_aws_api_gateway_stage_{rest_api_name}-{self.env}"})
        
        triggers = existing_deployment.get("params", {}).get("triggers", [])
        
        triggers = [
            t for t in triggers 
                if not (t["parent_resource_name"] == parent_resource_name
                and t["resource_name"] == resource_name)
            ]
            
        if not triggers:
            return

        params = {
            "rest_api_name": rest_api_name,
            "triggers": triggers
        }
        super().add_aws_resource("aws_api_gateway_stage", f"{rest_api_name}-{super().get_env()}", params)