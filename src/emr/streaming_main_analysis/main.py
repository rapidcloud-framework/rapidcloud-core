from __future__ import print_function

import sys
import os
import sys
import json
import argparse
import logging
import uuid 
from datetime import datetime

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.storagelevel import StorageLevel
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log(msg): 
    logger.warning(f"K I N E C T: {str(datetime.now())} {msg}")

if __name__ == "__main__":
    app_name, stream_name, end_point_url, region_name, s3_loc, awsAccessKeyId, awsSecretKey = sys.argv[1:]
    
    log("--------------------------------------------------------------")
    log(f"{str(datetime.now())} app_name: {app_name}")
    log(f'{str(datetime.now())} stream_name: {stream_name}')
    log(f'{str(datetime.now())} end_point_url: {end_point_url}')
    log(f'{str(datetime.now())} region_name: {region_name}')
    log(f'{str(datetime.now())} s3_loc: {s3_loc}')

    spark = SparkSession.builder.appName(app_name).getOrCreate()

    # read from kinesis
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
    df.printSchema()

    # print to console
    df.writeStream \
        .format("console") \
        .trigger(processingTime='10 seconds') \
        .start() \
        .awaitTermination() 

    # process row
    # def foreach_row_function(row):
    #     log(f"in foreach_row_function(..)")
    #     # log(str(row))

    # query = df.writeStream \
    #     .foreach(foreach_row_function) \
    #     .trigger(processingTime='5 seconds') \
    #     .start() \
    #     .awaitTermination() 

    # process batch
    # def foreach_batch_function(batch_df, epoch_id):
    #     log(f"in foreach_batch_function(..)")

    # df.writeStream \
    #     .foreachBatch(foreach_batch_function) \
    #     .start() \
    #     .awaitTermination() 



