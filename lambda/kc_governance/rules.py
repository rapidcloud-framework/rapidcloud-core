__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
import sys
import json
import boto3
import logging
import os
import uuid 
import names
import random
from random import seed
from random import randint
import string
import base64
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']
session = boto3.Session()
kms_client = session.client('kms')

# mask attribute except for last 4 characters (e.g. credit card)
def mask(value):
    last_4 = value[(len(value) - 4):]
    len_masked = len(value) - 4
    return ''.join([char*len_masked for char in '*']) + last_4 


# encrypt attribute 
def encrypt(secret):
    ciphertext = kms_client.encrypt(
        KeyId=f"alias/{PROFILE}",
        Plaintext=bytes(str(secret), "UTF-8"),
    )
    return base64.b64encode(ciphertext["CiphertextBlob"])


# decrypt attribute 
def decrypt(session, encrypted_secret):
    plaintext = kms_client.decrypt(
        CiphertextBlob=bytes(base64.b64decode(encrypted_secret))
    )
    return plaintext["Plaintext"]
    

# de-identify attribute. This operation should NOT be reversible
# supported type: [ssn|fullname|firstname|lastname|dob|id|float|int|string]
def deidentify(value, attr_type):
    if attr_type == 'ssn':
        return f"{randint(100, 999)}-{randint(10, 99)}-{randint(1000, 9999)}"
    elif attr_type == 'fullname':
        return f"{names.get_first_name()} {names.get_last_name()}"
    elif attr_type == 'firstname':
        return names.get_first_name()
    elif attr_type == 'lastname':
        return names.get_last_name()
    elif attr_type == 'dob':
        days_between_dates = (datetime.date(2021, 12, 31) - datetime.date(1900, 1, 1)).days
        random_date = datetime.date(1900, 1, 1) + datetime.timedelta(days=random.randrange(days_between_dates))
        return random_date.strftime("%Y-%m-%d")
        # return f"{randint(1900, 2001)}-{str(randint(1, 12)).zfill(2)}-{str(randint(1, 28)).zfill(2)}"
    elif attr_type == 'id':
        return uuid.uuid1()
    elif attr_type == 'float':
        return random.uniform(10.00, 100000.00)
    elif attr_type == 'int':
        return {randint(20000, 150000)}
    elif attr_type == 'string':
        return ''.join(random.choice(string.ascii_lowercase) for i in range(10))


def get_rules_for_dataset(dataset_name):
    logger.info(f"getting rules for dataset {PROFILE}/{dataset_name}")
    rules = session.resource('dynamodb').Table('rule').scan(        
        FilterExpression=Attr('dataset').eq(dataset_name) & Attr('profile').eq(PROFILE)
    )['Items']
    logger.info(json.dumps(rules, indent=2))
    return rules


def process(df, rules):
    for rule in rules:
        logger.info("applying rule:")
        logger.info(json.dumps(rule, indent=2))
        if rule['action'] == 'omit':    
            logger.info(f"dropping {rule['attr']}")
            df = df.drop([rule['attr']], axis=1)
        elif rule['action'] == 'mask':
            logger.info(f"masking {rule['attr']}")
            df[rule['attr']] = df[rule['attr']].apply(mask)
        elif rule['action'] == 'encrypt':
            logger.info(f"encrypting {rule['attr']}")
            df[rule['attr']] = df[rule['attr']].apply(encrypt)
        elif rule['action'] == 'deidentify':
            random.seed(71)
            logger.info(f"de-identifying {rule['attr']}")
            df[rule['attr']] = df[rule['attr']].apply(deidentify, attr_type=rule['attr_type'])

    return df

# this is for testing only
if __name__ == "__main__":
    random.seed(71)
    print(deidentify('1971-5-6', 'dob'))
    print(deidentify('2002-8-15', 'dob'))
    print(deidentify('2007-3-28', 'dob'))
    print(deidentify('Igor Johnson', 'fullname'))
    print(deidentify('Aaron Johnson', 'fullname'))
    print(deidentify('Adriana Johnson', 'fullname'))
    print(deidentify('Igor', 'firstname'))
    print(deidentify('Aaron', 'firstname'))
    print(deidentify('Adriana', 'firstname'))
    # session = boto3.Session(profile_name='default')
    # response = session.resource('dynamodb').Table('rule').scan(        
    #     FilterExpression=Attr('dataset').eq('employees') & Attr('profile').eq('kinect_atlas_dev')
    # )['Items']
    # print(json.dumps(response, indent=2))
        