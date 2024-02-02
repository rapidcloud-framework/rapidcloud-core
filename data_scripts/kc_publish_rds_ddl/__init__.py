__license__ = "MIT"

import sys
import os
import json
from datetime import datetime
import boto3
import fnmatch, re
from boto3.dynamodb.conditions import Key, Attr
import sqlparse
import argparse
import logging

from  data_scripts.kc_athena_access import Athena
from  data_scripts.kc_s3 import S3
from  data_scripts.kc_metadata import Metadata
from  data_scripts.kc_aws_secrets import Secrets
from  data_scripts.kc_postgresql_access import PostgreSQL
from  data_scripts.kc_mysql_access import MySQL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RdsSqlDDL():

    def create_schema(self,schema_name):

        sql_create_schema = f"""
        CREATE  SCHEMA IF NOT EXISTS  {schema_name} ;
        """
        return sql_create_schema

    def create_stage_ddl(self,schema_name,table_name,column_name_and_data_type_list,separator_comma):

        sql_create_table_header = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        """
        sql_create_table_footer = f"""     
        )
        """
        
        sql_create_table_footer = f"""  
        ) 
            """

        column_data_type_sql = "".join(column_name_and_data_type_list)
        return_sql = (
            f"{sql_create_table_header}{column_data_type_sql}{sql_create_table_footer}"
        )
        ## The sqlparse will provide the desired SQL formatting
        return_sql = sqlparse.format(return_sql, keyword_case='upper',comma_first=True)
        return return_sql

    def create_target_ddl(self,schema_name,table_name,column_name_and_data_type_list,separator_comma,primary_key):

        primary_key = primary_key.strip(separator_comma)
        sql_create_table_header = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        """
        sql_create_table_footer = f"""     
        )
        """    
        if  (primary_key != 'n/a'):
            sql_create_table_footer = f"""
            ,PRIMARY KEY ({primary_key})                            
            ) 
            """   
        else:
            sql_create_table_footer = f"""  
            ) ;
            """

        column_data_type_sql = "".join(column_name_and_data_type_list)
        return_sql = (
            f"{sql_create_table_header}{column_data_type_sql}{sql_create_table_footer}"
        )
        ## The sqlparse will provide the desired SQL formatting
        return_sql = sqlparse.format(return_sql, keyword_case='upper',comma_first=True)
        return return_sql

    def get_drop_table_sql(self,schema,table):

        sql = f"""
                                DROP TABLE IF EXISTS  {schema}.{table}
                """
        return sql 

    def get_record_count_sql(self,schema,table):

        sql = f"""
                                SELECT COUNT(*) AS record_count
                                FROM {schema}.{table}
                            """
        return sql 

    def  get_table_query(self,schema_name,table_name):

        sql = f"""
                SELECT COUNT(*) AS record_count
                FROM  INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = '{schema_name}'
                AND    TABLE_NAME = '{table_name}' 
                LIMIT  1 ;
                """
        return sql

    def get_athena_metadata(self,analysis_catalog,analysis_table):

        sql = f"""
                                SELECT 
                                        table_schema
                                        ,table_name
                                        ,column_name
                                        ,ordinal_position
                                        ,is_nullable
                                        ,data_type
                                FROM information_schema.columns 
                                WHERE table_schema = '{analysis_catalog}'
                                AND   table_name   = '{analysis_table}' 
                                ORDER BY ordinal_position    
                            """
        return sql 
                
    # function to get unique values 
    def unique_list(self,list): 

        # intilize a null list 
        return_unique_list = []       
        # traverse for all elements 
        for x in list: 
            # check if exists in unique_list or not 
            if x not in return_unique_list: 
                return_unique_list.append(x) 
        return return_unique_list

    def main(self,args):

            ## DECLARATION SECTION
            function_id = sys._getframe().f_code.co_name
            script_id = os.path.basename(str(sys.argv[0]))
            script_id = script_id.split(".")[0].split("/")[-1]
            engine_from = "athena"
            separator_dot = "."
            separator_comma = ","
            separator_underscore = "_"
            property_name_suffix_pk = '_varchar_max_length' ## The prefix will be concatenated with the db_engine (I.E. mysql, postgresql)
            job_name = function_id    
            now = datetime.now()  # current date and time
            date_string = now.strftime("%Y-%m-%d %H:%M:%S")
            publising_dnmo_table = "publishing"
            aws_service = "dynamodb"
            data_type = ""
            sql_file_extension = '.sql'
            schema_stage = ''
            has_schema_processed = False
            ## list object used to buld the dataset list for the most outer loop
            dataset_list = []

            try:
                
                if args.profile:
                    profile = args.profile.lower()
                if args.aws_profile:
                      aws_profile = args.aws_profile.lower()
                if args.aws_region:
                    aws_region = args.aws_region
                if args.env_prefix:
                    env_prefix = args.env_prefix
                if args.data_lake_fqn:
                    data_lake_fqn = args.data_lake_fqn.lower()
                if args.output_folder_path:
                    output_folder_path = args.output_folder_path
                if args.datasets:
                    datasets = args.datasets

                # if args.profile is None:
                #     profile = 'kinect_atlas_dev'      
                # if args.aws_profile is None:
                #     aws_profile =  'kinect_atlas_dev' 
                # if args.aws_region is None:
                #     aws_region = 'us-east-1'
                # if args.env_prefix is None:
                #     env_prefix = "dev"
                # if args.data_lake_fqn is None:
                #     data_lake_fqn = "kinect_dev"
                # if args.output_folder_path is None:
                #     output_folder_path = "output"
                # if args.datasets is None:
                #     datasets =  'all' ##'heartbeat_stats,service_endpoints_with_heartbeats' ## 'inbound_call' ## 'all'

                logger.info(f"Profile: {profile}")
                logger.info(f"AWS Profile: {aws_profile}")
                logger.info(f"AWS Region: {aws_region}")
                logger.info(f"Env Prefix: {env_prefix}")
                logger.info(f"Output Folder Path: {output_folder_path}")
                logger.info(f"Datasets: {datasets}")

                ## Instantiate the  Metadata Class
                metadata = Metadata(aws_region,aws_service,aws_profile)

                s3_conn = S3(job_name,aws_profile)

                ## Retrieve ALL metadata from the datalake entity
                response_datalake = metadata.query("datalake","fqn",data_lake_fqn) 

                logger.info(f"Data Lake Metadata: {response_datalake}")

                for datalake in response_datalake:
                    # environment = datalake["env"]
                    s3_athena_bucket = datalake["athena_s3_bucket"].replace("_","-")

                if datasets.lower() == 'all' or datasets == '' or  datasets.lower() == 'all,':
                    datasets = 'all,'
                else:
                    ## Evaluate if the last character has a comma, and if not, then add in a comma at the end of the datasets variable.
                    if datasets.endswith(separator_comma):
                        dataset_list = datasets.split(separator_comma)
                    else:
                        ## Adding in a comma at the tail end of the datasets variable
                        datasets = f'{datasets},'
                        dataset_list = datasets.split(separator_comma)

                if datasets == 'all,':
                    #     ## Retrieve ALL metadata from the publishing
                    #     ## This will retreive publishing records by profile and (exclude redshift and snowflake)
                    #     ## Need to strip out the trailing comma at the end of datasets whenever calling the get_metadata method
                    response_dataset_publishing = metadata.get_publishing_metadata(profile,datasets.strip(separator_comma)) 
                    
                    if len(response_dataset_publishing) == 0:
                            exception_msg = f"Exception Occurred Inside this method {function_id} --> No metadata returned for {publising_dnmo_table} no value for {datasets}"
                            logger.exception(exception_msg)
                            raise Exception(exception_msg)

                    for dataset in response_dataset_publishing:
                                dataset = dataset['name']
                                dataset_list.append(dataset)
                    
                for dataset in dataset_list:

                    ## If there are no more elements in the list array then do NOT process. We are adding in an extra comma at the tail end of the datasets variable, so this will give us an 
                    ## empty array element, so this would NOT process into the for loop.
                    if not dataset:
                        pass
                    else:

                        ##dataset = datasets.strip(separator_comma)
                        ## Retrieve ALL metadata from the transformation
                        ## This will retreive ALL publishing records by profile and dataset/name
                        ## Instantiate the  Metadata Class
                        metadata = Metadata(aws_region,aws_service,aws_profile)
                        response_publishing = metadata.get_publishing_metadata(profile,dataset)  

                        # # Evaluate if the response object is empty
                        if len(response_publishing) == 0:
                            exception_msg = f"EXCEPTION occurred inside this method {function_id} --> No metadata returned for {publising_dnmo_table} no value for {dataset}"
                            logger.exception(exception_msg)
                            raise Exception(exception_msg)

                        for publish in response_publishing:
                            ## Declaring list objects
                            table_name_list = []
                            column_name_and_data_type_list = []
                            column_list = []
                            data_type_list = []
                            ordinal_position_list = []
                            schema_list = []
                            schema_stage_list = []
                            pk_list = []
                            fqn_list = []
                            secret_name_list = []
                            db_engine = publish['db_engine']
                            output_folder_full_path  = ''                   
                            output_folder_full_path = f'{output_folder_path}/{db_engine}/{env_prefix}/'
                            fqn = publish['fqn']
                            pk = publish['primary_key']
                            secret_name = publish['connection_string']
                            analysis_catalog = publish['analysis_catalog']
                            analysis_table = publish["name"]  ## This is both the Catalog dataset name and the table name
                            schema = publish["schema"]
                            schema_stage = f'{schema}_stage'
                            table_name = publish["name"]  ## This is both the Catalog dataset name and the  table name
                        
                            ## Retrieve ALL metadata from the property entity                       
                            property_name_pk = f'{db_engine}{property_name_suffix_pk}'
                            logger.info(f"Profile: {profile}")
                            logger.info(f"Property Name Suffix PK: {property_name_pk}")
                            response_property = metadata.query_property("property",profile,property_name_pk) 
                            # # Evaluate if the response object is empty
                            if len(response_property) == 0:
                                exception_msg = f"EXCEPTION occurred inside this method {function_id} --> No metadata returned for property no value for {profile} and {property_name_pk}"
                                logger.exception(exception_msg)
                                raise Exception(exception_msg)

                            ## Retrieve the mysql_varchar_max_length mysql_varchar_max_length value to use for the maximum size for the varchar
                            for property  in response_property:
                                max_length = property["value"]
                                logger.info(f"Maximum Length: {max_length}")                        

                            athena_metadata_query = self.get_athena_metadata(analysis_catalog,analysis_table)
                            print(f'Athena Metadata Query: {athena_metadata_query}')
                            logger.info(f'Athena Metadata Query: {athena_metadata_query}')

                            athena_prefix = f"{analysis_catalog}/schema/{schema}/{table_name}/date={date_string}/"
                            athena_output = f"s3://{s3_athena_bucket}/{athena_prefix}"
                            
                            ## BEGIN Evaludate if the Athen S3 Bucket exists or not
                        ##s3_athena_bucket  = 'kinect-bi-dev-query-results-bucket-v2'
                            bucket_exists = s3_conn.s3_bucket_exists(s3_athena_bucket)
                            if bucket_exists:
                                s3_conn.deleteFiles(s3_athena_bucket, athena_prefix)
                            else:
                                exception_msg = f"Exception occurred inside this method {function_id} --> S3 Bucket {s3_athena_bucket} does NOT exists"
                                logger.error(exception_msg)     
                                raise Exception(exception_msg)
                            ## END Evaludate if the Athen S3 Bucket exists or not

                            metadata = Metadata(aws_region,aws_service,profile)
                            data_type_fqn =  f'{engine_from}{separator_underscore}{db_engine}'
                            metadata_datatype = metadata.query("data_type_translation","fqn",data_type_fqn) ##get_cdc_data_type(session, aws_service,data_type_fqn)

                            ## Evaluate if the response object is empty
                            if len(metadata_datatype) == 0:
                                exception_msg = f"Exception Occurred Inside this method {function_id} --> No metadata returned for data_type_translation for fqn {data_type_fqn}"
                                raise Exception(exception_msg)

                            ## Note: Populate dictionary with key = cast_from and value = cast_to
                            cast_dict = {}
                            for item in metadata_datatype:       
                                    cast_dict[item['cast_from']]=item['cast_to']
                                    
                            athena_conn = Athena(job_name, athena_output,aws_profile)
                            ## Get the information_schema to get the data types from Athena
                            athena_metadata = athena_conn.returnDataSet(athena_metadata_query)
                                            
                            ## Read the information_schema to get the data types from Athena
                            for metadata in athena_metadata:
                                # if metadata is not None:
                                if  len(metadata) != 0:
                                    ## table_name = metadata['table_name']
                                    ordinal_position = metadata['ordinal_position']
                                    column_name = metadata['column_name']
                                    from_data_type = metadata['data_type']       
                                    ## END retrieve source table metadata 

                                    ## Note: Athena data type to target data type
                                    ## No need for any if logic 
                                    data_type = cast_dict[from_data_type]   
                                    logger.info(f"From Data Type: {from_data_type}")      
                                    logger.info(f"To Data Type: {data_type}")                          
                                
                                ## Check to see if the data_type does NOT have a value, if true, then raise an exception
                                if (data_type is None):
                                    exception_msg = f"Exception Occurred Inside this method {function_id} --> Data Type {data_type} not regeristered in metadata"
                                    raise Exception(exception_msg)

                                ## Append to the list object
                                ## BEGIN all metadata is coming from the response_publishing list object
                                table_name_list.append(table_name)                                                                      
                                schema_list.append(schema)
                                schema_stage_list.append(schema_stage)
                                pk_list.append(pk)
                                fqn_list.append(fqn)
                                secret_name_list.append(secret_name)
                                ##db_engine_list.append(db_engine)
                                ## BEGIN all metadata is coming from the metadata_datatype list object
                                ordinal_position_list.append(ordinal_position)
                                column_list.append(column_name)
                                data_type_list.append(data_type)

                            ## Declare a list object to be used to identify if a pk column has been already defined inside the loop.
                            pk_colum_list = []
                            for table_name,column_name,data_type,ordinal_position,pk,schema,schema_stage,fqn,secret_name in zip(table_name_list,column_list,data_type_list,ordinal_position_list,pk_list,schema_list,schema_stage_list,fqn_list,secret_name_list):
                                ## BEGIN build out the columns and data type list object
                                if pk is None or pk == 'true':
                                    pk = 'n/a'
                                if pk != '':
                                    logger.info(f"Table: {table_name}")                            
                                    logger.info(f"Column Name: {column_name}")
                                    logger.info(f"Data Type: {data_type}")
                                    logger.info(f"Ordinal Position: {ordinal_position}")                                                     
                                    logger.info(f"PK: {pk}")
                                    logger.info(f"Schema: {schema}")
                                    logger.info(f"Stage Schema: {schema_stage}")  

                                    ## Note: May need to do this for the precision and/or scale of a numeric data type.
                                    ## BEGIN Evaluate if the data type is of a varchar or string data type, if so get the maximum size of the data value.                                
                                    if data_type == 'varchar':
                                        ## Use the max_length for the size of the varchar
                                        data_type = f'{data_type} ({max_length})'
                                    ## BEGIN Evaluate if the data type is of a varchar or string data type, if so get the maximum size of the data value.
                                
                                    ## Evaluate the ordinal position in the information schema metadata
                                    if ordinal_position != 1:
                                        if column_name in pk and column_name not in pk_colum_list:
                                            pk_colum_list.append(column_name)
                                            column_name_and_data_type = (f",{column_name}   {data_type}  not null \n")
                                        if  column_name not in pk:
                                            column_name_and_data_type = (f",{column_name}   {data_type} \n")
                                    else:
                                        if column_name in pk and column_name not in pk_colum_list:
                                            pk_colum_list.append(column_name)
                                            column_name_and_data_type = (f"{column_name}   {data_type}  not null \n")
                                        if  column_name not in pk:
                                            column_name_and_data_type = (f"{column_name}   {data_type} \n")
                                    ## Append to the list object
                                    column_name_and_data_type_list.append(column_name_and_data_type)   
                                    ## Need to de-dupe the column_name_and_data_type_list list object           
                                    ## END build out the columns and data type list object
                                
                            if len(column_name_and_data_type_list) != 0:
                                ## Build the Athena DDL query
                                ## Need to de-dupe the column_name_and_data_type_list list object
                                column_name_and_data_type_list = self.unique_list(column_name_and_data_type_list)   
                                stage_ddl = self.create_stage_ddl(schema_stage,table_name,column_name_and_data_type_list,separator_comma)
                                target_ddl = self.create_target_ddl(schema,table_name,column_name_and_data_type_list,separator_comma,pk)

                                schema_stage_ddl = self.create_schema(schema_stage)
                                schema_ddl = self.create_schema(schema)

                                ## BEGIN Create/Drop/Re-Create schema and tables target tables
                                aws_secret = Secrets(job_name, secret_name)
                                secret_json = aws_secret.get_secret()

                                ## Evaluate which target engine we are working with to decide which Class to instantiate
                                if db_engine.lower() == "mysql":
                                    ## Instantiate the  Database Class
                                    db_conn = MySQL(job_name, secret_json)    
                                elif db_engine.lower() == 'postgresql':
                                    ## Instantiate the  Database Class
                                    db_conn = PostgreSQL(job_name, secret_json)   

                                if  not has_schema_processed:
                                    db_conn.execute_sql(schema_stage_ddl)
                                    db_conn.execute_sql(schema_ddl)
                                    has_schema_processed = True

                                ## Query the information schema to see if the target table exists                            
                                table_query = self.get_table_query(schema,table_name)
                                rows = db_conn.return_dataset(table_query)
                                table_exists = rows[0]['record_count']                                                        

                                ## If the table is empty, then we can drop the target table
                                if  table_exists == 0:
                                    sql_drop_table = self.get_drop_table_sql(schema,table_name)
                                    db_conn.execute_sql(sql_drop_table)
                                else:                                
                                    sql_record_count = self.get_record_count_sql(schema,table_name)
                                    ## Get the record count, to determine if the targe table is empty, is so we can drop and re-create the table                            
                                    rows = db_conn.return_dataset(sql_record_count)
                                    record_count = rows[0]['record_count']     
                                    logger.info(f"Record Count: {record_count}")
                                    ## Check the record_cou is 0,  then drop the target table
                                    if record_count == 0:
                                        sql_drop_table = self.get_drop_table_sql(schema,table_name)
                                        db_conn.execute_sql(sql_drop_table)
                                    else:
                                        logger.warning(f'Table: {schema}.{table_name} is NOT empty, the table has not been dropped and recreated')   

                                ## Get the drop stage table sql
                                sql_drop_stage_table = self.get_drop_table_sql(schema_stage,table_name)
                                ## Drop stage table
                                db_conn.execute_sql(sql_drop_stage_table)
                                db_conn.execute_sql(stage_ddl)
                                db_conn.execute_sql(target_ddl)

                                logger.info(f"Schema/Table: {schema}.{table_name}")                           
                                logger.info(f"Drop Stage Table SQL: {sql_drop_stage_table}")
                                logger.info(f"Stage DDL: {stage_ddl}")
                                logger.info(f"Target DDL: {target_ddl}")

                                ## END Create/Drop/Re-Create schema and tables for target tables

                                ## Append the engine name to the output folder path
                                ## Check to see if folder exists, if not then create it.
                                output_folder_ddl_path = f'{output_folder_full_path}ddl'
                                if not os.path.exists(output_folder_ddl_path):
                                    os.makedirs(output_folder_ddl_path)

                                ## Create the Python Transformation script
                                ## Need to get the ".sql file name" from publishing dynamodb table
                                python_script = f"{output_folder_ddl_path}/{schema_stage}{separator_dot}{table_name}_ddl{sql_file_extension}"
                                with open(python_script, "w") as writer:
                                    writer.writelines(f'{stage_ddl};')           

                                ## Create the Python Transformation script
                                ## Need to get the ".sql file name" from publishing dynamodb table
                                python_script = f"{output_folder_ddl_path}/{schema}{separator_dot}{table_name}_ddl{sql_file_extension}"
                                with open(python_script, "w") as writer:
                                    writer.writelines(f'{target_ddl};')      

                                ## Inialize the boolean
                                has_schema_processed = False
                                if  not has_schema_processed:
                                    schema_stage_ddl = self.create_schema(schema_stage)
                                    ## Append the engine name to the output folder path
                                    ## Check to see if folder exists, if not then create it.
                                    output_folder_schema_path = f'{output_folder_full_path}schema/'
                                    if not os.path.exists(output_folder_schema_path):
                                        os.makedirs(output_folder_schema_path)

                                    ## Create the Python Transformation script
                                    ## Need to get the ".sql file name" from publishing dynamodb table
                                    python_script = f"{output_folder_schema_path}/{schema_stage}_schema{sql_file_extension}"
                                    with open(python_script, "w") as writer:
                                        writer.writelines(schema_stage_ddl)

                                    ## Create the Python Transformation script
                                    ## Need to get the ".sql file name" from publishing dynamodb table
                                    schema_ddl = self.create_schema(schema)
                                    python_script = f"{output_folder_schema_path}/{schema}_schema{sql_file_extension}"
                                    with open(python_script, "w") as writer:
                                        writer.writelines(schema_ddl)    

                                    logger.info(f"Stage Schema: {stage_ddl}")
                                    logger.info(f"Base Schema: {target_ddl}")   

                                    ## Flip the boolean to True   
                                    has_schema_processed = True

                                logger.info(f"Stage DDL: {stage_ddl}")
                                logger.info(f"Base DDl: {target_ddl}")
                                        
                            else:

                                warning_msg = f"Warning Occurred Inside this method {function_id} --> No metadata returned for query {athena_metadata_query}"
                                logger.warning(warning_msg)
                                pass                     

            except Exception as e:
                    msg = e.args
                    exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
                    logger.exception(exception_msg)
                    raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="Please pass in the appropriate --profile")
    parser.add_argument("--aws_profile", required=True, help="Please pass in the appropriate --aws_profile")
    parser.add_argument("--aws_region", required=True, help="Please pass in the appropriate --aws_region")
    parser.add_argument("--env_prefix", required=True,help="Please pass in the appropriate --env_prefix")
    parser.add_argument("--data_lake_fqn",required=True,help="Please pass in the appropriate --data_lake_fqn")
    parser.add_argument("--output_folder_path",required=True,help="Please pass in the appropriate --output_folder_path")    
    parser.add_argument("--datasets",required=True,help="Please pass in the appropriate --datasets")  
    args = parser.parse_args()
    RdsSqlDDL().main(args)

