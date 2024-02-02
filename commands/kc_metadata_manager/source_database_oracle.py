__author__ = "Igor Royzis"
__license__ = "MIT"


import logging
import cx_Oracle
from progress.bar import Bar

from commands.kc_metadata_manager.source_database import SourceDatabase
from commands.kc_metadata_manager.source_table_oracle import SourceTableOracle

class SourceDatabaseOracle(SourceDatabase):

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
                host=self.source_database['server']
                db = self.source_database['db']
                user = self.source_database['db_user']
                password = super().get_secret(self.source_database['password'])
                port = self.source_database['port']
                schema = self.source_database['schema']
                self.conn = cx_Oracle.connect(f"{user}/{password}@{host}:{port}/{schema}")
            return self.conn
        except cx_Oracle.Error as error:
            self.logger.error("ERROR: Unexpected error: Could not connect to Oracle instance.")
            self.logger.error(error)


    def get_ddl(self,table):
        return 'n/a'
    
    
    def update_schema_size_gb(self, schema):
        return 'n/a'


    def get_columns(self, schema, table):
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            sql = f"SELECT owner AS table_schema, table_name, column_name, data_type, data_length, data_precision, data_scale from sys.all_tab_columns col where col.owner = '{schema.upper()}' and col.table_name = '{table.upper()}'"
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description] 
            columns = []
            for row in cursor.fetchall():
                columns.append(dict(zip(row_headers,row)))
            return columns


    def get_pk(self, table_name):
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            sql = f"SELECT cols.column_name FROM all_constraints cons, all_cons_columns cols WHERE cols.OWNER = upper('{self.args.db}') AND cols.table_name = upper('{table_name}') AND cons.constraint_type = 'P' AND cons.constraint_name = cols.constraint_name AND cons.owner = cols.owner"
            self.logger.info(sql)
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description] 
            self.logger.info(row_headers)
            pk = []
            for row in cursor.fetchall():
                pk.append(row[0])
            return ",".join(pk)


    def save_tables(self):
        conn = self.get_conn()  
        with conn.cursor() as cursor:
            count_sql = f"SELECT count(*) FROM all_tables WHERE owner = '{self.args.db.upper()}'"
            self.logger.info(f"count_sql: {count_sql}")
            cursor.execute(count_sql)
            no_of_tables = cursor.fetchone()[0]
            self.logger.info(f"no_of_tables: {no_of_tables}")
            if no_of_tables == 0:
                return
            
            sql = f"SELECT * FROM all_tables WHERE owner = '{self.args.db.upper()}'"
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description] 
            source_table = SourceTableOracle(self.args)
            progress = Bar('Geting source tables information', max=no_of_tables)
            for row in cursor.fetchall():
                table_json = dict(zip(row_headers,row))
                ddl = self.get_ddl(table_json['TABLE_NAME'])
                columns = self.get_columns(table_json['OWNER'], table_json['TABLE_NAME'])
                pk = self.get_pk(table_json['TABLE_NAME'])
                source_table.save_source_table(self.args.db, table_json, ddl, columns, pk)
                progress.next()
            progress.finish()

        # update schema size (GB)
        self.update_schema_size_gb(self.args.db)

