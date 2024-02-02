__license__ = "MIT"

import sys
from pyspark.context import SparkContext
from pyspark.sql.window import Window
from pyspark.sql import SQLContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.transforms import *

# Create a Glue context
glue_context = GlueContext(SparkContext.getOrCreate())
spark = glue_context.spark_session
sql_context = SQLContext(spark)

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "ENV_PREFIX",
        "TABLE",
        "ANALYSIS_LOCATION",
    ],
)

job_name = args["JOB_NAME"]
env_prefix = args["ENV_PREFIX"]
table = args["TABLE"]
analysis_location = args["ANALYSIS_LOCATION"]
write_path = '{}'.format(analysis_location)

print("Job: {}".format(job_name))
print("Environment: {}".format(env_prefix))
print("Table: {}".format(table))

def query(table, key_attr, key_value):
    return dynamodb_resource.Table(table).query(
        KeyConditionExpression=Key(key_attr).eq(key_value)
    )['Items']

def get_transform_log(fqn):
    items = query("transform_log", "fqn", fqn)
    logger.info(json.dumps(items, indent=2))
    if items:
        return items[0]
    return None


def start_transform(env, dataset_name, job_name, job_arguments):
    fqn = f"{env}_{dataset_name}_{time.time() * 1000}"
    item = {
        "fqn": fqn,
        "profile": env,
        "dataset_name": dataset_name,
        "job_name": job_name,
        "job_arguments": job_arguments,
        "status": "started",
        "update_timestamp": str(datetime.now())            
    }
    put_item("transform_log", item)  
    return item


def update_transform(fqn, status, destination=[], error_msg=None):
    items = query("transform_log", "fqn", fqn)
    if items:
        item = items[0]
        item['status'] = status
        item['update_timestamp'] = str(datetime.now())
        item['destination'] = destination
        if error_msg is not None:
            item['error_msg'] = error_msg
    put_item("transform_log", item)  
    return item

    
try:

        sql =  """
                  {}
                  """

        ## Notes:
        ## 1. Join your cte's based upon the JOIN criteria
        ## 2. The final query will need to be defined, so that the Glue Spark job can execute and produce a dataset in the appropriate S3 analysis bucket.
        ## Example Final cte query --> SELECT * FROM cte_final Please do NOT include any semi-columns (;) in your Spark SQL

        df = sql_context.sql(sql)
        print("writing to {}".format(write_path))
        df.write.mode("overwrite").parquet(write_path)

except Exception as e:
    exception_message = "Exception occurred in {} ==> {}".format(job_name, e)
    print(exception_message)
    raise Exception(exception_message)