__author__ = "Igor Royzis"
__license__ = "MIT"


import os
import sys
import json
import datetime
import time
import math
import threading
import boto3
import botocore
import pandas as pd
import pyarrow
import logging
import numpy as np
import traceback

from  boto3.dynamodb.conditions import Key, Attr

from kc_governance import rules
from kc_common import s3
from kc_common import metadata
from kc_common import reformat

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(message)s')
logger = logging.getLogger()

PROFILE = os.environ['PROFILE']
DEFAULT_PARTITIONS = "year,month,day,timestamp"
JOB_NAME = "cdc"
MAX_BATCH_SIZE_BYTES = 4 * 1024 * 1024 # 4MB
MAX_BATCH_SIZE_ROWS = 5000 
MIN_BATCHES = 1 # run N batches at the same time

class Cdc(object):

    def __init__(self):        
        session = boto3.Session()
        self.s3_resource = session.resource('s3')
        self.s3_client = session.client('s3')
        self.dynamodb_resource = session.resource('dynamodb')
        self.athena_client = session.client('athena')
        self.sns_client = boto3.client('sns')
        
        config = botocore.config.Config(
            read_timeout=900,
            connect_timeout=900,
            retries={"max_attempts": 0}
        )
        self.lambda_client = session.client("lambda", config=config)

        self.result_json = {}


    def json_converter(self, obj):
        return str(obj)


    def df_info(self, df, msg, count=3):
        if df is not None:
            log_msg = f"{msg}: {len(df.index)}"
            logger.info(log_msg)
            logger.info(df.iloc[0:count])
            self.result_json['log'].append(f"{datetime.datetime.now()}: {log_msg}")
        else:
            logger.info(f"df is None; msg: {msg}")


    def call_lambda(self, function_name, dataset_name, df_json, key):
        logger.info(f"Calling lambda function: {function_name}")
        payload = json.dumps({
            "dataset": dataset_name,
            "source_file_key": key,
            "data": df_json
        }, default=self.json_converter)
        return self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=payload
        )


    def enrich(self, df, dataset, key):
        enrich_name = dataset['enrich_name']
        total_size = len(df.index)
        batch_size = self.get_batch_size(df, total_size)
        batches = []
        batch_no = 1
        no_of_batches = math.ceil(total_size / batch_size)
        logger.info(f"{no_of_batches} batches")
        # total_size = 100
        # batch_size = 30
        for start_index in range(0, total_size, batch_size):
            batch_df = df.iloc[start_index : start_index + batch_size]
            self.df_info(batch_df, "Before enriching (batch)")

            batch_thread = threading.Thread(target=self.process_batch, args=(dataset, df, enrich_name, start_index, batch_size, batch_no, key, True))
            batches.append(batch_thread)
            batch_thread.start()
            logger.info(f"started thread for batch {batch_no} of {no_of_batches}, {batch_thread}")

            # wait for threads to finish before proceeding to next batch of N threads
            if batch_no % MIN_BATCHES == 0 or batch_no == no_of_batches:
                for batch_thread in batches:
                    batch_thread.join()
                    logger.info(f"joined thread: {batch_thread}")
                batches = []
            batch_no += 1    
            
                    
    def get_batch_size(self, df, total_size):
        logger.info(f"total_size: {total_size}")
        df_json = df.to_dict(orient='records')
        size = sys.getsizeof(json.dumps(df_json, default=self.json_converter))
        no_of_batches = size / MAX_BATCH_SIZE_BYTES
        if no_of_batches > 1:
            if no_of_batches < MIN_BATCHES:
                no_of_batches = MIN_BATCHES
            batch_size = len(df.index) / no_of_batches
            rounded_batch_size = int(round(batch_size, -3))
            if rounded_batch_size > MAX_BATCH_SIZE_ROWS:
                rounded_batch_size = MAX_BATCH_SIZE_ROWS
            logger.info(f"size: {size}")
            logger.info(f"max_batch_size_bytes: {MAX_BATCH_SIZE_BYTES}")
            logger.info(f"no_of_batches: {no_of_batches}")
            logger.info(f"batch_size: {rounded_batch_size}")
            return rounded_batch_size
        else:
            logger.info(f"batch_size: {total_size}")
            return total_size



    def process_batch(self, dataset, df, enrich_name, start_index, batch_size, batch_no, key, save_batch=True):
        batch = df.iloc[start_index : start_index + batch_size]
        batch = batch.replace(np.nan, '')

        self.df_info(batch, f"Batch {batch_no}: {start_index} - {start_index + batch_size}")
        df_json = batch.to_dict(orient='records')

        function_name = f"{PROFILE}_{enrich_name}"
        lambda_response = self.call_lambda(function_name, dataset['name'], df_json, key)
        logger.info(f"completed {function_name}")
        payload_json = json.loads(lambda_response['Payload'].read().decode("utf-8"))
        logger.info(f"got payload")

        if 'data' in payload_json:
            new_df = pd.DataFrame.from_records(payload_json['data'])
            self.df_info(new_df, "Batch result")
            if new_df is not None:
                new_df = new_df.astype(str)
                if save_batch:
                    self.save_to_destination(dataset, key, new_df, batch_no)

        else:
            logger.info(f"no data in response\n{payload_json}")
            return None


    def get_cdc_path(self, dataset):
        # get path prefix if cdc_type starts with 'cumulative_'
        cdc_path = None
        if dataset['cdc_type'].startswith("cumulative_"):
            key = self.result_json['source_key']
            end = key.find('/', key.find('/') + 1)
            cdc_year_start = end + 1
            cdc_year_end = key.find('/', cdc_year_start)
            cdc_year = key[cdc_year_start : cdc_year_end]
            cdc_path = f"cdc_year={cdc_year}"

            if dataset['cdc_type'] in ["cumulative_month", "cumulative_day"]:
                cdc_month_start = cdc_year_end + 1
                cdc_month_end = key.find('/', cdc_month_start)
                cdc_month = key[cdc_month_start : cdc_month_end]
                cdc_path += f"/cdc_month={cdc_month}"
            
                if dataset['cdc_type'] == "cumulative_day":
                    cdc_day_start = cdc_month_end + 1
                    cdc_day_end = key.find('/', cdc_day_start)
                    cdc_day = key[cdc_day_start : cdc_day_end]
                    cdc_path += f"/cdc_day={cdc_day}"
            
            logger.info(f"CDC path prefix: {cdc_path}")

        return cdc_path


    def save_to_destination(self, dataset, src_file_key, df, batch_no=1):
        try:
            # print("\n\n\n>>>")
            # logger.info(json.dumps(dataset, indent=2))
            # print("<<<\n\n\n")
            if 'raw_location' in dataset: # DMS
                destination = dataset['raw_location'] + '/'
            
            else: # semi-structured
                raw_bucket = f"{PROFILE.replace('_','-')}-raw"
                destination_prefix = f"semistructured/{dataset['name']}"
                
                # handle cumulative_[year|month|day] cdc
                cdc_path = self.get_cdc_path(dataset)
                if cdc_path is not None:
                    destination_prefix += f"/{cdc_path}"
                
                destination = f"s3://{raw_bucket}/{destination_prefix}/"

            # cleanup for cumulative cdc
            if 'cdc_type' in dataset: # semi-structured
                if dataset['cdc_type'] == "cumulative" and batch_no == 1:
                    logger.info(f"deleting {destination} for {dataset['cdc_type']} cdc")
                    s3.delete_folder(raw_bucket, destination_prefix)
                elif dataset['cdc_type'].startswith("cumulative_") and batch_no == 1:
                    logger.info(f"deleting {destination} for {dataset['cdc_type']} cdc")
                    s3.delete_folder(raw_bucket, destination_prefix)

            # save transformed data to raw bucket with partitions  
            now = datetime.datetime.now()
            obj_name = f"{self.result_json['file_name']}-{batch_no}.parquet"

            # create new column `cdc_batch_no`
            df['cdc_batch_no'] = batch_no

            ymd_partition = f"datalake_year={now.year}/datalake_month={now.month}/datalake_day={now.day}"
            if 'raw_location' in dataset: # DMS
                partitions = dataset['partitioned_by']
                if partitions == 'n/a':
                    partitions = DEFAULT_PARTITIONS
            else:
                partitions = dataset['partitions']

            if partitions == DEFAULT_PARTITIONS:
                destination += f"{ymd_partition}/{obj_name}"
                logger.info(f"saving {destination}")
                s3.to_parquet(df, destination)

            else:
                groupby_list = partitions.split(',')
                no_of_partitions = len(groupby_list)
                grouped_data = df.groupby(groupby_list)
                for group_partitions, group_df in grouped_data:
                    if no_of_partitions == 1:
                        destination += f"/{groupby_list[0]}={group_partitions}"
                    else:
                        for i in range(no_of_partitions):
                            destination += f"/{groupby_list[i]}={group_partitions[i]}"
                    
                    destination += f"/{ymd_partition}/{obj_name}"
                    logger.info(destination)
                    s3.to_parquet(group_df, destination)
                    # group_df.to_parquet(destination, engine='pyarrow',allow_truncated_timestamps=True)

            self.result_json['destination'].append(destination)

        except Exception as e:
                self.result_json['log'].append(e)
                logger.error(e.args)
                self.send_sns("FAILED")
                raise e


    def normalize_xml(self, xml_tree, bucket, key, dataset_name, file_name):
        pass


    def process_df(self, df, dataset_name, dataset, bucket, key):
        # clean up columns (make all lower case)
        # df.columns= df.columns.str.lower() # already done in s3.py

        # use first row as column headings
        if 'use_first_row_as_cols' in dataset and dataset['use_first_row_as_cols']:
            self.df_info(df, "Before renaming columns from first row")
            df.columns = df.iloc[0]
            df = df.drop(0)
            df = df.reset_index(drop=True)
            self.df_info(df, "After renaming columns from first row")

        # create new column `src_file_key` as the s3 key for this file
        df['src_file_key'] = key

        # apply rules (if applicable)
        dataset_rules = rules.get_rules_for_dataset(dataset_name)
        if dataset_rules:
            self.df_info(df, "Before processing rules")
            df = rules.process(df, dataset_rules)
            self.df_info(df, "After applying rules")

        # apply reformatting (if applicable)
        formats = reformat.get_formats_for_dataset(dataset_name)
        if formats:
            self.df_info(df, "Before reformatting")
            df = reformat.process(df, formats)
            self.df_info(df, "After reformatting")

        # enrich data (if applicable)
        if 'enable_enrich' in dataset and dataset['enable_enrich']:
            self.df_info(df, "Before enriching (all)")
            self.enrich(df, dataset, key)
            self.df_info(df, "After enriching (all)")
        else:
            self.save_to_destination(dataset, key, df)

        try:
            # add partition
            destination = self.result_json['destination'][0]

            if 'raw_location' in dataset: # DMS
                start_idx = len(dataset['raw_location'] + '/')
            
            else: # semi-structured
                raw_bucket = f"{PROFILE.replace('_','-')}-raw"
                start_idx = len(f"s3://{raw_bucket}/semistructured/{dataset_name}/")

            end_idx = destination.rindex("/")
            partition_key = []
            for partition in destination[start_idx:end_idx].split("/"):
                partition_key.append(partition)

            add_partitions = f"ALTER TABLE {PROFILE}_rawdb.{dataset_name.lower()} ADD IF NOT EXISTS PARTITION({','.join(partition_key)})"

            logger.info(f"Adding partitions: [{add_partitions}]")  
            output_loc = f"s3://{PROFILE.replace('_','-')}-query-results-bucket/output/"
            query_exec_id = self.athena_client.start_query_execution(
                QueryString = add_partitions,
                QueryExecutionContext = {
                    "Database": f"{PROFILE}_rawdb".lower()
                },
                ResultConfiguration={
                    'OutputLocation': output_loc
                }
            )

            query_resp_details = self.athena_client.get_query_execution(
                QueryExecutionId = query_exec_id['QueryExecutionId']
            )
            logger.info(json.dumps(query_resp_details, indent=2, default=self.json_converter))
            

        except Exception as e:
            # mark cdc_log as failed
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "failed", error_msg=str(e))
            self.result_json['log'].append(e)
            logger.error(e.args)
            raise e


    def process_file(self, bucket, key):
        started = time.time()
        logger.info(f"processing {bucket}/{key}")
        self.result_json.clear()
        self.result_json['log'] = []
        self.result_json['destination'] = []
        self.result_json['started'] = datetime.datetime.now()
        self.result_json['source_bucket'] = bucket
        self.result_json['source_key'] = key
    
        try:
            # get dataset info 
            if 'semistructured' in key:
                # key format for semi-structured: semistructured/dataset_name/
                parsed = key.split("/")
                dataset_name = parsed[1]
                dataset_fqn = f"{PROFILE}_{dataset_name}"
                dataset = metadata.query('dataset_semi_structured', 'fqn', dataset_fqn)[0]
                dataset_type = "dataset_semi_structured"

            elif 'databases' in key:
                # key format for database: databases/schema/dataset_name/
                # "key": "databases/theia_sample/guest/orders/LOAD00000001.csv"
                parsed = key.split("/")
                source_database = parsed[1]
                source_schema = parsed[2]
                dataset_name = parsed[3]
                dataset = metadata.scan('dataset', {
                    "source_database": source_database,
                    "source_schema": source_schema,
                    "source_table": dataset_name
                })[0]
                dataset_type = "dataset"

                # cdc action for timestamp based dms tasks
                cdc_action = None
                if '/action=i' in key:
                    cdc_action = 'i'
                elif '/action=u' in key:
                    cdc_action = 'u'

            else:
                logger.warn(f"unknown dataset type: {key}")
                return

            logger.info("dataset:")
            logger.info(json.dumps(dataset, indent=2, default=self.json_converter))
            self.result_json['dataset_name'] = dataset_name

            # mark cdc_log as pending
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "pending")

            # file name
            start = key.rfind('/') + 1
            file_name = key[start:]
            self.result_json['file_name'] = file_name

            # read from S3. `data` is a panda DataFrame
            if dataset_type == "dataset": # from DMS
                df = s3.read_csv(bucket, key) # replace with `read_parquet`
                if cdc_action is not None: # timestamp based dms task
                    df['cdc_action'] = cdc_action
            elif dataset['format'] == 'csv':
                df = s3.read_csv(bucket, key, dataset['separator_char'])
            elif dataset['format'] in ['xls', 'xlsx']:
                df = s3.read_excel(bucket, key, dataset['sheet_name'])
            elif dataset['format'] == 'json':
                # Temporary fix for json with nested lists
                obj = self.s3_client.get_object(Bucket=bucket, Key=key)
                data = json.loads(obj['Body'].read())
                df = pd.json_normalize(data)
                df.fillna('', inplace=True) # TODO review
                # df = s3.read_json(bucket, key)
            elif dataset['format'] == 'xml' and not dataset['normalize']:
                # Temporary fix before upgrade to new version
                # df = s3.read_xml(bucket, key)
                obj = self.s3_resource.Object(bucket, key)
                df = pd.read_xml(obj.get()['Body'].read().decode('utf-8'))
                s3.sanitize_col_names(df)
                
            # elif dataset['format'] == 'xml' and dataset['normalize'] and dataset['normalize_config'] is not None:
            #         xml_tree = s3.read_xml_as_tree(bucket, key, dataset['path_to_data'])
            #         dfs = self.normalize_xml(xml_tree, bucket, key, dataset_name, file_name)
                # for k, df in dfs.items():
                #     self.process_df(df, dataset_name, k, dataset, bucket, key)

            # process df
            self.process_df(df, dataset_name, dataset, bucket, key)

            # mark file as processed    
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "processed", destination=self.result_json['destination'])

        except Exception as e:
            # mark cdc_log as failed
            metadata.mark_file(bucket, key, dataset_name, JOB_NAME, "failed", error_msg=str(e))
            self.result_json['log'].append(e)
            logger.error("ERROR:")
            logger.error(e.args)
            self.send_sns("FAILED")
            traceback.print_exc()
            raise e

        self.result_json['finished'] = datetime.datetime.now()
        self.result_json['duration'] = time.time() - started
        
        # send completion notification
        self.send_sns("SUCCESS")


    def send_sns(self, status):
        for topic in self.sns_client.list_topics()['Topics']:
            if f"{PROFILE}_general_notifications" in topic['TopicArn']:
                self.sns_client.publish(
                    TopicArn=topic['TopicArn'],
                    Subject=f"{status} - {JOB_NAME} / {self.result_json['dataset_name']}",    
                    Message=json.dumps(self.result_json, indent=2, default=self.json_converter)    
                )




