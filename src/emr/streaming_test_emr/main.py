from __future__ import print_function
import sys
import sys
import json
import logging
from datetime import datetime
import ast
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import *
from pyspark.storagelevel import StorageLevel
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log(msg):
    # change this as needed
    logger.warning(f"K I N E C T: {str(datetime.now())} {msg}")

if __name__ == "__main__":
    print(sys.argv[1:])
    app_name, stream_name, end_point_url, region_name, s3_loc, awsAccessKeyId, awsSecretKey, mode, df_format = sys.argv[1:]
    
    log("--------------------------------------------------------------")
    log(f"{str(datetime.now())} app_name: {app_name}")
    log(f'{str(datetime.now())} stream_name: {stream_name}')
    log(f'{str(datetime.now())} end_point_url: {end_point_url}')
    log(f'{str(datetime.now())} region_name: {region_name}')
    log(f'{str(datetime.now())} s3_loc: {s3_loc}')
    log(f'{str(datetime.now())} mode: {mode}')
    log(f'{str(datetime.now())} df_format: {df_format}')

    spark = SparkSession.builder.appName(app_name).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    log(f"After SparkSession.builder.appName('{app_name}').getOrCreate()")

    # read from kinesis
    if mode == 'local':
        log(f"Before spark.readStream: {mode}")
        df = spark \
            .readStream \
            .format("kinesis") \
            .option("streamName", stream_name) \
            .option("initialPosition", "latest") \
            .option("endpointUrl", end_point_url) \
            .option("region", region_name) \
            .option("awsAccessKeyId", awsAccessKeyId) \
            .option("awsSecretKey", awsSecretKey) \
            .load()
    else:
        log(f"Before spark.readStream: {mode}")
        df = spark \
            .readStream \
            .format("kinesis") \
            .option("streamName", stream_name) \
            .option("initialPosition", "latest") \
            .option("endpointUrl", end_point_url) \
            .option("region", region_name) \
            .load()

    log('After spark.readStream')
    df.printSchema()


    # process batch
    def foreach_batch_function(batch_df, epoch_id):
        log(f"in foreach_batch_function -> epoch_id: {epoch_id}, batch_df: {batch_df}")
        batch_df.show()
        # TODO add your processing logic for each micro-batch here


    if df_format == 'console':
        log(f"Before df.writeStream: {df_format}")
        df \
            .selectExpr('CAST(data AS STRING)') \
            .writeStream \
            .format("console") \
            .trigger(processingTime='10 seconds') \
            .outputMode('append') \
            .start() \
            .awaitTermination() 

    elif df_format == 'foreachBatch':
        df.writeStream \
            .foreachBatch(foreach_batch_function) \
            .trigger(processingTime='10 seconds') \
            .start() \
            .awaitTermination() 

