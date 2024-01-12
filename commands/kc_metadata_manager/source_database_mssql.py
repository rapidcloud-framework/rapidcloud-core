__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging
from progress.bar import Bar
from boto3.dynamodb.conditions import Key, Attr
# import pymssql

from commands.kc_metadata_manager.source_database import SourceDatabase
from commands.kc_metadata_manager.source_table_mssql import SourceTableMssql

class SourceDatabaseMssql(SourceDatabase):

    logger = logging.getLogger(__name__)

    def __init__(self, args, source_database):
        super().__init__(args)
        self.env = super().get_env()
        self.args = args
        self.source_database = source_database
        self.conn = None


    # def get_conn(self):
    #     try:
    #         if self.conn is None:
    #             host=self.source_database['server']
    #             db = self.source_database['db']
    #             user = self.source_database['db_user']
    #             password = super().get_secret(self.source_database['password'])
    #             self.conn = pymssql.connect(server=host, user=user, password=password, database=db)
    #         return self.conn
    #     except Exception as e:
    #         self.logger.error("ERROR: Unexpected error: Could not connect to MSSql instance.")
    #         self.logger.error(e)


    # def get_ddl(self,table):
    #     conn = self.get_conn()  
    #     with conn.cursor() as cursor:
    #         sql = f"SHOW CREATE TABLE {table}"
    #         cursor.execute(sql)
    #         return cursor.fetchone()
    
     
    # def update_schema_size_gb(self, schema):
    #     conn = self.get_conn()  
    #     with conn.cursor() as cursor:
    #         sql = f"SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 1) as size_in_gb FROM information_schema.tables WHERE table_schema = '{schema}' GROUP BY table_schema;"
    #         cursor.execute(sql)
    #         result = cursor.fetchone()
    #         fqn = super().get_env() + '_' + super().get_args().name
    #         response = super().get_dynamodb_resource().Table('source_database').update_item(Key={'fqn': fqn},
    #             UpdateExpression="set size_gb = :p",
    #             ExpressionAttributeValues={':p': result[0]}
    #         )


    # def get_columns(self,schema, table):
    #     conn = self.get_conn()  
    #     with conn.cursor() as cursor:
    #         sql = f"select table_schema, table_name, column_name, data_type, character_maximum_length, numeric_precision, numeric_scale from information_schema.COLUMNS WHERE TABLE_CATALOG='{super().get_args().db}' and TABLE_SCHEMA = '{super().get_args().schema}' and table_name='{table}'"
    #         self.logger.info(sql)
    #         cursor.execute(sql)
    #         row_headers=[x[0] for x in cursor.description] 
    #         columns = []
    #         for row in cursor.fetchall():
    #             columns.append(dict(zip(row_headers,row)))
    #         return columns


    # def get_pk(self, table_name):
    #     conn = self.get_conn()  
    #     with conn.cursor() as cursor:
    #         sql = f"select column_name from INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu join     INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc on ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME and CONSTRAINT_TYPE = 'PRIMARY KEY' where ccu.TABLE_CATALOG='{super().get_args().db}' and ccu.TABLE_SCHEMA = '{super().get_args().schema}' and ccu.table_name='{table_name}'"
    #         self.logger.info(sql)
    #         cursor.execute(sql)
    #         row_headers=[x[0] for x in cursor.description] 
    #         self.logger.info(row_headers)
    #         pk = []
    #         for row in cursor.fetchall():
    #             pk.append(row[0])
    #         return ",".join(pk)


    def save_tables(self):
        self.logger.warning("MS SQL Server Source is currently not supported")
        # conn = self.get_conn()  
        # with conn.cursor() as cursor:
        #     count_sql = f"select count(*) from information_schema.TABLES where TABLE_CATALOG='{super().get_args().db}' and TABLE_SCHEMA = '{super().get_args().schema}'"
        #     self.logger.info(count_sql)
        #     cursor.execute(count_sql)
        #     no_of_tables = cursor.fetchone()[0]
        #     self.logger.info(f"no_of_tables: {no_of_tables}")
            
        #     sql = f"select * from information_schema.TABLES where TABLE_CATALOG='{super().get_args().db}' and TABLE_SCHEMA = '{super().get_args().schema}'"
        #     self.logger.info(sql)
        #     cursor.execute(sql)
        #     row_headers=[x[0] for x in cursor.description] 
        #     self.logger.info(row_headers)
        #     source_table = SourceTableMssql(super().get_args())
        #     progress = Bar('Geting source tables information', max=no_of_tables)
        #     for row in cursor.fetchall():
        #         table_json = dict(zip(row_headers,row))
        #         self.logger.info(table_json)
        #         # ddl = self.get_ddl(table_json['TABLE_NAME'])
        #         ddl = "n/a"
        #         columns = self.get_columns(table_json['TABLE_SCHEMA'], table_json['TABLE_NAME'])
        #         pk = self.get_pk(table_json['TABLE_NAME'])
        #         source_table.save_source_table(super().get_args().db, table_json, ddl, columns, pk)
        #         progress.next()
        #     progress.finish()

        # # update schema size (GB)
        # # self.update_schema_size_gb(super().get_args().service)