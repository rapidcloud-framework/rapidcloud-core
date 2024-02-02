__author__ = "mbartoli"

import boto3
import logging

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

logger = logging.getLogger(__name__)

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def _linked_role_check(self) -> bool:
        iam = self.get_iam_client()

        role_name = 'AWSServiceRoleForAmazonOpenSearchService'

        try:
            response = iam.get_role(RoleName=role_name)
            role = response['Role']
            logger.debug(f"The role '{role_name}' already exists with ARN '{role['Arn']}'")
            return True
        except iam.exceptions.NoSuchEntityException:
            logger.debug(f"The role '{role_name}' does not exist")
            return False

    def create(self, metadata=None):
        AwsInfra(self.args).delete_aws_infra()
        params = super().get_opensearch_params()
        params['aws_os_service_role_exists'] = self._linked_role_check()
        logger.debug(f'linked_role: {params["aws_os_service_role_exists"]}')
        super().add_aws_resource("aws_opensearch", self.args.name, params)
