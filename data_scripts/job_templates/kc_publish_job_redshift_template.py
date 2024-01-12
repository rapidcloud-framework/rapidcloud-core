__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

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

os.environ["PYTHON_EGG_CACHE"] = "/tmp/totallynew"

from awsglue.utils import getResolvedOptions

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "IAM_ROLE",
        "ENV_PREFIX",
        "SCHEMA_NAME",
        "TABLE_NAME",
        "AWS_REGION",
        "PROFILE",
        "ANALYSIS_LOCATION",
    ],
)

job_name = args["JOB_NAME"]
iam_role = args["IAM_ROLE"]
env_prefix = args["ENV_PREFIX"]
schema_name = args["SCHEMA_NAME"]
table_name = args["TABLE_NAME"]
aws_region = args["AWS_REGION"]
profile = args["PROFILE"]
analysis_location = args["ANALYSIS_LOCATION"]
secret_name = '{}/redshift_cluster/main/connection_string'.format(profile)
glue_etl_toolkit_utils = 'modules.zip'
## Build the full S3 path with dataset name
s3_path =  '{}'.format(analysis_location)

## BEGIN These Python functions are used to locate and unzip the custom etl toolkit utils class modules
def _find(file_name):

    try:

        for dirname in sys.path:
            candidate = os.path.join(dirname, file_name)
            if os.path.isfile(candidate):
                return candidate
        raise Exception("Can't find file {}".format(file_name))

    except Exception as e:
        exception_message = "Exception occurred inside this glue etl ==> {} with this exception ==> {}".format(job_name,e)
        print("ERROR: {}".format(exception_message))
        raise e


def findFile(file_name):
    return _find(file_name)


print(findFile(glue_etl_toolkit_utils))

zip_ref = zipfile.ZipFile(findFile(glue_etl_toolkit_utils), "r")
print(os.listdir("."))
zip_ref.extractall("/tmp/packages")
zip_ref.close()

sys.path.insert(0, "/tmp/packages")

## END These Python functions are used to locate and unzip the custom etl toolkit utils class modules

from data_scripts.kc_logging import Logger
from data_scripts.kc_aws_secrets import Secrets
from data_scripts.kc_redshift_access import Redshift
from data_scripts.kc_notification import Notification

## Instantiate the Notification
sns = Notification("sns", aws_region)

try:

    logger = Logger(job_name)
    logger.log("INFO", "Inside job: {}".format(job_name))
    logger.log("INFO", "IAM Role: {}".format(iam_role))
    logger.log("INFO", "S3 Full Path: {}".format(s3_path))
    logger.log("INFO", "Schema Name: {}".format(schema_name))
    logger.log("INFO", "Table Name: {}".format(table_name))
    logger.log("INFO", "aws_region: {}".format(aws_region))
    logger.log("INFO", "Secret Name: {}".format(secret_name))

    aws_secret = Secrets(job_name, secret_name, aws_region)
    ## Get the secrets json
    aws_secrets = aws_secret.get_secret()

    redshift_conn = Redshift(job_name, aws_secrets)

    sql = '''
            TRUNCATE TABLE {}_stage.{};

            COPY {}_stage.{}
            FROM '{}'
            FORMAT AS PARQUET
            IAM_ROLE '{}' ;
            
            TRUNCATE TABLE {}.{} ; 
            
            INSERT INTO {}.{} 
            SELECT * 
            FROM {}_stage.{} ;
            
            TRUNCATE TABLE {}_stage.{};
        '''.format(schema_name,table_name,schema_name,table_name,s3_path,iam_role,schema_name,table_name,schema_name,table_name,schema_name,table_name,schema_name,table_name)

    redshift_conn.execute_sql(sql)

    logger.log("INFO", "Redshift SQL Command {}".format(sql))
    ## Success Notification
    message = "The Glue Job: {} has successfully completed".format(job_name)
    logger.log("INFO", message)

except Exception as e:
    exception_msg = "Exception occurred inside this glue etl ==> {} with this exception ==> {}".format(job_name,e)
    logger.log("ERROR", exception_msg)
    raise Exception(exception_msg)