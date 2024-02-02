__author__ = 'Ivan Mendez'
__license__ = 'MIT'

import datetime
import hashlib
import os
import json
import re
import logging
import sys

import psycopg2
import boto3

DBHOST = os.environ['DBHOST']
DBNAME = os.environ['DBNAME']
DBUSER = os.environ['DBUSER']
DBSCHEMA = os.environ['DBSCHEMA']
SECRETID = os.environ['SECRETID']
JOB_NAME = 'pii_matching'

logging.basicConfig()
logger = logging.getLogger(JOB_NAME)
logger.setLevel(logging.INFO)

session = boto3.Session()
s3_client = session.resource('s3')


class PIIMatch:

    def __init__(self):
        self.type_matching = None
        self.conn = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()
            logger.info('Database connection closed.')

    def connect(self):
        try:
            logger.info('Connecting to database...')
            secrets_client = boto3.client('secretsmanager')
            password = secrets_client.get_secret_value(SecretId=SECRETID)['SecretString']
            self.conn = psycopg2.connect(
                dbname=DBNAME,
                user=DBUSER,
                host=DBHOST,
                password=password,
                options=f'-c search_path={DBSCHEMA},public'
            )
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)

    @staticmethod
    def load_json(bucket, file_path):
        if bucket is None:
            with open(file_path) as json_file:
                data = json.load(json_file)
                return data
        else:
            obj = s3_client.Object(bucket, file_path)
            data = json.load(obj.get()['Body'])
            return data

    def load_file_type_matching(self, type_name):
        query = '''
        SELECT ftm.pii_type, ftm.pii_name FROM file_type
        INNER JOIN file_type_matching ftm on file_type.id = ftm.file_type_id
        WHERE file_type.name = %s
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(query, [type_name])
            self.type_matching = cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            logger.error("Error fetching type matching data", error)
        finally:
            cur.close()

    def get_field(self, db_field):
        _, field_name = next((row for row in self.type_matching if row[0] == db_field), [None, None])
        return field_name

    def generate_query(self, conditions, value, parameters=None):
        if parameters is None:
            parameters = []
        result = '('
        for condition in conditions:
            if condition.get('conditions') is not None:
                query, _ = self.generate_query(condition.get('conditions'), value, parameters)
                result += f' {condition.get("operator", "")} {query}'
            else:
                transform = condition.get('transform')
                db_field = condition.get('field')
                field = self.get_field(db_field)
                operator = condition.get('operator')
                if field is None:
                    # if the field is not on the dataset then the condition should always be false
                    result += 'false'
                else:
                    field_value = str(value.get(field))
                    if db_field == 'ssn':
                        if field_value is not None:
                            match = re.fullmatch(r'(:?\d{3}-\d{2}-\d{4}|\d{9}|.*\d{4})', field_value)
                            if match is None:
                                field_value = None
                    if transform is not None:
                        func_name = transform.get('function')
                        params = transform.get('params')
                        param_str = ''
                        for _ in params:
                            param_str += ',%s'
                        result += f'{func_name}({db_field}{param_str}) ' \
                                  f'{operator} ' \
                                  f'{func_name}(%s{param_str})'
                        parameters.extend(params)
                        parameters.append(field_value)
                        parameters.extend(params)
                    else:
                        result += f'{db_field} {operator} %s'
                        parameters.append(field_value)

        result += ')'
        return result, parameters

    def get_match(self, conditions, value):
        cur = self.conn.cursor()
        query, params = self.generate_query(conditions, value)
        person_id = None
        try:
            logger.debug(cur.mogrify(f'SELECT id FROM person_view'
                                     f' WHERE {query}', params))
            cur.execute(f'SELECT id FROM person_view'
                        f' WHERE {query}', params)
            person_id = cur.fetchone()
        except (Exception, psycopg2.Error) as error:
            logger.error("Error executing query: ", error)
            logger.error(json.dumps(value, indent=2))
        finally:
            cur.close()

        if person_id is None:
            return None
        return person_id[0]

    def db_insert(self, query, params):
        cur = self.conn.cursor()
        result = None
        try:
            logger.debug(f'Executing query: {cur.mogrify(query, params)}')
            cur.execute(query, params)
            result = cur.fetchone()
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            logger.error('Error inserting data', error)
        finally:
            cur.close()
        if result is None:
            return None
        return result[0]

    @staticmethod
    def hash_list(values):
        concatenated = ''
        for value in values:
            concatenated += str(value or '')
        return hashlib.md5(concatenated.encode('utf-8')).hexdigest()

    def process_data(self, values, file_type):
        try:
            logger.info('Loading configuration files')
            bucket = f'{os.environ["PROFILE"].replace("_", "-")}-ingestion'
            exact = PIIMatch.load_json(bucket, 'config/exact_match.json')
            proposed = PIIMatch.load_json(bucket, 'config/proposed_match.json')
        except Exception as error:
            logger.error('Error loading configuration files')
            logger.error(error)
            return
        for value in values:
            try:
                logger.debug(f'Trying to find a match for record with id: {value.get("id")}')
                match = self.get_match(exact, value)
                params = [value.get(self.get_field('ssn')), value.get(self.get_field('first_name')),
                          value.get(self.get_field('last_name')), value.get(self.get_field('date_of_birth')),
                          value.get(self.get_field('client_id'))]
                pii_hash = PIIMatch.hash_list(params)
                if match is None:
                    logger.debug('No exact match found, trying proposed match')
                    match = self.get_match(proposed, value)
                    if match is None:
                        logger.debug('No proposed match found, creating new person')
                        query = 'INSERT INTO person ' \
                                '(created_by, ssn, first_name, last_name, date_of_birth, client_id) ' \
                                'VALUES (0, %s, %s, %s, %s, %s) RETURNING id;'
                        person_id = self.db_insert(query, params)
                        logger.debug(f'New person created with id: {person_id}')
                        value['person_id'] = person_id
                        value['match_status'] = 'New'
                        value['pii_hash'] = pii_hash
                    else:
                        logger.debug('Proposed match found')
                        query = 'INSERT INTO proposed_match ' \
                                '(created_by, ssn, first_name, last_name, ' \
                                'date_of_birth, client_id, pii_hash, person_id, file_type) ' \
                                'VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'
                        params.append(pii_hash)
                        params.append(match)
                        params.append(file_type)
                        proposed_match_id = self.db_insert(query, params)
                        logger.debug(f'New proposed_match created with id: {proposed_match_id}')
                        value['person_id'] = proposed_match_id
                        value['match_status'] = 'Proposed'
                        value['pii_hash'] = pii_hash
                else:
                    logger.debug(f'Exact match found: {match}')
                    value['person_id'] = match
                    value['match_status'] = 'Exact'
                    value['pii_hash'] = pii_hash

            except Exception as error:
                logger.error(json.dumps(value, indent=2))

        return values


def lambda_handler(event, context, test=False):
    pii_match = PIIMatch()
    pii_match.connect()
    file_type = event['dataset']
    pii_match.load_file_type_matching(file_type)
    if pii_match.conn is None:
        return {
            'error': 'Can\'t connect to database'
        }
    if pii_match.type_matching is None:
        return {
            'error': 'Dataset not found'
        }
    pii_match.process_data(event['data'], file_type)
    return event


if __name__ == '__main__':
    start = datetime.datetime.now()
    data = {
        'data': PIIMatch.load_json(None, sys.argv[1]),
        'dataset': sys.argv[2]
    }

    lambda_handler(data, None)
    print(f"Start: {start}")
    print(f"End: {datetime.datetime.now()}")
