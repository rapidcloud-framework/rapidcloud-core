__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import logging
from pyspark.context import SparkContext
from pyspark.sql.window import Window
from pyspark.sql import SQLContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.sql.functions import udf, struct,col
from awsglue.transforms import *
import boto3 
import botocore.session
from boto3.dynamodb.conditions import Key, Attr
import base64
import hashlib
import pickle

print(boto3.__version__)
print(botocore.__version__)

from data_scripts.kc_governance_spark import kc_rules

## s3://kinect-atlas-dev-utils/glue_site_packages/site-packages.zip,s3://kinect-atlas-dev-utils/etl_modules/modules.zip
## s3://kinect-atlas-dev-utils/java_jars/httpclient-4.5.9-javadoc.jar

##from cryptography.hazmat.bindings._padding import lib
##from cryptography.fernet import Fernet

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a Glue context
glue_context = GlueContext(SparkContext.getOrCreate())
spark = glue_context.spark_session
sql_context = SQLContext(spark)

args = getResolvedOptions(
    sys.argv,
    [
        "PROFILE",
        "JOB_NAME",
        "ENV_PREFIX",
        "TABLE",
        "ANALYSIS_LOCATION",
    ],
)

profile = args["PROFILE"]
job_name = args["JOB_NAME"]
env_prefix = args["ENV_PREFIX"]
table = args["TABLE"]
analysis_location = args["ANALYSIS_LOCATION"]
write_path = '{}'.format(analysis_location)

logger.info(f"Job Name: {job_name}")
logger.info(f"Environment: {env_prefix}")
logger.info(f"Table: {table}")

session = boto3.session.Session(region_name='us-east-1')
## session = pickle.loads(pickle.dumps(session))
kms_client = session.client('kms')
dynamodb_client = session.resource('dynamodb') 

## client = boto3.Session(profile_name='aws_cli_profile').client('client_x')

def encrypt_hash(secret):
    encrypted_value = hashlib.sha256(secret.encode()).hexdigest()
    return encrypted_value
 
def encrypt_v4(secret):
    key_id = f"alias/kinect_atlas_dev"
    ciphertext = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=bytes(str(secret), "utf-8"),
    )
    return base64.b64encode(ciphertext["CiphertextBlob"])     
    
    
def encrypt(secret):
    key_id = f"alias/kinect_atlas_dev"
    print('Inside encrypt function')
    print(f'Key Id: {key_id}')
    print(f'Secret: {secret}')
    plaint_text = secret.encode('utf-8') 
    print(f'Pain Text: {plaint_text}')
    print(type(plaint_text))
    print('Pickled Cipher Text: {pickle.loads(pickle.dumps(plaint_text))}')
    ciphertext = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaint_text,
    )
    print(f'Cipher Text: {ciphertext}')
    return base64.b64encode(ciphertext["CiphertextBlob"])
    
@udf("byte")  
def encrypt_v2(secret):
    plaint_text = secret.encode('utf-8')
    ciphertext = kms_client.encrypt(
        KeyId=f"alias/{profile}",
        Plaintext=pickle.loads(pickle.dumps(plaint_text)),
    )
    return base64.b64encode(ciphertext["CiphertextBlob"])

try:    
       
    ##encrypted_value = f.encrypt(string_value)
    ##encrypted_value = encrypt_hash(string_value)
    ##rules = get_rules_for_dataset(table)
    ##print(rules)
    string_value = 'Hello KMS!!'
    encrypted_value = encrypt_v2(string_value)
    ## encrypted_value = encrypt_v4(string_value)
    print(f'Encrypted Value: {encrypted_value}')
    
    ##rules = get_rules_for_dataset(table)
    ##print(rules)

except Exception as e:
    exception_message = "Exception occurred in {} ==> {}".format(job_name, e)
    print(exception_message)
    raise Exception(exception_message)