def lambda_handler(event, context, test=False): 
    logger.info(json.dumps(event, indent=2))
    for record in event['Records']:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]  
        key = record['s3']['object']['key'] 
        if test or not metadata.is_file_loaded(f"s3://{bucket}/{key}"):
            Cdc().process_file(bucket, key)
        else:
            logger.info("this file has already been processed")


TEST_DMS_INGESTION = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2021-10-18T18:19:21.670Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AWS:AROATTKLAGPXZW3QQE3KS:dms-session-for-replication-engine"
                },
                "requestParameters": {
                    "sourceIPAddress": "54.160.59.41"
                },
                "responseElements": {
                    "x-amz-request-id": "EA5C88HE3AHBMWPA",
                    "x-amz-id-2": "W1Q5AAT3RNtCUTbYMbKE1kolXsc62YH8ymcufCNYLDqr0FkLKj32PevXT4XqjSH/6c+yvKEWsAgP6ajSLvShqsF6qJvkVytt"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "tf-s3-lambda-2021060818254264810000001d",
                    "bucket": {
                        "name": "kinect-theia-2-ingestion",
                        "ownerIdentity": {
                            "principalId": "A2HE2OAPHXSZ2H"
                        },
                        "arn": "arn:aws:s3:::kinect-theia-2-ingestion"
                    },
                    "object": {
                        "key": "databases/theia_sample/guest/staffs/LOAD00000001.parquet",
                        "size": 2521,
                        "eTag": "72c7ea93f0848c4dc396379871a656f1",
                        "sequencer": "00616DBAA99EDF22A6"
                    }
                }
            }
        ]
    }


