__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import sys
import json
import boto3
import logging
import os
import uuid 
import string
import base64
import datetime
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']
session = boto3.Session()


def df_info(df, msg, count=10):
    print(f"{msg}: {len(df.index)}")
    print(df.iloc[0:count])


def remove_timezone(dt, format):
    if dt is not None:
        return dt[0: len(format) - 1]
    return None


def split_fullname(f, df, attr):
    if f['from_format'].replace(' ','') == 'l,f':
        df[['x_last_name', 'x_first_name']] = df[attr].str.split(",", expand=True)
        df['x_last_name'] = df['x_last_name'].str.strip()
        df['x_first_name'] = df['x_first_name'].str.strip()
        # df_obj = df.select_dtypes(['object'])
        # df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    elif f['from_format'] == 'f l':
        df[['x_first_name','x_last_name']] = df[attr].str.split(n=1, expand=True)
        df['x_last_name'] = df['x_last_name'].str.strip()
        df['x_first_name'] = df['x_first_name'].str.strip()
        # df_obj = df.select_dtypes(['object'])
        # df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())


def split_datetime(f, df, attr, from_format):
    print(f"df[attr].dtype.name = {df[attr].dtype.name}")
    if df[attr].dtype.name != 'datetime64[ns]':
        df[attr] = df[attr].apply(remove_timezone, format=from_format)
    df[f'x_{attr}'] = pd.to_datetime(df[attr], errors='coerce', format=from_format).dt.date
    df[f'x_{attr}_time'] = pd.to_datetime(df[attr], errors='coerce', format=from_format).dt.time


def reformat(value, attr_type, from_format, to_format):
    if attr_type == 'date':
        try:
            date_obj = datetime.datetime.strptime(str(value), from_format)
            return date_obj.strftime(to_format)
        except:
            return value

    elif attr_type == 'amount':
        if from_format == "\$*" and to_format == "*":
            return value.replace('$', '')

    elif to_format == 'string':
        return str(value)

    return value


def eval_stmt(value, attr, to_format):
    return eval(to_format.replace(attr, f"\"{value}\""))


def get_formats_for_dataset(dataset_name):
    logger.info(f"getting formats for dataset {PROFILE}/{dataset_name}")
    formats = session.resource('dynamodb').Table('format').scan(        
        FilterExpression=Attr('dataset').eq(dataset_name) & Attr('profile').eq(PROFILE)
    )['Items']
    logger.info(json.dumps(formats, indent=2))
    return formats


def process(df, formats):
    for f in formats:
        logger.info("applying reformatting:")
        logger.info(json.dumps(f, indent=2))
        attr = f['attr'].lower()
        if f['attr_type'] == 'fullname' and f['to_format'] == 'split':
            split_fullname(f, df, attr)
        elif f['attr_type'] == 'date' and f['to_format'] == 'split':
            split_datetime(f, df, attr, f['from_format'])
        elif f['from_format'] == 'eval':
            df[attr] = df[attr].apply(eval_stmt, attr=attr, to_format=f['to_format'])
        else:
            df[attr] = df[attr].apply(reformat, attr_type=f['attr_type'], from_format=f['from_format'], to_format=f['to_format'])
    return df


