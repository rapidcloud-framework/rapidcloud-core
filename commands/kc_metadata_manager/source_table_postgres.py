__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
from datetime import datetime
import logging

from commands.kc_metadata_manager.source_table import SourceTable

class SourceTablePostgres(SourceTable):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_source_table(self, schema, table_json, ddl, columns):
        fqn = f"{super().get_env()}_{super().get_args().name}_{super().get_args().schema}_{table_json['table_name']}"
        # self.logger.debug(fqn)

        # save source table columns info
        pk = []
        for column in columns:
            if column.get('constraint_type') == 'PRIMARY KEY':
                pk.append(column['column_name'])

            item={
                'table': fqn, 
                'profile': super().get_env(),
                'column': column['column_name'],
                'table_schema': column['table_schema'],
                'column_type': None,
                'data_type': column['data_type'],
                'data_length': column.get('character_maximum_length', 0),
                'data_precision': column.get('numeric_precision', 0),
                'data_scale': column.get('numeric_scale', 0),
                'timestamp': str(datetime.now()),
            }
            super().put_item('source_column', item)

        # save source table info
        if not pk:
            pk.append('n/a')

        # self.logger.info(json.dumps(table_json, indent=2, default=super().json_converter))
        item={
            'fqn': fqn, 
            'profile': super().get_env(), 
            'database': super().get_args().name, 
            'engine': super().get_args().engine,
            'table_name': table_json.get('table_name'),
            'table_schema': table_json.get('table_schema'),
            'table_rows': table_json.get('table_rows'),
            'data_length': table_json.get('data_length'),
            'pk': ",".join(pk),
            'create_ddl': str(ddl),
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
