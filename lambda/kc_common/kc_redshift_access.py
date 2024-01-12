__author__ = "Jeffrey Planes"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "jplanes@kinect-consulting.com"

import sys
import os
import json
import contextlib
import psycopg2
import psycopg2.extras
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Redshift:
    def __init__(self, job_name, aws_secrets):
        self.job_name = job_name
        self.aws_secrets = aws_secrets

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

        try:

            if len(self.aws_secrets) == 5:
                self.db_name = self.aws_secrets["dbname"]
                self.port_number = self.aws_secrets["port"]
                self.user = self.aws_secrets["user"]
                self.password = self.aws_secrets["password"]
                self.host = self.aws_secrets["host"]
            else:
                exception_message = "The Secrets JSON needs to have 6 elements!!"
                raise Exception(exception_message)

            logger.info( f"Host: {self.host}")
            logger.info( f"Database Name: {self.db_name}")
            logger.info( f"Port Number: {self.port_number}")
            logger.info( f"User ID: {self.user}")

        except Exception as e:
            msg = e.args
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_message)
            raise Exception(exception_message)

    def connect(self):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

        ## Build the redshift connection string
        connection = psycopg2.connect(
            dbname=self.db_name,
            host=self.host,
            port=self.port_number,
            user=self.user,
            password=self.password,
        )

        ## This sets the connection to autocommit on the transactions
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        return connection

    def execute_sql(self, sql, parameter=None):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

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
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_message)
            raise Exception(exception_message)

    def get_column_header(self, sql):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

        try:

            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    cursor.execute(sql)
                    #  Get the fields name (only once!)
                    columnHeader = [field[0] for field in cursor.description]
                return columnHeader

        except Exception as e:
            msg = e.args
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_message)
            raise Exception(exception_message)

    def return_dataset(self, sql, parameter=None):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        logger.info(f"Inside method: {function_id}")

        try:

            with contextlib.closing(self.connect()) as connection:
                with contextlib.closing(connection.cursor(cursor_factory=psycopg2.extras.DictCursor)) as cursor:
                    if parameter is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, parameter)
                    rows = cursor.fetchall()
                return rows

        except Exception as e:
            msg = e.args
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_message)
            raise Exception(exception_message)