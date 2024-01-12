from datetime import datetime
import logging
import random
from commands.kc_metadata_manager.azure_metadata import Metadata


class Profile(Metadata):

    TABLE_NAME = 'profile'
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def get_profile(self, env):
        return super().get_item_by_key(self.TABLE_NAME, env)

    def save_profile(self, profile_to_update=None):
        tfstorage = f'kcrcaztfstate{super().get_args().env_suffix}'
        tfcontainer = super().get_env().replace('_','-')
        if profile_to_update is None:
            item={
                'name': super().get_env(), 
                'id': super().get_env(), 
                'enabled': True,
                'env_id': ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)]),
                'client': self.args.client,
                'workload': self.args.workload,
                'env': self.args.env_suffix,
                'shared': self.args.shared.lower() in ["yes", "true", True],
                'shared_with': self.args.shared_with.split(",") if self.args.shared_with else "all",
                'subscription': self.args.subscription,
                'vnet': self.args.vnet,
                'region': self.args.region,
                'vpn_only': self.args.vpn_only,
                'tf_storage': tfstorage,
                'tf_container': tfcontainer,
                'tf_storage_rg': super().RESOURCE_GROUP,
                'created_timestamp': str(datetime.now()),
                'created_by': self.args.current_session_email,
                'timestamp': str(datetime.now()),
                'updated_by': self.args.current_session_email
            }
        # updating existing profile
        else:
            item = profile_to_update
            item.update({
                'shared': self.args.shared.lower() in ["yes", "true", True],
                'shared_with': self.args.shared_with.split(",") if self.args.shared_with else "all",
                'vpc': self.args.vpc,
                'vpn_only': self.args.vpn_only.lower() in ["yes", "true", True],
                'timestamp': str(datetime.now()),
                'created_by': profile_to_update['updated_by'] if 'created_by' not in profile_to_update else profile_to_update['created_by'],
                'updated_by': self.args.current_session_email
            })  

        super().put_item(self.TABLE_NAME, item)