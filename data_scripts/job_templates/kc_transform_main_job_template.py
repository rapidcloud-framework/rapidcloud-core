__license__ = "MIT"

import os
import sys
import json
import boto3
import datetime
import contextlib
import logging
import awswrangler as wr
import pandas as pd
from awsglue.utils import getResolvedOptions

logging.basicConfig()
logger = logging.getLogger("transform")
logger.setLevel(logging.INFO)

def df_info(df, msg, count=3):
    logger.info(f"{msg}: {len(df.index)}")
    logger.info(df.iloc[0:count])

try:
    args = getResolvedOptions(sys.argv,[
            "job_name",
            "env",
            "region",
            "source_bucket",
            "target_bucket",
            "source_glue_database",
            "target_glue_database"
        ]
    )

    job_name = args['job_name']
    env = args['env']
    region = args['region']
    source_bucket = args['source_bucket']
    target_bucket = args['target_bucket']
    source_glue_database = args['source_glue_database']
    target_glue_database = args['target_glue_database']

    logger.info(f"job_name: {job_name}")
    logger.info(f"region: {region}")
    logger.info(f"source_location: {source_bucket}")
    logger.info(f"target_location: {target_bucket}")
    logger.info(f"source_glue_database: {source_glue_database}")
    logger.info(f"target_glue_database: {target_glue_database}")

    # this job does nothing and only serves as a trigger mechanism for all transformations
    logger.info(f"The Glue Job: {job_name} has successfully completed")

except Exception as e:
    exception_msg = f"Exception occurred inside this glue etl ==> {job_name} with this exception ==> {e}"
    logger.log("ERROR", exception_msg)
    raise Exception(exception_msg)