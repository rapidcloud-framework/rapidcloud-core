__author__ = 'Ivan Mendez'
__license__ = 'MIT'

import json
import os
import re

import awswrangler as wr


PROFILE = os.environ['PROFILE']
MAX_LIMIT = os.environ.get('MAX_LIMIT', 1000)
ALLOW_ORIGIN = os.environ.get('ALLOW_ORIGIN')


def escape(val):
    return val.replace("'", "''")


def lambda_handler(event, context, test=False):
    path = event['path']

    match = re.fullmatch(r'^/([^/]+)/([^/]+)/?$', path)
    if match is None:
        return {
            'statusCode': 404,
            'body': None
        }
    else:

        dbname, table = match.groups()
        database = f'{PROFILE}_{dbname}db'

        query_params = event['queryStringParameters'] or {}

        limit = query_params.pop('limit', MAX_LIMIT)

        where = ''
        for param in query_params:
            value = query_params.get(param)
            if value is not None:
                if len(where) == 0:
                    where += f' WHERE '
                else:
                    where += f' AND '
                where += f'"{param}" = \'{escape(value)}\''

        query = f'SELECT * FROM "{table}" {where} LIMIT {limit}'
        df = wr.athena.read_sql_query(
            sql=query,
            database=database,
            ctas_approach=False,
            s3_output=f"s3://{PROFILE.replace('_', '-')}-query-results-bucket/output/",
            keep_files=False)

        output = [
            dict([
                (column_name, row[i])
                for i, column_name in enumerate(df.columns)
            ])
            for row in df.values
        ]

        result = json.dumps(output, default=lambda v: str(v))
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': ALLOW_ORIGIN,
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': result
        }
