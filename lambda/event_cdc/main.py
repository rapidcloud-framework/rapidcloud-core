__author__ = "Jeffrey Planes"
__license__ = "MIT"


import os
import sys
import s3fs
import json
from datetime import datetime
import pandas as pd
import awswrangler as wr
import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
import traceback 

# for local testing of lambda layer modules
if os.environ.get('TEST_MODE') == 'true':
    print("sys.path.append(os.path.join(os.path.dirname(__file__), '..'))")
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from kc_governance import rules
from kc_common import s3
from kc_common import metadata
from kc_common import reformat

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']
JOB_NAME = 'event_cdc'

session = boto3.Session()
dynamodb_resource = session.resource('dynamodb')


def json_converter(obj):
    return str(obj)


def allow_processing(bucket, key):
    items = metadata.query('cdc_log', 'fqn', f's3://{bucket}/{key}')
    cdc_log_item = None
    if items:
        cdc_log_item = items[0]
        logger.info(json.dumps(cdc_log_item, indent=2, default=json_converter))  
    return True if cdc_log_item is None or cdc_log_item['status'] != 'processed' else False


def get_event_info(fqn):
    return metadata.query('event', 'fqn', fqn)[0]


def get_dataset_info(fqn):
    return metadata.query('dataset', 'fqn', fqn)[0]


def load_file(file):
    events = []
    with s3fs.S3FileSystem(anon=False).open(file, 'r') as json_file:
        events.append('{\"events\":[')
        for line in json_file.readlines():
            line_len = len(line)
            if line[line_len - 1] == ',': 
                events.append(line[0: line_len - 1])
            else:
                events.append(line)
        events.append(']}')
    return json.loads(''.join(events))


def df_info(df, msg, count=3):
    if df is not None:
        log_msg = f"{msg}: {len(df.index)}"
        logger.info(log_msg)
        logger.info(f"\n{df.iloc[0:count]}")
    else:
        logger.info(f"df is None; msg: {msg}")


def apply_rules_and_formatting(dataset, df):

    # apply rules (if applicable)
    dataset_rules = rules.get_rules_for_dataset(dataset)
    if dataset_rules:
        df = rules.process(dataset, df)
        df_info(df, "After processing rules:")

    # apply reformatting (if applicable)
    formats = reformat.get_formats_for_dataset(dataset)
    if formats:
        df = reformat.process(dataset, df)
        df_info(df, "After reformatting:")

    return df


def add_partitions(dataset):
    logger.info(f"Adding partition to metastore")
    wr.athena.repair_table(
        table=dataset, 
        database=f"{PROFILE}_rawdb",
        s3_output=f"s3://{PROFILE.replace('_','-')}-query-results-bucket/output/")


def process_database_events(bucket, key, dataset, events):
    logger.info(f"processing {len(events)} database events for {dataset}")
    
    event_info = get_event_info(f"{PROFILE}_{dataset}")
    logger.info(json.dumps(event_info, indent=2, default=json_converter))

    df = pd.DataFrame(events)
    # df_info(df, dataset)
    
    # add date info
    now = datetime.now()
    df['datalake_year'] = now.year
    df['datalake_month'] = now.month
    df['datalake_day'] = now.day

    # df_info(df, dataset)

    ## Drop metadata columns from the Dataframe
    df = df.drop(columns=['source_database','source_schema','dataset'])
    df_info(df, dataset)

    df = apply_rules_and_formatting(dataset, df)

    dataset_info = get_dataset_info(f"{PROFILE}_{dataset}")
    logger.info(json.dumps(dataset_info, indent=2, default=json_converter))

    destination = f"s3://{dataset_info['raw_location']}"
    logger.info(f"writing to {destination}")

    partition_cols = "cdc_action"
    if dataset_info['partitioned_by'] != 'n/a':
        partition_cols = f"{dataset_info['partitioned_by']},{partition_cols}"

    logger.info(f"partition_cols: [{partition_cols}]")
    wr.s3.to_parquet(
        df=df,
        path=destination,
        dataset=True,
        partition_cols=partition_cols.split(','),
        mode="append",
        compression="snappy" 
    ) 


