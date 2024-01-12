import sys
import datetime
import boto3
import base64
from pyspark.sql import DataFrame, Row
from pyspark.context import SparkContext
from pyspark.sql.types import *
from pyspark.sql.functions import *
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

s3_kinesis_checkpoint = 's3://kinect-atlas-dev-raw/kinesis_emr_event_checkpoint/'
s3_kinesis_event = 's3:///kinect-atlas-dev-raw/kinesis_emr_event'
table_name = 'jeffrey_kinesis_streaming_service_events'
database = 'kinect_atlas_dev_ingestiondb'

def processBatch(data_frame, batchId):
    now = datetime.datetime.now()
    year = "{:0>4}".format(str(now.year))
    month = "{:0>2}".format(str(now.month))
    day = "{:0>2}".format(str(now.day))
    hour = "{:0>2}".format(str(now.hour))
    minute = "{:0>2}".format(str(now.minute))

    if (data_frame.count() > 0):
        dynamic_frame = DynamicFrame.fromDF(data_frame, glueContext, "from_data_frame")
        
        apply_mapping = ApplyMapping.apply(
            frame = dynamic_frame, 
            mappings = [("service_id", "int", "service_id", "int"), ("base_path", "string", "base_path", "string"), ("name", "string", "name", "string"), ("description", "string", "description", "string"), ("registration_ts", "string", "registration_ts", "string"), ("start_ts", "string", "start_ts", "string"), ("status", "string", "status", "string"), ("swagger_doc", "string", "swagger_doc", "string"), ("type", "string", "type", "string"), ("version", "string", "version", "string"), ("domain_id", "int", "domain_id", "int"), ("source_database", "string", "source_database", "string"), ("source_schema", "string", "source_schema", "string"), ("dataset_name", "string", "dataset_name", "string")], 
            transformation_ctx = "apply_mapping")
        
        path = f"{s3_kinesis_event}/ingest_year={year}/ingest_month={month}/ingest_day={day}/ingest_hour={hour}/"

        datasink1 = glueContext.write_dynamic_frame.from_options(
            frame = apply_mapping, 
            connection_type = "s3", 
            connection_options = {"path": path}, 
            format = "json", 
            transformation_ctx = "datasink1")
        
        print(f"S3 Path Location: {path}")
        print(f"Data Frame: {data_frame}")

datasource0 = glueContext.create_data_frame.from_catalog(
    database = database, 
    table_name = table_name, 
    transformation_ctx = "datasource0", 
    additional_options = {
        "startingPosition": "TRIM_HORIZON", 
        "inferSchema": "true"
    })

glueContext.forEachBatch(
    frame = datasource0, 
    batch_function = processBatch, 
    options = {
        "windowSize": "100 seconds", 
        "checkpointLocation": s3_kinesis_checkpoint
    })

job.commit()

