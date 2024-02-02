__license__ = "MIT"

# import sys
# import os
# import json
# import contextlib
# import pymssql

# from  modules.kc_logging import Logger


# class SQLServer:
#     def __init__(self, jobName, connectionTuple):
#         self.jobName = jobName
#         self.connectionTuple = connectionTuple

#         ##DECLARATION SECTION
#         functionID = sys._getframe().f_code.co_name

#         self.logger = Logger(self.jobName)
#         self.logger.log("INFO", f"Inside method: {functionID}")

#         try:

#             ## Unpack the Connection Property Tuple
#             if len(self.connectionTuple) == 5:

#                 self.host = self.connectionTuple[0]
#                 self.username = self.connectionTuple[1]
#                 self.password = self.connectionTuple[2]
#                 self.portNumber = self.connectionTuple[3]
#                 self.initialDatabase = self.connectionTuple[4]

#             else:
#                 exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Wrong number of elements in the Tuple"
#                 raise Exception(exceptionMessage)

#         except Exception as e:
#             msg = e.args
#             exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exceptionMessage)
#             raise Exception(exceptionMessage)

#     def connect(self):

#         ## DECLARATION SECTION
#         functionID = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {functionID}")

#         return pymssql.connect(
#             server=self.host,
#             user=self.username,
#             password=self.password,
#             port=self.portNumber,
#             database=self.initialDatabase,
#         )

#     def executeSQL(self, sql, parameter=None):

#         ## DECLARATION SECTION
#         functionID = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {functionID}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor()) as cursor:
#                     if parameter is None:
#                         cursor.execute(sql)
#                     else:
#                         cursor.execute(sql, parameter)
#                     cursor.close()

#         except Exception as e:
#             msg = e.args
#             exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exceptionMessage)
#             raise Exception(exceptionMessage)

#     def getColumnHeader(self, sql):

#         ## DECLARATION SECTION
#         functionID = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {functionID}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor(buffered=True)) as cursor:
#                     cursor.execute(sql)
#                     #  Get the fields name (only once!)
#                     columnHeader = [field[0] for field in cursor.description]
#                 return columnHeader

#         except Exception as e:
#             msg = e.args
#             exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exceptionMessage)
#             raise Exception(exceptionMessage)

#     def returnDataSet(self, sql, parameter=None):

#         ## DECLARATION SECTION
#         functionID = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {functionID}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor(dictionary=True)) as cursor:
#                     if parameter is None:
#                         cursor.execute(sql)
#                     else:
#                         cursor.execute(sql, parameter)
#                     rows = cursor.fetchall()
#                 return rows

#         except Exception as e:
#             msg = e.args
#             exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exceptionMessage)
#             raise Exception(exceptionMessage)

#     def executeStoredProcedure(self, sql, parameters=None):

#         ## DECLARATION SECTION
#         functionID = sys._getframe().f_code.co_name
#         self.logger.log("INFO", f"Inside method: {functionID}")

#         try:

#             with contextlib.closing(self.connect()) as connection:
#                 with contextlib.closing(connection.cursor()) as cursor:
#                     if parameters is None:
#                         cursor.callproc(sql)
#                     else:
#                         cursor.callproc(sql, parameters)
#                     cursor.close()

#         except Exception as e:
#             msg = e.args
#             exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
#             self.logger.log("ERROR", exceptionMessage)
#             raise Exception(exceptionMessage)
