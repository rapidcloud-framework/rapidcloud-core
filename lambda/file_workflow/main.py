import boto3
import json
import os

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')

    profile = os.environ['PROFILE']

    print(f'event: {event}')
    print(f'context: {context}')

    payload = {
        "event": event,
        "context": str(context)
    }

    print(f'payload: {payload}')

    response = lambda_client.invoke(
        FunctionName=f'{profile.replace("-", "_")}_file_workflow_manual',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(payload)
    )

    response_from_second_lambda = json.loads(
        response['Payload'].read()
    )

    print(f'response_from_second_lambda: {response_from_second_lambda}')

    return {
        'statusCode': 200,
        'body': json.dumps(response_from_second_lambda)
    }
