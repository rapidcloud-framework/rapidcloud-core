__license__ = "MIT"

import sys
import os
import json
import contextlib
from mysql.connector import connect
from mysql.connector import Error

from  data_scripts.kc_logging import Logger


class MySQL:
    def __init__(self, jobName, aws_secrets):
        self.jobName = jobName
        self.aws_secrets = aws_secrets

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger = Logger(self.jobName)
        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            if len(self.aws_secrets) == 5:
                self.dbname = self.aws_secrets["dbname"]
                self.host = self.aws_secrets["host"]
                self.password = self.aws_secrets["password"]
                self.port = self.aws_secrets["port"]
                self.user = self.aws_secrets["user"]
            else:
                exception_message = "The Secrets JSON needs to have 5 elements!!"
                raise Exception(exception_message)

            self.logger.log("INFO", f"Host: {self.host}")
            self.logger.log("INFO", f"Database: {self.dbname}")
            self.logger.log("INFO", f"Port Number: {self.port}")
            self.logger.log("INFO", f"User ID: {self.user}")

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def connect(self):
        return connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.dbname,
            port=self.port,
        )

    def execute_sql(self, sql, parameter=None):

        ## DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    if parameter is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, parameter)
                    cursor.close()

        except Error as e:
            msg = e.msg
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def get_column_header(self, sql):

        ## DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor(buffered=True)) as cursor:
                    cursor.execute(sql)
                    #  Get the fields name (only once!)
                    columnHeader = [field[0] for field in cursor.description]
                return columnHeader

        except Error as e:
            msg = e.msg
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def return_dataset(self, sql, parameter=None):

        ## DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor(dictionary=True)) as cursor:
                    if parameter is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, parameter)
                    rows = cursor.fetchall()
                return rows

        except Error as e:
            msg = e.msg
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def execute_stored_procedure(self, sql, parameters=None):

        ## DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    if parameters is None:
                        cursor.callproc(sql)
                    else:
                        cursor.callproc(sql, parameters)
                    cursor.close()

        except Error as e:
            msg = e.msg
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
