import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import DataFrame, Row
import datetime
from awsglue import DynamicFrame

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

s3_kinesis_checkpoint = 's3://kinect-atlas-dev-raw/kinesis_emr_event_checkpoint/'
s3_kinesis_event = 's3:///kinect-atlas-dev-raw/kinesis_emr_event'
##table_name = 'jeffrey_kinesis_streaming_events'
table_name = 'jeffrey_kinesis_streaming_service_events'
database = 'kinect_atlas_dev_ingestiondb'
## @type: DataSource
## @args: [database = "kinect_atlas_dev_ingestiondb", table_name = "jeffrey_kinesis_streaming_events", additionalOptions = {"startingPosition": "TRIM_HORIZON", "inferSchema": "true"}, stream_type = kinesis]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_data_frame.from_catalog(database = database, table_name = table_name, transformation_ctx = "datasource0", additional_options = {"startingPosition": "TRIM_HORIZON", "inferSchema": "true"})
## @type: DataSink
## @args: [mapping = [("service_id", "int", "service_id", "int"), ("base_path", "string", "base_path", "string"), ("name", "string", "name", "string"), ("description", "string", "description", "string"), ("registration_ts", "string", "registration_ts", "string"), ("start_ts", "string", "start_ts", "string"), ("status", "string", "status", "string"), ("swagger_doc", "string", "swagger_doc", "string"), ("type", "string", "type", "string"), ("version", "string", "version", "string"), ("domain_id", "int", "domain_id", "int"), ("source_database", "string", "source_database", "string"), ("source_schema", "string", "source_schema", "string"), ("dataset_name", "string", "dataset_name", "string")], stream_batch_time = "100 seconds", stream_checkpoint_location = "s3://kinect-atlas-dev-raw/event/checkpoint/", connection_type = "s3", path = "s3://kinect-atlas-dev-raw/event", format = "json", transformation_ctx = "datasink1"]
## @return: datasink1
## @inputs: [frame = datasource0]
def processBatch(data_frame, batchId):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    if (data_frame.count() > 0):
        dynamic_frame = DynamicFrame.fromDF(data_frame, glueContext, "from_data_frame")
        apply_mapping = ApplyMapping.apply(frame = dynamic_frame, mappings = [("service_id", "int", "service_id", "int"), ("base_path", "string", "base_path", "string"), ("name", "string", "name", "string"), ("description", "string", "description", "string"), ("registration_ts", "string", "registration_ts", "string"), ("start_ts", "string", "start_ts", "string"), ("status", "string", "status", "string"), ("swagger_doc", "string", "swagger_doc", "string"), ("type", "string", "type", "string"), ("version", "string", "version", "string"), ("domain_id", "int", "domain_id", "int"), ("source_database", "string", "source_database", "string"), ("source_schema", "string", "source_schema", "string"), ("dataset_name", "string", "dataset_name", "string")], transformation_ctx = "apply_mapping")
        path = s3_kinesis_event + "/ingest_year=" + "{:0>4}".format(str(year)) + "/ingest_month=" + "{:0>2}".format(str(month)) + "/ingest_day=" + "{:0>2}".format(str(day)) + "/ingest_hour=" + "{:0>2}".format(str(hour)) + "/"
        datasink1 = glueContext.write_dynamic_frame.from_options(frame = apply_mapping, connection_type = "s3", connection_options = {"path": path}, format = "json", transformation_ctx = "datasink1")
        print('S3 Path Location: {}'.format(path))
        print('Data Frame: {}'.format(data_frame))
glueContext.forEachBatch(frame = datasource0, batch_function = processBatch, options = {"windowSize": "100 seconds", "checkpointLocation": s3_kinesis_checkpoint})
job.commit()