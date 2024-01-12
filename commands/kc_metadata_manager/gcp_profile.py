from datetime import datetime
import json
import logging
import os
import random

from google.cloud import firestore
from google.cloud.firestore_v1.document import DocumentReference

from commands import print_utils
from commands.kc_metadata_manager.gcp_metadata import Metadata
from commands.kc_metadata_manager.profile_manager import get_profile_manager


class Profile(Metadata):

    TABLE_NAME = 'profile'
    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def get_profile(self, env: str) -> dict:
        doc = self.get_metadata_root().collection('profile').document(env).get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def save_profile(self, profile_to_update: dict = None) -> None:
        tf_bucket = f"{super().get_env()}-kc-tf-state".replace('_','-')
        if profile_to_update is None:
            item={
                'name': super().get_env(),                                                           # 1
                'id': super().get_env(),                                                             # 2
                'enabled': True,                                                                     # 3
                'env_id': ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)]),         # 4
                'client': self.args.client,                                                          # 5
                'workload': self.args.workload,                                                      # 6
                'env': self.args.env_suffix,                                                         # 7
                'shared': self.args.shared.lower() in ["yes", "true", True],                         # 8
                'shared_with': self.args.shared_with.split(",") if self.args.shared_with else "all", # 9
                'env_project_id': get_profile_manager().get_env_project_id(),                        # 11
                'vpc': self.args.vpc,                                                                # 12
                'region': self.args.region,                                                          # 13
                'vpn_only': self.args.vpn_only.lower() in ["yes", "true", True],                     # 14
                'state_bucket': tf_bucket,                                                           # 15
                'created_timestamp': str(datetime.now()),                                            # 16
                'created_by': super().get_config()['email'],                                         # 17
                'timestamp': str(datetime.now()),                                                    # 18
                'updated_by': super().get_config()['email'],                                         # 19
            }
        else:
            # updating existing profile
            item = profile_to_update
            item.update({
                # 'name': ...                                                                        # 1. Omit because this is essentially part of the primary key.
                # 'id': ...                                                                          # 2. Omit because this is essentially part of the primary key.
                'enabled': True,                                                                     # 3
                # 'env_id': ...                                                                      # 4. Omit because this was created as a random number and therefore immutable.
                # 'client': ...                                                                      # 5. Omit because this is essentially part of the primary key.
                # 'workload': ...                                                                    # 6. Omit because this is essentially part of the primary key.
                # 'env': ...                                                                         # 7. Omit because this is essentially part of the primary key.
                'shared': self.args.shared.lower() in ["yes", "true", True],                         # 8
                'shared_with': self.args.shared_with.split(",") if self.args.shared_with else "all", # 9
                'env_project_id': get_profile_manager().get_env_project_id(),                        # 11
                'vpc': self.args.vpc,                                                                # 12
                'region': self.args.region,                                                          # 13
                'vpn_only': self.args.vpn_only.lower() in ["yes", "true", True],                     # 14
                # 'state_bucket': ...                                                                # 15. Omit because we don't want to lose the previous state.
                # 'created_timestamp': ...                                                           # 16. Omit because this is logically immutable.
                'created_by': profile_to_update['updated_by'] if 'created_by' not in profile_to_update else profile_to_update['created_by'], # 17
                'timestamp': str(datetime.now()),                                                    # 18
                'updated_by': super().get_config()['email'],                                         # 19
            })

        super().put_item(self.TABLE_NAME, item)


    def get_all_profiles(self):
        data = []
        all_profiles_filename = "./config/all_gcp_profiles.json"
        if os.path.exists(all_profiles_filename):
            with open(all_profiles_filename, 'r') as f:
                all_profiles = json.load(f)
                for env_name, project_id in all_profiles.items():
                    p = self.get_profile(project_id, env_name)
                    if p:
                        p["project"] = project_id
                        data.append(p)
                    else:
                        self.logger.warn(f"The environment name '{env_name}' (project_id={project_id}) has no corresponding profile in database.")

        if len(data) == 0:
            self.logger.warn(f"The file '{all_profiles_filename}' doesn't exist or is empty. This might be OK depending on the scenario.")

        data.sort(key=lambda x: (x["project"],x["name"]))
        return data


    def list(self):
        profiles = self.get_all_profiles()
        print_utils.print_grid_from_json(profiles, cols=['name','project','vpc','region','timestamp'])

