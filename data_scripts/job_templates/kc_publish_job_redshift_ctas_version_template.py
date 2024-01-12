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
        "iam_role",
        "env_prefix",
        "table_properties",
        "secret_name",
        "aws_region",
        "job_name_prefix",
        "custom_module_util",
        "sns_topic_arn",
    ],
)

iam_role = args["iam_role"]
env_prefix = args["env_prefix"]
redshift_db_name = '{}'
schema_name = '{}'
table_name = '{}'
table_properties = args["table_properties"]
secret_name = args["secret_name"]
aws_region = args["aws_region"]
job_name_prefix = args["job_name_prefix"]
glue_etl_toolkit_utils = args["custom_module_util"]
sns_topic_arn = args["sns_topic_arn"]
## Build the full S3 path with dataset name
job_name = '{}{}'.format(job_name_prefix,table_name) 
s3_bucket = '{}'
s3_path =  '{}/{}/'.format(s3_bucket,table_name)

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
    logger.log("INFO", "Redshift Database: {}".format(redshift_db_name))
    logger.log("INFO", "Schema Name: {}".format(schema_name))
    logger.log("INFO", "Table Name: {}".format(table_name))
    logger.log("INFO", "Table Properties: {}".format(table_properties))
    logger.log("INFO", "aws_region: {}".format(aws_region))
    logger.log("INFO", "Secret Name: {}".format(secret_name))

    aws_secret = Secrets(job_name, secret_name, aws_region)
    ## Get the secrets json
    aws_secrets = aws_secret.get_secret()

    redshift_conn = Redshift(job_name, aws_secrets)

    sql = '''
            TRUNCATE TABLE {}_stage.{};

            COPY {}_stage.{}
            FROM 's3://{}'
            FORMAT AS PARQUET
            IAM_ROLE '{}' ;
            
            DROP TABLE IF EXISTS {}.{} ; 
            
            CREATE TABLE {}.{} 
            {}
            AS 
            SELECT * 
            FROM {}_stage.{} ;
            
            TRUNCATE TABLE {}_stage.{};
        '''.format(s3_path,iam_role,table_properties)

    redshift_conn.execute_sql(sql)

    logger.log("INFO", "Redshift SQL Command {}".format(sql))
    ## Success Notification
    message = "The Glue Job: {} has successfully completed".format(job_name)
    sns.sendNotification(sns_topic_arn, message)

except Exception as e:
    exception_msg = "Exception occurred inside this glue etl ==> {} with this exception ==> {}".format(job_name,e)
    logger.log("ERROR", exception_msg)
    ## Failure Notification
    sns.sendNotification(sns_topic_arn, exception_msg)
    raise Exception(exception_msg)