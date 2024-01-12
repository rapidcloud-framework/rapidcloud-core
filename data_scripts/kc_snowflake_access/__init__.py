__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

# import sys
# import os
# import json
# import contextlib
# import s3fs

# ##import snowflake.connector as snowflake
# from snowflake.connector import connect
# from snowflake.connector import DictCursor
# from  modules.kc_logging import Logger

# from snowflake.sqlalchemy import URL
# from sqlalchemy import *

# s3 = s3fs.S3FileSystem(anon=False)   # Connecting to S3

# class Snowflake:
#     def __init__(self, jobName, aws_secrets):
#         self.jobName = jobName
#         self.aws_secrets = aws_secrets

#         ##DECLARATION SECTION
#         function_id = sys._getframe().f_code.co_name

#         self.logger = Logger(self.jobName)
#         self.logger.log("INFO", f"Inside method: {function_id}")

#         try:

#             if len(self.aws_secrets) == 6:

#                 self.account = self.aws_secrets['snowflake_account']
#                 self.user = self.aws_secrets['snowflake_user']
#                 self.password = self.aws_secrets['snowflake_password']
#                 self.dbname = self.aws_secrets['snowflake_dbname']
#                 self.warehouse = self.aws_secrets['snowflake_warehouse']
#                 self.role = self.aws_secrets['snowflake_role']

#             else:
#                 exception_message = f"Exception Occurred Inside this method {function_id} --> Wrong number of metadata key/value in the secret json"
#                 raise Exception(exception_message)

#         except Exception as e:
#             msg = e
#             exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exception_message)
#             raise Exception(exception_message)

#     def connect(self):

#         ## DECLARATION SECTION
#         function_id = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {function_id}")

#         try:

#             connection = connect(
#                 user=self.user,
#                 password=self.password,
#                 account=self.account,
#                 database=self.dbname,
#                 warehouse=self.warehouse,
#                 role=self.role,
#                 autocommit=True,
#             )

#             return connection

#         except Exception as e:
#             msg = e
#             exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exception_message)
#             raise Exception(exception_message)

#     def execute_sql(self, sql, parameter=None):

#         ## DECLARATION SECTION
#         function_id = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {function_id}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor()) as cursor:
#                     if parameter is None:
#                         cursor.execute(sql)
#                     else:
#                         cursor.execute(sql, parameter)
#                     cursor.close()

#         except Exception as e:
#             msg = e
#             exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exception_message)
#             raise Exception(exception_message)

#     def execute_snowflake_string(self,snowflake_sql):

#         ## DECLARATION SECTION
#         function_id = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {function_id}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor()) as cursor:
#                         connection.execute_string(snowflake_sql)
#                 cursor.close()

#         except Exception as e:
#             msg = e
#             exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exception_message)
#             raise Exception(exception_message)

#     def execute_snowflake_stream(self,snowflake_file):

#         ## DECLARATION SECTION
#         function_id = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {function_id}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 ##with contextlib.closing(connection.cursor()) as cursor:
#                 with s3.open(snowflake_file, 'r', encoding='utf-8') as snowflake_sql:
#                     for cur in connection.execute_stream(snowflake_sql):
#                         for ret in cur:
#                                 self.logger.log("INFO", ret)
#                 cur.close()

#         except Exception as e:
#             msg = e
#             exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exception_message)
#             raise Exception(exception_message)

#     def return_dataset(self, sql, parameter=None):

#         ## DECLARATION SECTION
#         function_id = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {function_id}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor(DictCursor)) as cursor:
#                     if parameter is None:
#                         cursor.execute(sql)
#                     else:
#                         cursor.execute(sql, parameter)
#                     rows = cursor.fetchall()
#                 return rows

#         except Exception as e:
#             msg = e
#             exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exception_message)
#             raise Exception(exception_message)
