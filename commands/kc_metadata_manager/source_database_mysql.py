__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import sys
import logging
import pymysql
from progress.bar import Bar

from commands.kc_metadata_manager.source_database import SourceDatabase
from commands.kc_metadata_manager.source_table_mysql import SourceTableMysql

class SourceDatabaseMysql(SourceDatabase):

    logger = logging.getLogger(__name__)

    def __init__(self, args, source_database):
        super().__init__(args)
        self.env = super().get_env()
        self.args = args
        self.source_database = source_database
        self.conn = None


    def get_conn(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(
                    host=self.source_database['server'],
                    db = self.source_database['db'],
                    user = self.source_database['db_user'],
                    passwd = super().get_secret(self.source_database['password']),
                    port = self.source_database['port'],
                    connect_timeout=10)
            return self.conn
        except pymysql.MySQLError as e:
            self.logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            self.logger.error(e)


    def get_ddl(self,table):
        # self.logger.info("Getting table ddl...")  
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            sql = f"SHOW CREATE TABLE {table}"
            cursor.execute(sql)
            return cursor.fetchone()
    
    
    def update_schema_size_gb(self, schema):
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            sql = f"SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 1) as size_in_gb FROM information_schema.tables WHERE table_schema = '{schema}' GROUP BY table_schema;"
            cursor.execute(sql)
            result = cursor.fetchone()
            fqn = super().get_env() + '_' + self.args.name
            response = super().get_dynamodb_resource().Table('source_database').update_item(Key={'fqn': fqn},
                UpdateExpression="set size_gb = :p",
                ExpressionAttributeValues={':p': result[0]}
            )


    def get_columns(self,schema, table):
        # self.logger.info("Getting table columns...")  
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            sql = f"select table_schema, table_name, column_name, column_type, data_type, column_key, character_maximum_length, numeric_precision, numeric_scale from information_schema.COLUMNS WHERE table_schema='{schema}' and table_name='{table}'"
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description] 
            columns = []
            for row in cursor.fetchall():
                columns.append(dict(zip(row_headers,row)))
            return columns


    def save_tables(self):
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            count_sql = f"select count(*) from information_schema.TABLES where table_schema='{self.args.db}'"
            cursor.execute(count_sql)
            no_of_tables = cursor.fetchone()[0]
            
            sql = f"select * from information_schema.TABLES where table_schema='{self.args.db}'"
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description] 
            source_table = SourceTableMysql(self.args)
            progress = Bar('Geting source tables information', max=no_of_tables)
            for row in cursor.fetchall():
                table_json = dict(zip(row_headers,row))
                ddl = self.get_ddl(table_json['TABLE_NAME'])
                columns = self.get_columns(table_json['TABLE_SCHEMA'], table_json['TABLE_NAME'])
                source_table.save_source_table(self.args.db, table_json, ddl, columns)
                progress.next()
            progress.finish()

        # update schema size (GB)
        self.update_schema_size_gb(self.args.db)


