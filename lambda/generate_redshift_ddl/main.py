__license__ = "MIT"

import os
import sys
import json
import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
from kc_common.kc_redshift_access import Redshift
from kc_common.kc_aws_secrets import Secrets

## Passed in an environment variables
profile = os.environ['profile']
aws_service = 'dynamodb'
secret_name = 'kinect_atlas_dev/redshift_cluster/main/connection_string'
## Retrieve AWS Lambda Environmental Variables
aws_region = os.environ['AWS_REGION']
lambda_function = os.environ['AWS_LAMBDA_FUNCTION_NAME']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_boto3_session(aws_region="us-east-1", profile=None):

    ## DECLARATION SECTION
    function_id = sys._getframe().f_code.co_name

    try:

        if profile is not None:
            session = boto3.session.Session(profile_name=profile, region_name=aws_region)
        else:
            session = boto3.session.Session()

        return session

    except Exception as e:
        msg = e.args
        exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
        raise Exception(exception_msg)
        
def get_publishing(session, aws_service, profile):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name

        try:

            table = session.resource(aws_service).Table("publishing")
            response = table.scan(FilterExpression=Attr("profile").eq(profile))
                
            return response['Items']

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            raise Exception(exception_msg)
            
def table_exists_query(schema_name,table_name):
    
  
    sql = f"""
            SELECT table_name
            FROM  information_schema.columns
            WHERE table_schema = '{schema_name}'
            AND   table_name = '{table_name}';
          """
          
    return sql 
            
def get_record_count_query(schema_name,table_name):

    sql = f"""
            SELECT COUNT(*) AS RecordCount
            FROM  {schema_name}.{table_name} ;
          """
          
    return sql 

def lambda_handler(event, context):
    
    try:
            
             ## Retreive the boto3 session object
            session = get_boto3_session(aws_region)
            response_publishing = get_publishing(session,aws_service,profile)
            has_executed = False
            
            for publishing in response_publishing:
                redshift_table_property = publishing["redshift_table_property"]
                redshift_stage_ddl = publishing["redshift_ddl"]
                redshift_base_ddl = publishing["redshift_ddl"]
                schema_name = publishing["schema"]
                table_name = publishing["name"]
                
                ## Instantiate Secrets Class
                aws_secret = Secrets(lambda_function, secret_name)
                secret_json = aws_secret.get_secret()
                ## Instantiate Redshift Class
                redshift_conn = Redshift(lambda_function, secret_json)
                
                if has_executed == False:
                    create_stage_schema = f"""
                                            CREATE SCHEMA IF NOT EXISTS {schema_name}_stage ;
                                          """
                    create_base_schema = f"""
                                            CREATE SCHEMA IF NOT EXISTS {schema_name} ;
                                          """
                                          
                    logger.info(f'Create Stage Schema: {create_stage_schema}')
                    logger.info(f'Create Base Schema: {create_base_schema}')
                    redshift_conn.execute_sql(create_stage_schema)
                    redshift_conn.execute_sql(create_base_schema)
                    ## Flip the boolean to True
                    has_executed = True
                    
                table_exists_sql = table_exists_query(schema_name,table_name)
                record_count_sql = get_record_count_query(schema_name,table_name)
                
                logger.info(f'Table Exists Query: {table_exists_sql}')
                logger.info(f'Record Count Query: {record_count_sql}')
                
                record_count = -9999
                exists_rows = redshift_conn.return_dataset(table_exists_sql)
                ## Evaluate if the table exists before executing a count query
                if  exists_rows != []:
                    rows = redshift_conn.return_dataset(record_count_sql)
                    if  rows != None:
                        for row in rows:
                            record_count = row[0]
                
                if record_count > 0:
                    return_message = f'Table: {schema_name}.{table_name} is NOT empty, the table has not been dropped and recreated'
                    logger.warning(return_message)
                    
                elif record_count == 0 or record_count == -9999:
                    
                    drop_stage_table_query = f"""
                                       DROP TABLE IF EXISTS {schema_name}_stage.{table_name} ;
                                       """
                    redshift_conn.execute_sql(drop_stage_table_query)
                    
                    drop_base_table_query = f"""
                                       DROP TABLE IF EXISTS {schema_name}.{table_name} ;
                                       """
                    redshift_conn.execute_sql(drop_base_table_query)
                    
                    logger.info(f'Drop Base Table Query: {drop_stage_table_query}')
                    logger.info(f'Drop Base Table Query: {drop_base_table_query}')
                    ## Replace the '{}' with the schema_name from the metadata
                    
                    redshift_stage_ddl = redshift_stage_ddl.format(f'{schema_name}_stage')
                    logger.info(f'Redshift Stage DDL: {redshift_stage_ddl}')
                    redshift_conn.execute_sql(redshift_stage_ddl)
                    
                    redshift_base_ddl = redshift_base_ddl.format(schema_name)
                    ## Add in the redshift table properties to the base DDL script
                    redshift_base_ddl = f'{redshift_base_ddl} {redshift_table_property}'
                    logger.info(f'Redshift Base DDL: {redshift_base_ddl}')
                    redshift_conn.execute_sql(redshift_base_ddl)
                    
                    return_message = f"Redshift DDL were created successfully for profile:  {profile}"
                
                logger.info(f'Profile: {profile}')
                logger.info(f'AWS Service: {aws_service}')
                logger.info(f'Redshift Table Property: {redshift_table_property}')      
                logger.info(f'Schema Name: {schema_name}')
                logger.info(f'Table Name: {table_name}')
                logger.info(f'Create Stage Schema: {create_stage_schema}')
                logger.info(f'Create Base Schema: {create_base_schema}')
                logger.info(f"Ending lambda function ==> {lambda_function}")            
        
            return {
                'statusCode': 200,
                'body': return_message
            }    
        
    except Exception as e:
        msg = e.args
        exception_msg = f"Exception Occurred Inside this method {lambda_function} --> Here is the exception Message {msg}"
        logger.error(exception_msg)
        raise e