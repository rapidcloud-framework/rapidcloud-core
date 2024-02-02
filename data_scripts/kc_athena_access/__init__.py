__license__ = "MIT"

import json
import os
import sys
import contextlib
import pyathena as athena
from datetime import datetime
from  data_scripts.kc_logging import Logger

class Athena:
    def __init__(self, jobName, athenaOutput, credentitalName=None):
        self.jobName = jobName
        self.athenaOutput = athenaOutput
        self.credentitalName = credentitalName
        functionID = sys._getframe().f_code.co_name
        self.logger = Logger(self.jobName)


    def connect(self):
        functionID = sys._getframe().f_code.co_name
        if self.credentitalName is not None:
            return athena.connect(profile_name=self.credentitalName, s3_staging_dir=self.athenaOutput)
        else:
            return athena.connect(s3_staging_dir=self.athenaOutput)


    def executeSQL(self, sql, parameter=None):
        functionID = sys._getframe().f_code.co_name
        try:
            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    if parameter is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, parameter)
                    cursor.close()

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)


    def returnDataSet(self, sql, parameter=None):
        functionID = sys._getframe().f_code.co_name
        try:
            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    if parameter is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, parameter)
                    columns = self.getColumnHeader(sql)
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

                return rows

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)


    def getColumnHeader(self, sql):
        functionID = sys._getframe().f_code.co_name
        try:
            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    cursor.execute(sql)
                    #  Get the fields name (only once!)
                    columnHeader = [field[0] for field in cursor.description]
                return columnHeader

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
