__author__ = "Jeffrey Planes"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "jplanes@kinect-consulting.com"

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

class kc_rules:

    def __init__(self, profile,region_name='us-east-1',credentital_name=None):
        self.profile = profile
        self.region_name = region_name
        self.credentital_name = credentital_name

        if self.credentital_name is not None:
            session = boto3.session.Session(profile_name=self.credentital_name, region_name=self.region_name)
        else:
            session = boto3.session.Session(region_name=self.region_name)

        self.kms_client = session.client('kms')
        self.dynamodb_client = session.resource('dynamodb') 

    def get_rules_for_dataset(self,dataset_name):
        
        rules_by_dataset = {} 

        logger.info(f"getting rules for {dataset_name}")
        if dataset_name in rules_by_dataset:
            return rules_by_dataset[dataset_name]
        else:
            rules = self.dynamodb_client.Table('rule').scan(
                FilterExpression=Attr('profile').eq(self.profile) & Attr('dataset').eq(dataset_name)
                )['Items']
            if rules:
                rules_by_dataset[dataset_name] = rules
            return rules

    def encrypt(self,secret):
            ##ciphertext = self.kms_client.encrypt(KeyId="77a6aa22-b7d3-4cbf-b5fe-f16cd724dc76",Plaintext=bytes(str(secret),"UTF-8"))
            ciphertext = self.kms_client.encrypt(KeyId=f"alias/{self.profile}",Plaintext=bytes(str(secret),"UTF-8"))
            return base64.b64encode(ciphertext["CiphertextBlob"])

    def decrypt(self,encrypted_secret):
            plaintext = self.kms_client.decrypt(CiphertextBlob=bytes(base64.b64decode(encrypted_secret)))
            return plaintext["Plaintext"]

    def mask(self,value):
            if len(value)==16:
                charList=list(value)
                charList[0:12]='x'*8
                return "".join(charList)
            else:
                charList=list(value)
                charList[0:len(value) -2]='x'*len(value)
                return "".join(charList)


    # de-identify attribute. This operation should NOT be reversible
    # supported type: [ssn|fullname|firstname|lastname|dob|id|float|int|string]
    def deidentify(self,value, attr_type):
        if attr_type == 'ssn':
            return f"{randint(100, 999)}-{randint(10, 99)}-{randint(1000, 9999)}"
        elif attr_type == 'fullname':
            return f"{names.get_first_name()} {names.get_last_name()}"
        elif attr_type == 'firstname':
            return names.get_first_name()
        elif attr_type == 'lastname':
            return names.get_last_name()
        elif attr_type == 'dob':
            return f"{randint(1900, 2001)}-{randint(1, 12)}-{randint(1, 29)}"
        elif attr_type == 'id':
            return uuid.uuid1()
        elif attr_type == 'float':
            return random.uniform(10.00, 100000.00)
        elif attr_type == 'int':
            return {randint(20000, 150000)}
        elif attr_type == 'string':
            return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            
    def process(self,dataset_name, items):
        
        rules = self.get_rules_for_dataset(dataset_name)
        
        logger.info(f'rules metadata: {rules}')
        
        if rules:
            for rule in rules:
                logger.info("applying rule:")
                logger.info(json.dumps(rule, indent=2))
                # for omit rule no need to iterate through each item, just drop the column 
                if rule['action'].lower() == 'omit': 
                    logger.info(f"dropping {rule['attr']} from DataFrame")
                    columns_to_drop = [rule['attr']]                        
                    items = items.drop(*columns_to_drop)  
                # for masking rule, to mask the last 4 characters to '****'
                elif rule['action'].lower() == 'mask':    
                    logger.info(f"encrypt {rule['attr']} from DataFrame")                    
                    print(items[rule['attr']])
                    items[rule['attr']] = items[rule['attr']].apply(self.mask)                      
                # for encrypt rule, to encrypt the values
                elif rule['action'].lower() == 'encrypt':    
                    logger.info(f"encrypt {rule['attr']} from DataFrame")                    
                    print(items[rule['attr']])
                    items[rule['attr']] = items[rule['attr']].apply(self.encrypt)
                # for encrypt rule, to encrypt the values
                elif rule['action'].lower() == 'encrypt':    
                    logger.info(f"encrypt {rule['attr']} from DataFrame")                    
                    print(items[rule['attr']])
                    items[rule['attr']] = items[rule['attr']].apply(self.encrypt)
                elif rule['action'] == 'deidentify':
                    logger.info(f"de-identifying {rule['attr']}")
                    items[rule['attr']] = items[rule['attr']].apply(self.deidentify, attr_type=rule['attr_type'])

        return items
        
        
        
        
