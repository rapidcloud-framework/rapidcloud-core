__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
from datetime import datetime
import logging

from commands.kc_metadata_manager.source_table import SourceTable

class SourceTableOracle(SourceTable):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)


    def save_source_table(self, schema, table_json, ddl, columns, pk):
        fqn = f"{super().get_env()}_{super().get_args().name}_{super().get_args().db}_{table_json['TABLE_NAME']}".lower()
        self.logger.debug(fqn)

        # save source table columns info
        for column in columns:
            data_length = 0
            if 'DATA_LENGTH' in column:
                data_length = column['DATA_LENGTH']

            data_precision = 0
            if 'DATA_PRECISION' in column:
                data_precision = column['DATA_PRECISION']

            data_scale = 0
            if 'DATA_SCALE' in column:
                data_scale = column['DATA_SCALE']

            item={
                'table': fqn, 
                'profile': super().get_env(),
                'column': column['COLUMN_NAME'],
                'table_schema': column['TABLE_SCHEMA'],
                'column_type': "",
                'data_type': column['DATA_TYPE'],
                'data_length': data_length,
                'data_precision': data_precision,
                'data_scale': data_scale,
                'timestamp': str(datetime.now()),
            }
            super().put_item('source_column', item)

        # save source table info
        if not pk:
            pk.append('n/a')

        self.logger.info(json.dumps(table_json, indent=2, default=super().json_converter))
        item={
            'fqn': fqn, 
            'profile': super().get_env(), 
            'database': super().get_args().name, 
            'engine': super().get_args().engine,
            'table_name': table_json['TABLE_NAME'],
            'table_schema': table_json['OWNER'],
            'table_rows': table_json['NUM_ROWS'],
            'data_length': int(table_json['NUM_ROWS']) * int(table_json['AVG_ROW_LEN']),
            'pk': pk,
            'create_ddl': str(ddl),
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)


