__author__ = "Igor Royzis"
__license__ = "MIT"


from datetime import datetime
import logging
from commands.kc_metadata_manager.aws_metadata import Metadata

class DataTypeMapping(Metadata):

    TABLE_NAME = 'data_type_translation'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_data_type_mapping(self):
        item = {
            "fqn": f"{super().get_args().engine_from}_{super().get_args().engine_to}",
            "cast_from": super().get_args().cast_from,
            "cast_to": super().get_args().cast_to,
            "engine_from": super().get_args().engine_from,
            "engine_to": super().get_args().engine_to,
            "create_timestamp": str(datetime.now())
        }
        super().put_item(self.TABLE_NAME, item)
