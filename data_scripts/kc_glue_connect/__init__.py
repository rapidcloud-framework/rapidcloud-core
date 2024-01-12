__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import boto3
import psycopg2
import psycopg2.extras
from    data_scripts.kc_logging import Logger


class GlueConnection:
   
    def __init__(self, job_name, aws_service='glue',region_name='us-east-1',seperator='~~~~',credential_name=None):
        self.job_name = job_name
        self.aws_service = aws_service
        self.region_name = region_name
        self.credential_name = credential_name
        self.seperator = seperator 

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        self.logger = Logger(self.job_name)
        self.logger.log("INFO", f"Inside method: {function_id}")

        try:

            if self.credential_name is not None:
                session = boto3.session.Session(region_name=self.region_name,profile_name=self.credential_name)
            else:
                session = boto3.session.Session(region_name=self.region_name)

            self.glue_client = session.client(self.aws_service)

            self.logger.log("INFO", f"Job Name: {self.job_name}")
            self.logger.log("INFO", f"AWS Service: {self.aws_service}")
            self.logger.log("INFO", f"Region Name: {self.region_name}")
            self.logger.log("INFO", f"Credential Name: {self.credential_name}")

        except Exception as e:
            msg = e.args
            exception_message = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exception_message)
            raise Exception(exception_message)

    def  get_glue_connection(self,connection_name):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name      

        self.logger.log("INFO", f"Inside method: {function_id}")

        response = self.glue_client.get_connection(Name=connection_name)

        connection_properties = response['Connection']['ConnectionProperties']
        url = connection_properties['JDBC_CONNECTION_URL']
        url_list = url.split("/")

        host = "{}".format(url_list[-2][:-5])        
        database = "{}".format(url_list[-1])
        user = "{}".format(connection_properties['USERNAME'])
        pwd = "{}".format(connection_properties['PASSWORD'])
        port = url_list[-2][-4:]

        self.logger.log("INFO", f"User: {user}")
        self.logger.log("INFO", f"Host: {host}")
        self.logger.log("INFO", f"Port: {port}")
        self.logger.log("INFO", f"Redshift Database: {database}")

        connection_string = f"{host}{self.seperator}{database}{self.seperator}{user}{self.seperator}{pwd}{self.seperator}{port}"

        return connection_string

    def get_redshift_connection(self,connection_name):

        ##DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {function_id}")

        connection_string = self.get_glue_connection(connection_name)
        ## Get the connection list
        connection_list = connection_string.split(self.seperator)
        connection_list_length = len(connection_list)

        if connection_list_length == 5:
               ## Build the redshift connection string
                connection = psycopg2.connect(
                    dbname=connection_list[1],
                    host=connection_list[0],
                    port=connection_list[4],
                    user=connection_list[2],
                    password=connection_list[3],
                )
        else:
            exception_message = "The connection needs 5 properties"
            raise Exception(exception_message)

        ## This sets the connection to autocommit on the transactions
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        return connection
