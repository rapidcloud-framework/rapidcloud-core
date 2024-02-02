__license__ = "MIT"

import sys
import os
import sys
import json
import boto3
import datetime
import contextlib
import zipfile
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time

from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from data_scripts.kc_logging import Logger
from data_scripts.kc_aws_secrets import Secrets

## Python Library Path Property
## s3://kinect-atlas-dev-utils/etl_modules/modules.zip

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "CATALOG_DATABASE",
        "CATALOG_DATASET",
        "JDBC_CONNECTION",
        "SCHEMA_TARGET", 
        "DATABASE_TARGET",
        "SECRET"
    ],
)

## DECLARATION SECTION
job_name = args["JOB_NAME"]
catalog_database = args["CATALOG_DATABASE"] 
catalog_dataset = args["CATALOG_DATASET"] ## This is used for both the analysisdb catalog dataset and the target table
jdbc_connection = args["JDBC_CONNECTION"]
schema_target = args["SCHEMA_TARGET"]
database_target = args["DATABASE_TARGET"]
secret = args["SECRET"]
## Derive the variables based upon another variable
schema_stage = '{}_stage'.format(schema_target)
table = catalog_dataset ## Ths catalog_dataset is used for the target table too

table_stage = "{}.{}".format(schema_stage,table)
table_target = "{}.{}".format(schema_target,table)
truncate_table_stage = "TRUNCATE TABLE {} ;".format(table_stage)
##truncate_table_target = "TRUNCATE TABLE {} ;".format(table_target)

## Instantiate the logger
logger = Logger(job_name)

logger.log("INFO", "Job Name: {}".format(job_name))           
logger.log("INFO", "Catalog Database: {}".format(catalog_database))           
logger.log("INFO", "Catalog Dataset: {}".format(catalog_dataset))           
logger.log("INFO", "Jdbc Connection: {}".format(jdbc_connection))           
logger.log("INFO", "Target Database: {}".format(database_target))    
logger.log("INFO", "Schema Target: {}".format(schema_target))           
logger.log("INFO", "Schema Stage: {}".format(schema_stage))           
logger.log("INFO", "Staging Table: {}".format(table_stage))
logger.log("INFO", "Target Table: {}".format(table_target))
logger.log("INFO", "Secret Name: {}".format(secret))

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(job_name, args)

def get_my_secret(job_name,secret):
    
    ##DECLARATION SECTION
    functionID = sys._getframe().f_code.co_name
    logger.log("INFO", "Inside function: {}".format(functionID))
    
    aws_secret = Secrets(job_name, secret)
    secret_json = aws_secret.get_secret()
    
    return secret_json
        
def get_connection(host,user,password,dbname,port):
    
    ##DECLARATION SECTION
    functionID = sys._getframe().f_code.co_name
    logger.log("INFO", "Inside function: {}".format(functionID))
    
    db_conn = MySQLdb.connect(host=host,user=user,password=password,database=dbname,port=port)
    
    return db_conn

try:

    secret_json = get_my_secret(job_name,secret)
    logger.log("INFO", "Secret Json: {}".format(secret_json))
    
    if len(secret_json) == 5:
        dbname = secret_json["dbname"]
        host = secret_json["host"]
        password = secret_json["password"]
        port = secret_json["port"]
        user = secret_json["user"]
    else:
        exception_message = "The Secrets JSON needs to have 5 elements"
     
    ## Get connection object              
    db_conn = get_connection(host,user,password,dbname,port)
    # prepare a cursor object using cursor() method
    cursor = db_conn.cursor()
    
    logger.log("INFO", "Truncate Stage Table SQL: {}".format(truncate_table_stage)) 
    try:
        cursor.execute(truncate_table_stage)
        # Commit your changes in the database
        db_conn.commit()
    except Exception as e:
        exception_message = "Exception occurred in {} ==> {}".format(job_name, e)
        # Rollback in case there is any error
        db_conn.rollback()
        raise Exception(exception_message)
    
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = catalog_database, table_name = catalog_dataset, transformation_ctx = "datasource0")
    
    ##applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("concat_business_key", "string", "concat_business_key", "string"), ("base_path", "string", "base_path", "string"), ("description", "string", "description", "string"), ("domain_id", "int", "domain_id", "int"), ("name", "string", "name", "string"), ("registration_ts", "timestamp", "registration_ts", "timestamp"), ("service_id", "int", "service_id", "int"), ("start_ts", "string", "start_ts", "string"), ("status", "string", "status", "string"), ("swagger_doc", "string", "swagger_doc", "string"), ("type", "string", "type", "string"), ("version", "string", "version", "string"), ("cdc_action", "string", "cdc_action", "string")], transformation_ctx = "applymapping1")
    
    resolvechoice2 = ResolveChoice.apply(frame = datasource0, choice = "make_cols", transformation_ctx = "resolvechoice2")
    dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
    connection_option_string =  '''
                                "dbtable":"{}","database":"{}"
                                '''.format(table_stage,database_target)
    
    logger.log("INFO", "Connection Option String: {}".format(connection_option_string))    
    
    datasink4 = glueContext.write_dynamic_frame.from_jdbc_conf(frame = dropnullfields3, catalog_connection = jdbc_connection, connection_options =eval('!' + connection_option_string + '^'), transformation_ctx = "datasink4")
    
    replace_insert_sql = '''
                                    REPLACE INTO {} SELECT * FROM {} ;
                                    '''.format(table_target ,table_stage) 

    logger.log("INFO", "Replace Into SQL: {}".format(replace_insert_sql)) 
    try:
        cursor.execute(replace_insert_sql)
        # Commit your changes in the database
        db_conn.commit()
    except Exception as e:
        exception_message = "Exception occurred in {} ==> {}".format(job_name, e)
        # Rollback in case there is any error
        db_conn.rollback()
        raise Exception(exception_message)

    # disconnect from server
    db_conn.close()
    
    job.commit()

except Exception as e:
    exception_message = "Exception occurred in {} ==> {}".format(job_name, e)
    logger.log("ERROR", exception_message)
    raise Exception(exception_message)    