TEST_SEMIFILE_INGESTION = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2021-10-18T18:52:09.530Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDATTKLAGPXQKS3G3YUL'}, 'requestParameters': {'sourceIPAddress': '170.250.185.254'}, 'responseElements': {'x-amz-request-id': 'AQ2RH7XV6DK06RDZ', 'x-amz-id-2': 'WCKOslMNSGceBgpIVG7WeSvJrzwu041vuXn/U2Dhwk0g0jUXPGHHB6OpIEq2hgi5+sZ5Uv2WSn4hOg3UygpCqMp7I2ZeQiR5'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'tf-s3-lambda-2021060818254264810000001d', 'bucket': {'name': 'kinect-theia-2-ingestion', 'ownerIdentity': {'principalId': 'A2HE2OAPHXSZ2H'}, 'arn': 'arn:aws:s3:::kinect-theia-2-ingestion'}, 'object': {'key': 'semistructured/benefits/benefits_sample.csv', 'size': 147, 'eTag': '1dda1668b368a80da59b5a91281c49df', 'sequencer': '00616DC25977641BD3'}}}]}



def main():
    # lambda_handler(TEST_DMS_INGESTION, '', True)
    # lambda_handler(TEST_SEMIFILE_INGESTION, '', True)
    pass

if __name__ == "__main__":
    main()
