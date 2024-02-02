__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
from datetime import datetime
import logging

from commands.kc_metadata_manager.aws_metadata import Metadata

class Datawarehouse(Metadata):

    TABLE_NAME = 'datawarehouse'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def save_datawarehouse(self):
        dw_type = self.args.type if self.args.type else "Redshift"
        item={
            'fqn': f"{super().get_env()}_{dw_type}".replace('-','').replace('_',''), 
            'profile': super().get_env(), 
            'type': dw_type, 
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata", dw_type)

        if dw_type == 'Redshift':
            super().save_password(super().get_env(), 'redshift_cluster', 'main', '')
            params = super().get_redshift_params()
            super().add_aws_resource('redshift_cluster', 'main', params)
        
        # elif dw_type == 'Snowflake':
        #     super().add_aws_resource('snowflake_warehouse', 'main', {})

