__author__ = "Igor Royzis"
__license__ = "MIT"


import sys
import json
import logging
import psycopg2
from progress.bar import Bar

from commands.kc_metadata_manager.source_database import SourceDatabase
from commands.kc_metadata_manager.source_table_postgres import SourceTablePostgres


class SourceDatabasePostgres(SourceDatabase):
    
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args, source_database):
        super().__init__(args)
        self.env = super().get_env()
        self.args = args
        self.source_database = source_database
        self.conn = None


    def get_conn(self):
        try:
            if self.conn is None:
                self.conn = psycopg2.connect(
                    host=self.source_database['server'],
                    database = self.source_database['db'],
                    user = self.source_database['db_user'],
                    password = super().get_secret(self.source_database['password']),
                    port = self.source_database['port'],
                    options = f"-c search_path={self.source_database['schema']}")
            return self.conn
        except psycopg2.Error as e:
            self.logger.error("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
            self.logger.error(e)

    def get_ddl(self, table):
        return 'n/a'

    def update_schema_size_gb(self, schema):
        conn = self.get_conn()
        with conn.cursor() as cursor:
            sql = f"SELECT ROUND(sum(pg_relation_size(quote_ident(schemaname) " \
                  f"|| '.' || quote_ident(tablename)))::bigint / 1024 / 1024 / 1024) " \
                  f"FROM pg_tables WHERE schemaname = '{schema}';"
            cursor.execute(sql)
            result = cursor.fetchone()
            fqn = self.env + '_' + self.args.name
            super().get_dynamodb_resource()\
                .Table('source_database')\
                .update_item(Key={'fqn': fqn},
                             UpdateExpression="set size_gb = :p",
                             ExpressionAttributeValues={':p': result[0]})

    def get_columns(self, schema, table):
        conn = self.get_conn()
        with conn.cursor() as cursor:
            sql = f"SELECT c.table_schema, c.table_name, c.column_name, c.data_type, " \
                  f"c.character_maximum_length, c.numeric_precision, c.numeric_scale, tc.constraint_type " \
                  f"FROM information_schema.table_constraints tc " \
                  f"RIGHT JOIN information_schema.constraint_column_usage ccu on tc.table_name = ccu.table_name " \
                  f"AND tc.constraint_name = ccu.constraint_name " \
                  f"RIGHT JOIN information_schema.columns c ON c.table_schema = tc.constraint_schema " \
                  f"AND tc.table_name = c.table_name AND ccu.column_name = c.column_name " \
                  f"WHERE c.table_schema='{schema}' AND c.table_catalog='{self.args.db}' " \
                  f"AND c.table_name='{table}'; "
            # self.logger.info(sql)
            cursor.execute(sql)
            row_headers = [x[0] for x in cursor.description]
            columns = []
            for row in cursor.fetchall():
                columns.append(dict(zip(row_headers, row)))
            return columns

    def save_tables(self):
        conn = self.get_conn()
        with conn.cursor() as cursor:
            count_sql = f"SELECT count(*) from information_schema.TABLES " \
                        f"WHERE table_schema='{self.args.schema}' " \
                        f"AND table_catalog='{self.args.db}'"
            self.logger.info(count_sql)
            cursor.execute(count_sql)
            no_of_tables = cursor.fetchone()[0]

            sql = f"SELECT * from information_schema.TABLES WHERE table_schema='{self.args.schema}' AND table_catalog='{self.args.db}'"
            self.logger.info(sql)
            cursor.execute(sql)
            row_headers = [x[0] for x in cursor.description]
            source_table = SourceTablePostgres(self.args)
            progress = Bar('Geting source tables information', max=no_of_tables)
            for row in cursor.fetchall():
                table_json = dict(zip(row_headers, row))
                # self.logger.info(json.dumps(table_json))
                ddl = self.get_ddl(table_json['table_name'])
                columns = self.get_columns(table_json['table_schema'], table_json['table_name'])
                source_table.save_source_table(self.args.db, table_json, ddl, columns)
                progress.next()
            progress.finish()

        # update schema size (GB)
        self.update_schema_size_gb(self.args.db)
