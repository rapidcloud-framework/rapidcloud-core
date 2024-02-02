__author__ = "Igor Royzis"
__license__ = "MIT"


import json
from datetime import datetime
import logging

from commands.kc_metadata_manager.source_table import SourceTable

class SourceTableMysql(SourceTable):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)

    def save_source_table(self, schema, table_json, ddl, columns):
        fqn = f"{super().get_env()}_{super().get_args().name}_{super().get_args().db}_{table_json['TABLE_NAME']}"
        self.logger.debug(fqn)

        # save source table columns info
        pk = []
        for column in columns:
            if column['column_key'] in ['PRI']:  
                pk.append(column['column_name'])

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
                'column_type': column['column_type'],
                'data_type': column['data_type'],
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
            'table_schema': table_json['TABLE_SCHEMA'],
            'table_rows': table_json['TABLE_ROWS'],
            'data_length': table_json['DATA_LENGTH'],
            'pk': ",".join(pk),
            'create_ddl': str(ddl),
            'timestamp': str(datetime.now()),
        }
        super().put_item(self.TABLE_NAME, item)
