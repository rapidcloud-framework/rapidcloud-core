__author__ = "Jeffrey Planes"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "jplanes@kinect-consulting.com"

import os
import sys
import json
import boto3
import pickle
import logging
import botocore.session
import base64
from boto3.dynamodb.conditions import Key, Attr

from pyspark.sql.types import *
from pyspark.sql.functions import udf, struct,col,sha2,concat_ws


import hashlib
## from cryptography.fernet import Fernet

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
            rules = self.dynamodb_client.Table('rule').scan(FilterExpression=Attr('profile').eq(self.profile) & Attr('dataset').eq(dataset_name))['Items']
            if rules:
                rules_by_dataset[dataset_name] = rules
            return rules

    def process(self,dataset_name, items, encryption_method='encrypt'):
        
        # mask attribute except for last 4 characters (e.g. credit card)
        ## This defines the python function as a PySpark udf
        @udf("string") 
        def mask(value):
            if len(value)==16:
                charList=list(value)
                charList[0:12]='x'*8
                return "".join(charList)
            else:
                charList=list(value)
                charList[0:len(value) -2]='x'*len(value)
                return "".join(charList)
        
        # encrypt attribute
        ## This defines the python function as a PySpark udf
        @udf("bytes")        
        def encrypt(secret):
            plaint_text = secret.encode('utf-8') 
            ciphertext = self.kms_client.encrypt(
                KeyId=f"alias/{self.profile}",
                Plaintext=plaint_text,
            )
            return base64.b64encode(ciphertext["CiphertextBlob"])
            
        # encrypt attribute
        ## This defines the python function as a PySpark udf
        @udf        
        def encrypt_hash(secret,hash_type='sha256'):
            ## https://medium.com/swlh/encrypting-column-of-a-spark-dataframe-35d64b0db00f
            if hash_type.lower() != 'sha256':
                encrypted_value = hashlib.hash_type(secret.encode()).hexdigest()            
            else:
                encrypted_value = hashlib.sha256(secret.encode()).hexdigest()
            
            return encrypted_value
           
        ##@udf("bytes")  
        ##def encrypt(key_id,column_value):
        ##    key = key_id.encode('utf-8')
        ##    cipher_suite = Fernet(key)
        ##    value =  column_value.encode('utf-8') 
        ##    https://xbuba.com/questions/45789355
        ##    return value[0], str(Fernet(key).encrypt(str.encode(value[1]))), value[2] * 100
        ##    return value[0], cipher_suite.encrypt(str.encode(value[1]))), value[2] * 100
        ##    ## return cipher_suite.encrypt(bytes(value))

        # decrypt attribute 
        ## This defines the python function as a PySpark udf
        @udf("bytes")      
        def decrypt(encrypted_secret):
            plaintext = self.kms_client.decrypt(CiphertextBlob=bytes(base64.b64decode(encrypted_secret)))
            return plaintext["Plaintext"]
            
            
        # @udf("bytes")  
        # def decrypt(key_id,column_value):
        #    key = key_id.encode('utf-8')
        #    cipher_suite = Fernet(key)
        #    return cipher_suite.decrypt(column_value) 
        
        rules = self.get_rules_for_dataset(dataset_name)
        
        logger.info(f'rules metadata: {rules}')
        
        ##encrypt_decrypt_udf = udf(encrypt_decrypt, ByteType())
        
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
                    logger.info(f"mask {rule['attr']} from DataFrame") 
                    print(items[rule['attr']])
                    items = items.withColumn(rule['attr'],mask(rule['attr']))     
                # for encrypt rule, to encrypt the values
                elif rule['action'].lower() == 'encrypt':    
                    logger.info(f"encrypt {rule['attr']} from DataFrame")                    
                    print(items[rule['attr']])
                    if encryption_method.lower() == 'encrypt':
                        items = items.withColumn(rule['attr'],encrypt(rule['attr']))
                    else:
                        items = items.withColumn(rule['attr'],encrypt_hash(rule['attr']))
                # for decrypt rule, to decrypt the values
                elif rule['action'].lower() == 'decrypt':    
                    logger.info(f"encrypt {rule['attr']} from DataFrame")                    
                    print(items[rule['attr']])                                       
                    items = items.withColumn(rule['attr'],decrypt(rule['attr']))
                   
        return items      
        
        
        
