__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
from datetime import datetime
import logging

from commands.kc_metadata_manager.source_table import SourceTable

class SourceTableMssql(SourceTable):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_source_table(self, schema, table_json, ddl, columns, pk):
        fqn = f"{super().get_env()}_{super().get_args().db}_{super().get_args().schema}_{table_json['TABLE_NAME']}"
        self.logger.debug(fqn)

        # save source table columns info
        for column in columns:
            data_length = 0
            if 'character_maximum_length' in column:
                data_length = column['character_maximum_length']

            data_precision = 0
            if 'numeric_precision' in column:
                data_precision = column['numeric_precision']

            data_scale = 0
            if 'numeric_scale' in column:
                data_scale = column['numeric_scale']

            item={
                'table': fqn, 
                'profile': super().get_env(),
                'column': column['column_name'],
                'table_schema': column['table_schema'],
                'column_type': '', #column['column_type'],
                'data_type': column['data_type'],
                'data_length': data_length,
                'data_precision': data_precision,
                'data_scale': data_scale,
                'timestamp': str(datetime.now()),
            }
            super().put_item('source_column', item)

        # save source table info
        if not pk:
            pk = ['n/a']

        self.logger.info(json.dumps(table_json, indent=2))
        item={
            'fqn': fqn, 
            'profile': super().get_env(), 
            'database': super().get_args().name, 
            'engine': super().get_args().engine,
            'table_name': table_json['TABLE_NAME'],
            'table_schema': table_json['TABLE_SCHEMA'], 
            'table_rows': "n/a",
            'data_length': "n/a",
            'pk': pk,
            'create_ddl': "n/a",
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