def process_simple_events(bucket, key, dataset, events):
    logger.info(f"processing {len(events)} simple events for {dataset}")
    df = pd.DataFrame(events)
    
    # add date info
    now = datetime.now()
    df['datalake_year'] = now.year
    df['datalake_month'] = now.month
    df['datalake_day'] = now.day

    df_info(df, dataset)

    df = apply_rules_and_formatting(dataset, df)

    raw_bucket = f"{PROFILE.replace('_','-')}-raw"
    destination = f"s3://{raw_bucket}/events/{dataset}"
    logger.info(f"writing to {destination}")
    event_info = get_event_info(f"{PROFILE}_{dataset}")

    logger.info(f"partitions: [{event_info['partitions']}]")
    df.to_parquet(destination, engine='pyarrow', compression="snappy", partition_cols=event_info['partitions'].split(","), allow_truncated_timestamps=True)


def mark_dataset_status(bucket, key, dataset, status, count):
    dataset_status = {
        "status": status,
        "count": count,
        "update_timestamp": str(datetime.now()) 
    }
    metadata.mark_file(bucket, key, dataset, JOB_NAME, status, dataset_status=dataset_status)


def lambda_handler(event, context, test=False):
    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]    
        key = event['Records'][0]['s3']['object']['key']
        if allow_processing(bucket, key):

            # mark cdc_log as pending for the entire file
            metadata.mark_file(bucket, key, '', JOB_NAME, "pending")
            cdc_log = metadata.get_cdc_log(f's3://{bucket}/{key}')

            cdc_log_datasets = {
                "database": {},
                "simple": {}
            }

            events = {
                "database": {},
                "simple": {}
            }

            # split events by type and dataset
            events_from_file = load_file(f"{bucket}/{key}")
            for cdc_event in events_from_file['events']:
                dataset_name = cdc_event['dataset']
                event_type = "simple"
                if 'source_database' in cdc_event:
                    event_type = "database"

                if dataset_name not in events[event_type]:
                    events[event_type][dataset_name] = []
                    cdc_log_datasets[event_type][dataset_name] = {}
                events[event_type][dataset_name].append(cdc_event)

            # process database events
            for dataset, database_events in events['database'].items():
                if cdc_log['dataset_status'].get(dataset) is None or cdc_log['dataset_status'][dataset]['status'] != 'processed':
                    mark_dataset_status(bucket, key, dataset, 'pending', len(database_events))
                    process_database_events(bucket, key, dataset, database_events)
                    mark_dataset_status(bucket, key, dataset, 'processed', len(database_events))
                else:
                    logger.warn(f"{dataset} has already been processed from {cdc_log['fqn']}")

            # process simple events
            for dataset, simple_events in events['simple'].items():
                if cdc_log['dataset_status'].get(dataset) is None or cdc_log['dataset_status'][dataset]['status'] != 'processed':
                    mark_dataset_status(bucket, key, dataset, 'pending', len(simple_events))
                    process_simple_events(bucket, key, dataset, simple_events)
                    mark_dataset_status(bucket, key, dataset, 'processed', len(simple_events))
                else:
                    logger.warn(f"{dataset} has already been processed from {cdc_log['fqn']}")

            msg = f"{bucket}/{key} processed successfully"

            # mark cdc_log as completed for the entire file
            metadata.mark_file(bucket, key, '', JOB_NAME, "processed")

        else:
            msg = f"{bucket}/{key} has been processed already"
            logger.warn(msg) 

        
    except Exception as e:
        # mark cdc_log as failed for the entire file
        metadata.mark_file(bucket, key, '', JOB_NAME, "failed")

        logger.error(e)
        traceback.print_exc() 
        msg = e
    
    finally:
        logger.info(msg)
        return {
            'statusCode': 200,
            'body': msg
        }             


# testing
def main():
    # atlas_Service: 
    # events/2021/01/29/19/kinect_theia_1_main-1-2021-01-29-19-05-21-1abc9a1b-1797-4cc5-8d04-e68eb6b7a625
    
    # employees and transactions
    # events/2021/01/28/18/kinect_theia_1_main-1-2021-01-28-18-12-46-e2c982d0-e08f-4115-8718-a434849d4c26

    lambda_handler({
      "Records": [
        {
          "s3": {
            "bucket": {
              "name": "kinect-theia-1-ingestion"
            },
            "object": {
              "key": "events/2021/01/29/19/kinect_theia_1_main-1-2021-01-29-19-05-21-1abc9a1b-1797-4cc5-8d04-e68eb6b7a625"
            }
          }
        }
      ]
    }, '', True)


if __name__ == "__main__":
    main()
