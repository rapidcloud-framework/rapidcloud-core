__author__ = "Igor Royzis"
__license__ = "MIT"


import sys
import json
import boto3
import logging
import os
import csv
import datetime
import time
import pandas as pd
import awswrangler as wr
# import xml.etree.ElementTree as et 
# from xml.etree import ElementTree
# import xmltodict
import pyarrow
# import json_flatten 

logger = logging.getLogger("s3")
logger.setLevel(logging.INFO)

session = boto3.Session()
s3_resource = session.resource('s3')


def json_converter(self, obj):
    return str(obj)


def sanitize_col_names(df):
    # df.info(verbose=True)
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace('#', '_no')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace('(', '_')
    df.columns = df.columns.str.replace(')', '')
    df.columns = df.columns.str.replace('__', '_')
    for col in df:
        if col[0:1] >= '0' and col[0:1] <= '9':
            df.rename(columns={col: f"_{col}"}, inplace=True)
        if len(col) > 50:
            df.rename(columns={col: f"{col[0:50]}_"}, inplace=True)


def read_csv(bucket, key, sep=","):
    df = wr.s3.read_csv(f"s3://{bucket}/{key}", sep=sep, skip_blank_lines=True)
    sanitize_col_names(df)
    return df


def read_excel(bucket, key, sheet_name=None):
    if sheet_name is None or len(sheet_name) == 0:
        df = wr.s3.read_excel(f"s3://{bucket}/{key}")
    else:
        df = wr.s3.read_excel(f"s3://{bucket}/{key}", sheet_name=sheet_name)
    sanitize_col_names(df)
    return df


def read_json(bucket, key, boto3_session=None):
    if boto3_session:
        df = wr.s3.read_json(f"s3://{bucket}/{key}", boto3_session=boto3_session)
    else:
        df = wr.s3.read_json(f"s3://{bucket}/{key}")
    # sanitize_col_names(df)
    return df


def read_parquet(bucket, key):
    df = wr.s3.read_parquet(f"s3://{bucket}/{key}")
    return df


def read_xml_old(bucket, key):
    # import fsspec
    # print(f"fsspec: {fsspec.__version__}")
    # import s3fs
    # print(f"  s3fs: {s3fs.__version__}")
    df = pd.read_xml(f"s3://{bucket}/{key}")
    sanitize_col_names(df)
    return df


def read_xml(bucket, key):
    obj = s3_resource.Object(bucket, key)
    xml_str = obj.get()['Body'].read().decode('utf-8') 
    df = pd.read_xml(xml_str)
    return df


def to_parquet(df, path):
    # convert object to str
    for col in df:
        # print(f"{col}")
        try:
            if df[col].dtype.name == 'object':
                df[col] = df[col].astype(str)
        except:
            pass

    # remove duplicate columns
    df = df.loc[:,~df.columns.duplicated()]

    df.info(verbose=True)
    wr.s3.to_parquet(
        df=df,
        path=path
    )


# def read_xml_simple(bucket, key, path_to_data=[]):
#     obj = s3_resource.Bucket(bucket).Object(key=key).get()
#     xmldata = obj['Body'].read().decode('utf-8')
#     parsed_xml = et.fromstring(xmldata)

#     # get attr names for df
#     cols = []
#     for node in parsed_xml.getchildren():
#         for attr in node.getchildren():
#             cols.append(attr.tag)
#         break 
#     print(f"XML Columns: {cols}")

#     df = pd.DataFrame(columns=cols)
#     for node in parsed_xml.getchildren():
#         values = []
#         for col in cols:
#             values.append(node.find(col).text)
#         df = df.append(pd.Series(values, index=cols), ignore_index=True)
#     print("XML Dataframe:")
#     print(df.iloc[:3])
#     return df


# def xml_to_json(bucket, key, path_to_data=[], flatten=False):
#     obj = s3_resource.Bucket(bucket).Object(key=key).get()
#     xmldata = obj['Body'].read().decode('utf-8')
#     jsondata = xmltodict.parse(xmldata)

#     if path_to_data:
#         for elem in path_to_data:
#             jsondata = jsondata[elem]
#     else:
#         jsondata = jsondata[next(iter(jsondata))]

#     if flatten:
#         return flatten_json(jsondata) 
#     else:
#         return jsondata
    

# def read_xml(bucket, key, path_to_data=[], flatten=False):
#     jsondata = xml_to_json(bucket, key, path_to_data, flatten)
#     return pd.read_json(json.dumps(jsondata, default=json_converter))


# def read_xml_as_tree(bucket, key, path_to_data=[], flatten=False):
#     obj = s3_resource.Bucket(bucket).Object(key=key).get()
#     xmldata = obj['Body'].read().decode('utf-8')
#     return ElementTree.parse(xmldata) 


# def read_xml_and_flatten(bucket, key, path_to_data=[]):
#     jsondata = xml_to_json(bucket, key, path_to_data)
#     df = pd.json_normalize(data=jsondata, max_level=10)
#     return df.applymap(str)


# def flatten_json(jsondata):
#     print(type(jsondata))
#     flat = []
#     for item in jsondata:
#         # print(item)
#         flat.append(json_flatten.flatten(item))
#     return flat


def delete_folder(bucket, prefix):
    s3_resource.Bucket(bucket).objects.filter(Prefix=prefix).delete()


if __name__ == "__main__":
    arg = sys.argv[1]
    bucket = f"{sys.argv[2]}-ingestion"
    raw = f"{sys.argv[2]}-raw"
    key = sys.argv[3]
    save = sys.argv[4]
    arg5 = sys.argv[5]
    aws_profile = sys.argv[6]

    print(f"bucket: {bucket}")
    print(f"key: {key}")
    print(f"raw: {raw}")
    # sys.exit(0)

    if arg == 'csv':
        df = read_csv(bucket, key)
    elif arg == 'json':
        boto3_session = boto3.Session(region_name="us-east-1", profile_name=aws_profile)
        df = read_json(bucket, key, boto3_session)
        
        df.columns = df.iloc[0]
        df = df.drop(0)
        df = df.reset_index(drop=True)
        
        # sanitize_col_names(df)


    elif arg == 'xlsx':
        df = read_excel(bucket, key, arg5)

    elif arg == 'xml':
        df = read_xml(bucket, key)

    elif arg == 'xml2':
        df = read_xml2(bucket, key)

    df.info(verbose=True)
    print(df.size)
    print(df.head(10))

    if save == "yes":
        dest = f"s3://{raw}/test/test.parquet"
        print(dest)
        to_parquet(df, dest)
