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
from  data_scripts.kc_redshift_access import Redshift

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RedshiftDDL():

    def build_create_schema(self,schema_name):

        sql_build_create_schema = f"""
        CREATE  SCHEMA IF NOT EXISTS  {schema_name} ;
        """
        return sql_build_create_schema

    def build_stage_ddl(self,schema_name,table_name,column_name_and_data_type_list,separator_comma,primary_key):

        ##primary_key = "".join(primary_key).strip(separator_comma)
        primary_key = primary_key.strip(separator_comma)
        sql_create_table_header = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        """
        sql_create_table_footer = f"""     
        )
        """
        ## Evaluate if the PK and/or the table properties have a value
        if  primary_key != 'n/a':
            sql_create_table_footer = f"""
        ,PRIMARY KEY ({primary_key})
        ) 
            """  
        else:
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

    def build_ddl(self,schema_name,table_name,column_name_and_data_type_list,separator_comma,primary_key,sort_key=None,dist_key=None):

        dist_key_length = len(dist_key.split(separator_comma))
        if (dist_key_length == 1):
        ## Evaluate if there is more than 1 dist keys. You can only have one dist key per table.
            if (dist_key is None or dist_key == 'n/a' or dist_key == 'tdb'):
                dist_key_property = 'n/a'
            else:
                dist_key_property = f'DISTKEY({dist_key})'
        else:
            dist_key_property = 'n/a'

        sort_key_length = len(sort_key.split(separator_comma))
        ## Evaluate if there is more than 1 sort keys, if so, then we need to include the key word "COMPOUND" in the sortkey definition.
        if (sort_key_length > 1):
            sort_key_property = f'COMPOUND SORTKEY({sort_key})'
        elif (sort_key is not None and sort_key != 'n/a' and sort_key != 'tdb'):
            sort_key_property = f'SORTKEY({sort_key})'
        else:
            sort_key_property = 'n/a'

        primary_key = primary_key.strip(separator_comma)
        sql_create_table_header = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        """
        sql_create_table_footer = f"""     
        )
        """
        ## Evaluate if the PK and/or the table properties have a value
        if  (primary_key != 'n/a' and sort_key_property != 'n/a' and dist_key_property != 'n/a'):
            sql_create_table_footer = f"""
            ,PRIMARY KEY ({primary_key})
            )
            {dist_key_property} {sort_key_property}  
            """
        elif  (primary_key != 'n/a' and sort_key_property == 'n/a' and dist_key_property == 'n/a'):
            sql_create_table_footer = f"""
            ,PRIMARY KEY ({primary_key})                            
            ) 
            """
        elif  (primary_key != 'n/a' and sort_key_property == 'n/a' and dist_key_property != 'n/a'):
            sql_create_table_footer = f"""
            ,PRIMARY KEY ({primary_key})     
            )
            {dist_key_property}  
            """
        elif  (primary_key != 'n/a' and sort_key_property != 'n/a' and dist_key_property == 'n/a'):
            sql_create_table_footer = f"""
            ,PRIMARY KEY ({primary_key})     
            )
            {sort_key_property}   
            """
        else:
            sql_create_table_footer = f"""  
            ) ;
            """

        column_data_type_sql = "".join(column_name_and_data_type_list)
        return_sql = f"{sql_create_table_header}{column_data_type_sql}{sql_create_table_footer}"
        ## The sqlparse will provide the desired SQL formatting
        return_sql = sqlparse.format(return_sql, keyword_case='upper',comma_first=True)
        return return_sql

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

    def get_record_count(self,schema,table):

        sql = f"""
                                SELECT COUNT(*) AS record_count
                                FROM {schema}.{table}
                            """
        return sql 

    def get_drop_table_sql(self,schema,table):

        sql = f"""
                                DROP TABLE IF EXISTS  {schema}.{table}
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
            engine_to = "redshift"
            separator_dot = "."
            separator_comma = ","
            separator_underscore = "_"
            property_name_pk = f'{engine_to}_varchar_max_length'
            job_name = function_id    
            now = datetime.now()  # current date and time
            date_string = now.strftime("%Y-%m-%d %H:%M:%S")
            db_engine = 'redshift'
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
                #     output_folder_path = 'output'
                # if args.datasets is None:
                #     datasets =   'all' ## 'heartbeat_stats,service_endpoints_with_heartbeats' ## 'inbound_call' ## 'all'

                logger.info(f"Profile: {profile}")
                logger.info(f"AWS Profile: {aws_profile}")
                logger.info(f"AWS Region: {aws_region}")
                logger.info(f"Env Prefix: {env_prefix}")
                logger.info(f"Output Folder Path: {output_folder_path}")
                logger.info(f"Datasets: {datasets}")

                ## Instantiate the  Metadata Class
                metadata = Metadata(aws_region,aws_service,aws_profile)

                s3_conn = S3(job_name,aws_profile)

                ## Retrieve ALL metadata from the property entity
                response_property = metadata.query_property("property",profile,property_name_pk) ## get_redshift_max_default_value(session, aws_service, property_name_pk)
                ## Retrieve the redshift_varchar_max_length value to use for the maximum size for the varchar
                for property in response_property:
                    redshift_max_length = property["value"]
                    logger.info(f"Redshift Maximum Length: {redshift_max_length}") 

                ## Retrieve ALL metadata from the datalake entity
                response_datalake = metadata.query("datalake","fqn",data_lake_fqn) ## get_cdc_datalake(session, aws_service, data_lake_fqn)

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
                    ## Retrieve ALL metadata from the publishing
                    ## This will retreive ALL publishing records by profile
                    ## Need to strip out the trailing comma at the end of datasets whenever calling the get_metadata method
                    response_dataset_publishing = metadata.get_publishing_metadata(profile,datasets.strip(separator_comma),engine_to) 

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
                        response_publishing = metadata.get_publishing_metadata(profile,dataset,engine_to)  

                        # Evaluate if the response object is empty
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
                            sort_key_list = []
                            dist_key_list = []
                            fqn_list = []
                            fqn = publish['fqn']
                            secret_name_list = []
                            db_engine = publish['db_engine']
                            output_folder_full_path  = ''                   
                            output_folder_full_path = f'{output_folder_path}/{db_engine}/{env_prefix}/'
                            pk = publish['primary_key']
                            secret_name = publish['connection_string']
                            sort_key = publish['sort_key']
                            dist_key = publish['dist_key']
                            analysis_catalog = publish['analysis_catalog']
                            analysis_table = publish["name"]  ## This is both the Catalog dataset name and the Redshift table name
                            schema = publish["schema"]
                            schema_stage = f'{schema}_stage'
                            table_name = publish["name"]  ## This is both the Catalog dataset name and the Redshift table name

                            ## Validating that there is ONLY one distkey in the metadata
                            dist_key_list_check = dist_key.split(separator_comma)
                            if len(dist_key_list_check) > 1:
                                exception_msg = f"Exception occurred inside this method {function_id} --> you can only have one distkey {dist_key} for a Redshift table. Please changed the metadata in the publishing table for {fqn}"
                                logger.exception(exception_msg)
                                raise Exception(exception_msg)

                            athena_metadata_query = self.get_athena_metadata(analysis_catalog,analysis_table)
                            print(f'Athena Metadata Query: {athena_metadata_query}')
                            logger.info(f'Athena Metadata Query: {athena_metadata_query}')

                            athena_prefix = f"{analysis_catalog}/schema/{schema}/{table_name}/date={date_string}/"
                            athena_output = f"s3://{s3_athena_bucket}/{athena_prefix}"
                            ## Use this to test out a scenario where the S3 bucket does NOT exists
                            ##s3_athena_bucket = "kinect-atlas-dev-query-results-bucket-v2"
                            
                            ## BEGIN Evaludate if the Athen S3 Bucket exists or not
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
                            metadata_datatype = metadata.query("data_type_translation","fqn",data_type_fqn) 

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
                                sort_key_list.append(sort_key)
                                dist_key_list.append(dist_key)
                                fqn_list.append(fqn)
                                secret_name_list.append(secret_name)
                                ## BEGIN all metadata is coming from the metadata_datatype list object
                                ordinal_position_list.append(ordinal_position)
                                data_type_list.append(data_type)
                                column_list.append(column_name)

                            ## Declare a list object to be used to identify if a pk column has been already defined inside the loop.
                            pk_colum_list = []
                            for table_name,column_name,data_type,ordinal_position,pk,sort_key,dist_key,schema,schema_stage,fqn,secret_name in zip(table_name_list,column_list,data_type_list,ordinal_position_list,pk_list,sort_key_list,dist_key_list,schema_list,schema_stage_list,fqn_list,secret_name_list):
                                ## BEGIN build out the columns and data type list object
                                if pk is None or pk == 'true':
                                    pk = 'n/a'
                                if sort_key == 'tbd' or sort_key is None or sort_key == 'true':
                                    sort_key = 'n/a'
                                if dist_key == 'tbd' or dist_key is None or dist_key == 'true':
                                    dist_key = 'n/a'
                                if pk != '':
                                    logger.info(f"Redshift Table: {table_name}")                            
                                    logger.info(f"Redshift Column Name: {column_name}")
                                    logger.info(f"Redshift Data Type: {data_type}")
                                    logger.info(f"Ordinal Position: {ordinal_position}")                                                     
                                    logger.info(f"PK: {pk}")
                                    logger.info(f"Sort Keys: {sort_key}")
                                    logger.info(f"Dist Keys: {dist_key}")
                                    logger.info(f"Redshift Schema: {schema}")
                                    logger.info(f"Redshift Stage Schema: {schema_stage}")  

                                    ## Note: May need to do this for the precision and/or scale of a numeric data type.
                                    ## BEGIN Evaluate if the data type is of a varchar or string data type, if so get the maximum size of the data value.                                
                                    if data_type == 'varchar':
                                        ## Use the redshift_max_length for the size of the varchar
                                        data_type = f'{data_type} ({redshift_max_length})'
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
                                stage_ddl = self.build_stage_ddl(schema_stage,table_name,column_name_and_data_type_list,separator_comma,pk)
                                base_ddl = self.build_ddl(schema,table_name,column_name_and_data_type_list,separator_comma,pk,sort_key,dist_key)

                                schema_stage_ddl = self.build_create_schema(schema_stage)
                                schema_ddl = self.build_create_schema(schema)

                                ## BEGIN Create/Drop/Re-Create schema and tables for MySQL
                                aws_secret = Secrets(job_name, secret_name)
                                secret_json = aws_secret.get_secret()

                                ## Instantiate the Redshift Class
                                redshift_conn = Redshift(job_name, secret_json)    

                                if  not has_schema_processed:
                                    redshift_conn.execute_sql(schema_stage_ddl)
                                    redshift_conn.execute_sql(schema_ddl)
                                    has_schema_processed = True

                                ## Query the information schema to see if the target table exists                            
                                table_query = self.get_table_query(schema,table_name)
                                rows = redshift_conn.return_dataset(table_query)
                                table_exists = rows[0]['record_count']                                                        

                                ## If the table is empty, then we can drop the target table
                                if  table_exists == 0:
                                    sql_drop_table = self.get_drop_table_sql(schema,table_name)
                                    redshift_conn.execute_sql(sql_drop_table)
                                else:                                
                                    sql_record_count = self.get_record_count(schema,table_name)
                                    ## Get the record count, to determine if the targe table is empty, is so we can drop and re-create the table                            
                                    rows = redshift_conn.return_dataset(sql_record_count)
                                    record_count = rows[0]['record_count']     
                                    logger.info(f"Record Count: {record_count}")
                                    ## Check the record_cou is 0,  then drop the target table
                                    if record_count == 0:
                                        sql_drop_table = self.get_drop_table_sql(schema,table_name)
                                        redshift_conn.execute_sql(sql_drop_table)
                                    else:
                                        logger.warning(f'Table: {schema}.{table_name} is NOT empty, the table has not been dropped and recreated')   

                                ## Get the drop stage table sql
                                sql_drop_stage_table = self.get_drop_table_sql(schema_stage,table_name)
                                ## Drop stage table
                                redshift_conn.execute_sql(sql_drop_stage_table)
                                redshift_conn.execute_sql(stage_ddl)
                                redshift_conn.execute_sql(base_ddl)

                                logger.info(f"Schema/Table: {schema}.{table_name}")                           
                                logger.info(f"Drop Stage Table SQL: {sql_drop_stage_table}")
                                logger.info(f"Stage DDL: {stage_ddl}")
                                logger.info(f"Target DDL: {base_ddl}")

                                ## END Create/Drop/Re-Create schema and tables for Redshift

                                ## Append the engine name to the output folder path
                                ## Check to see if folder exists, if not then create it.
                                output_folder_ddl_path = f'{output_folder_full_path}ddl/'
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
                                    writer.writelines(f'{base_ddl};')      

                                ## Inialize the boolean
                                has_schema_processed = False
                                if not has_schema_processed:
                                    schema_stage_ddl = self.build_create_schema(schema_stage)                               
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
                                    schema_ddl = self.build_create_schema(schema)
                                    python_script = f"{output_folder_schema_path}/{schema}_schema{sql_file_extension}"
                                    with open(python_script, "w") as writer:
                                        writer.writelines(schema_ddl)    

                                    logger.info(f"Stage Schema: {stage_ddl}")
                                    logger.info(f" Base Schema: {base_ddl}")   
                                    ## Flip the boolean to True   
                                    has_schema_processed = True

                                logger.info(f"Stage DDL: {stage_ddl}")
                                logger.info(f"Base DDl: {base_ddl}")
                                        
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
    RedshiftDDL().main(args)

