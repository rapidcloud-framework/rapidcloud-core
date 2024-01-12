import csv
import datetime
import io
import json
import os

import boto3


s3 = boto3.client('s3')
session = boto3.Session()
dynamodb_resource = session.resource('dynamodb')


def put_item(table, item):
    response = dynamodb_resource.Table(table).put_item(Item=item)
    #logger.info(json.dumps(item, indent=2, default=json_converter))
    #logger.info(json.dumps(response, indent=2))


def s3_json_to_dict(bucket, key):
    object_response = s3.get_object(Bucket=bucket, Key=key)
    data = object_response['Body'].read()
    return json.loads(data)


def flatten(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten(item))
        else:
            flattened.append(item)
    return flattened


def parse(data_dict):
    blocks = data_dict.get("Blocks")

    lines = [block for block in blocks if block.get("BlockType") == "LINE"]

    words = [block for block in blocks if block.get("BlockType") == "WORD"]

    kv_set = [block for block in blocks if block.get("BlockType") == "KEY_VALUE_SET"]

    keys = [block for block in kv_set if "KEY" in block.get("EntityTypes")]

    text_to_str = {}
    for mapping in [lines, words]:
        for obj in mapping:
            text_to_str[obj.get("Id")] = obj.get("Text")

    v_ids = set(
        flatten(
            [
                obj.get("Ids") for obj in flatten(
                    [
                        [
                            relationship for relationship in block.get("Relationships", []) if relationship.get("Type") == "VALUE"
                        ] for block in keys
                    ]
                )
            ]
        )
    )

    v_id_to_child_ids = {}

    for block in kv_set:
        if block.get("Id") in v_ids:
            child_ids = []
            for relationship in block.get("Relationships", []):
                if relationship.get("Type") == "CHILD":
                    child_ids.extend(relationship.get("Ids", []))
            v_id_to_child_ids[block.get("Id")] = flatten(child_ids)

    k_id_to_child_ids = {block.get("Id"): flatten([obj.get("Ids") for obj in [relationship for relationship in block.get("Relationships") if relationship.get("Type") == "CHILD"]]) for block in keys}

    kv_ids = {obj[0]: obj[1].get("Ids")[0] for obj in flatten([[(block.get("Id"), relationship) for relationship in block.get("Relationships") if relationship.get("Type") == "VALUE"] for block in keys])}

    k_id_to_str = {k: " ".join(flatten([text_to_str.get(child) for child in v])) for k, v in k_id_to_child_ids.items()}

    v_id_to_str = {k: " ".join(flatten([text_to_str.get(child, '') for child in v])) for k, v in v_id_to_child_ids.items()}

    kv_str = {k_id_to_str.get(k): v_id_to_str.get(v) for k,v in kv_ids.items()}

    if '' in kv_str:
        del kv_str['']

    return kv_str


def iterate_over_results(bucket, prefix='files/'):
    print(f'starting iterate_over_results :: bucket: {bucket}')
    paginator = s3.get_paginator('list_objects_v2')
    results = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for content in page.get('Contents', []):
            if content['Key'].endswith('-extracted-document-analysis-forms.json'):
                results.append(content['Key'])
    print('ending iterate_over_results')
    return results


def lambda_handler(event, context):
    print('starting execution')
    print(f'event: {event}')
    print(f'context: {context}')
    env = os.environ["PROFILE"]
    bucket_prefix = env.replace('_', '-')
    src_bucket = f'{bucket_prefix}-raw'
    dest_bucket = f'{bucket_prefix}-analysis'
    existing_files_content = []
    existing_files = iterate_over_results(src_bucket, prefix='files/')
    for existing_file in existing_files:
        if '.json' not in existing_file:
            continue
        if '/rc_any/' in existing_file or '/rc_samples/' in existing_file or '/old/' in existing_file:
            continue
        existing_file_text = parse(s3_json_to_dict(src_bucket, existing_file))
        existing_files_content.append({'file': existing_file, 's3': f's3://{src_bucket}/{existing_file}', 'content': existing_file_text})
    print(f'existing_files_content: {existing_files_content}')
    
    matches = {}
    try:
        with open('./mapping_textract.json', 'r') as f:
            matches = json.load(f)
    except Exception as e:
        print(f'Error loading mapping_textract.json: {e}')
        #raise e
        return {'status': 'failed', 'error': e}

    try:
        rubric = {v.lower(): k for k, lst in matches.items() for v in lst}
        print(f'rubric: {rubric}')
        rows = []
        for file_data in existing_files_content:
            extracted_kv = file_data.get('content')
            extracted_filename = file_data.get('file')
            extracted_s3_uri = file_data.get('s3')
            row = {def_key: '' for def_key in matches.keys()}
            for key_case_sensitive, value in extracted_kv.items():
                key = key_case_sensitive.lower()
                if key in rubric:
                    row[rubric[key]] = value
            rows.append(row)
        
        print(f'rows: {rows}')
        
        # create tmp csv
        csv_file = io.StringIO()
        print('io file defined')
        fieldnames = rows[0].keys()
        print('fieldnames defined')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        
        print('csv written in memory')
        # get csv data as a string
        csv_content = csv_file.getvalue()
        
        # upload temp csv to s3 under rc-reports
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', '--')
        report_file_name = f'reports/report-{timestamp}.csv'
        s3 = boto3.client('s3')
        s3.put_object(Body=csv_content, Bucket=dest_bucket, Key=report_file_name)
        print(f'uploading csv file to: s3://{dest_bucket}/{report_file_name}')
        
        # TODO: put this functionality in reports module
        fqn = f'{env}_report_sample_report_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}'
        job_type = 'report'
        profile = env
        report_name = 'sample_report'
        status = 'SUCCESS'
        update_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        results = f's3://{dest_bucket}/{report_file_name}'
        data = rows
        
        item = {
            'fqn': fqn,
            'job_type': job_type,
            'profile': profile,
            'report_name': report_name,
            'status': status,
            'update_timestamp': update_timestamp,
            'results': results,
            'data': data,
        }
        
        print(f'item: {item}')
        
        put_item('transform_log', item)
        
        print('updated obj')
        
        resp = {
            's3': f's3://{dest_bucket}/{report_file_name}',
            'report_name': report_file_name,
            'status': 'success',
            'update_timestamp': timestamp,
            'results': rows,
        }
        print(f'resp: {resp}')
        return resp
    except Exception as e:
        print(e)
        return {'status': 'failed', 'error': e}