if __name__ == "__main__":

    # df = pd.read_xml("/Users/iroyzis/Workspace/kinect/clients/PinelasCounty/opioid/data/JIMS_RELEASED.XML")

    df = pd.read_excel("/Users/iroyzis/Workspace/kinect/clients/PinelasCounty/workspace/human-services-opioids/data/ems_suspected_overdoses_with_narcan/1_2_3_for_102021.xlsx", sheet_name="3")

    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('#', '_no')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace('(', '_')
    df.columns = df.columns.str.replace(')', '')
    df.columns = df.columns.str.replace('__', '_')

    df = df[['name','dob']]
    df_info(df, 'before')
    df.info(verbose=True)

    df['dob'] = df['dob'].apply(reformat, attr_type='date', from_format="%m/%d/%Y", to_format="%Y-%m-%d")

    # df[['x_last_name', 'x_first_name']] = df['patient'].str.split(",", expand=True)
    # df['x_last_name'] = df['x_last_name'].str.strip()
    # df['x_first_name'] = df['x_first_name'].str.strip()

    # eval0 = "patient[0].upper()"
    # eval0 = "for i in range[0:10000000]:pass"
    # eval0 = "sys.exit(0)"
    # df['patient_0'] = df['patient'].apply(eval_stmt, attr='patient', to_format=eval0)
    # df = df[['patient','patient_0']]

    # df['x_first_name'] = df['x_first_name'].astype(str)
    # df['x_last_name'] = df['x_last_name'].astype(str)

    # df.info(verbose=True)

    # df_info(df[['x_last_name', 'x_first_name']], "test")

    # df_obj = df.select_dtypes(['object'])

    # df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    df.info(verbose=True)
    df_info(df, 'after')

    # <ADMITTED_DATE>2021-10-06T15:16:26-04:00</ADMITTED_DATE>
    # <RELEASED_DATE>2021-10-06T23:40:42-04:00</RELEASED_DATE>

    # for col in df:
    #     if df[col].dtype.name == 'object':
    #         df[col] = df[col].astype(str)
    #         print(f"{col} -> str")
    # df.info(verbose=True)

    # print(df.admitted_date.max())
    # print(df.admitted_date.min())
    # print(df.released_date.max())
    # print(df.released_date.min())

    # df = pd.DataFrame(data={
    #     'col1': ['Royzis, Igor', 'Doe,Jane'],
    #     'col2': [1,2],
    #     'patient_gender': ['Male','Female'],
    #     'date1': ['2021-10-06T23:53:17-04:00','2021-10-07T0xx5:15:00-04:00']
    # })
    # df_info(df, 'before')

    # format='%Y-%m-%dT%H:%M:%S'
    # for attr in ['admitted_date', 'released_date']:
    #     df[attr] = df[attr].apply(remove_timezone, format=format)
    #     df[f'x_{attr}'] = pd.to_datetime(df[attr], errors='coerce', format=format).dt.date
    #     df[f'x_{attr}_time'] = pd.to_datetime(df[attr], errors='coerce', format=format).dt.time

    # # split first and last names
    # df[['x_last_name', 'x_first_name']] = df['col1'].str.split(",", expand=True)

    # eval: get first char of gender
    # df['x_patient_gender'] = df['patient_gender'].apply(eval_stmt, attr='patient_gender', to_format="patient_gender[0].upper()")

    # # split datetime into date and time 
    # attr = 'date1'
    # df[f'x_{attr}'] = pd.to_datetime(df[attr], errors='coerce').dt.date
    # df[f'x_{attr}_time'] = pd.to_datetime(df[attr], errors='coerce').dt.time

    # df_info(df, 'after')

    # test fullname split
    # df = pd.DataFrame(data={'col1': ['Royzis, Igor', 'Doe,John'], 'col2': [1,2]})
    # df_info(df, 'before')
    # df[['x_last_name', 'x_first_name']] = df['col1'].str.split(",", expand=True)
    # df_info(df, 'after split')

    # for index, row in df.iterrows():
    #     print(f"[{row['col1']}] [{row['col1']}] [{row['x_last_name']}] [{row['x_first_name']}]")

    # df_obj = df.select_dtypes(['object'])
    # df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    # df_info(df, 'after strip')

    # for index, row in df.iterrows():
    #     print(f"[{row['col1']}] [{row['col1']}] [{row['x_last_name']}] [{row['x_first_name']}]")

    # start = datetime.datetime.now()
    # bucket = sys.argv[1]
    # key = sys.argv[2]
    # df = pd.read_csv(f"s3://{bucket}/{key}")
    # df_info(df, "1: Before")

    # df = process(sys.argv[3], df)
    # df_info(df, "1: After")

    # print(f"Start: {start}")
    # print(f"End: {datetime.datetime.now()}")


        