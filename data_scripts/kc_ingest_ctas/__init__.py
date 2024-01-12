__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import os
import json
from datetime import datetime
import boto3
import fnmatch, re
from boto3.dynamodb.conditions import Key, Attr
import argparse
import logging 
from decimal import Decimal
from  data_scripts.kc_athena_access import Athena
from  data_scripts.kc_s3 import S3
from  data_scripts.kc_metadata import Metadata

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IngestCtas():

    def build_drop_ctas(self,schema_name, table_name):
        return f"""
                DROP  TABLE IF  EXISTS {schema_name}.{table_name}
            """


    def build_ctas_statement(self,raw_catalog,ingestion_catalog,schema_name,table_name,raw_location,column_name_list,cdc_action_column,ctas_table_format="PARQUET",ctas_compression="SNAPPY"):
        return f"""
                CREATE TABLE IF NOT EXISTS {raw_catalog}.{table_name}
                WITH (
                format = '{ctas_table_format}', 
                external_location = '{raw_location}/',
                parquet_compression = '{ctas_compression}'
                ) AS 
                SELECT {"".join(column_name_list) + cdc_action_column}
                FROM  {ingestion_catalog}.{table_name} ;
            """
        return sql


    def json_converter(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


    def main(self,args):
        function_id = sys._getframe().f_code.co_name
        separator = "_"
        separater_path = "/"
        separator_dataset = ","
        sql_file_extension = '.sql'
        cdc_action_value = 'initial load'
        cdc_action_column = f",'{cdc_action_value}' AS cdc_action"
        job_name = function_id    
        now = datetime.now()  # current date and time
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")
        aws_service = "dynamodb"
        source_table_dnmo_table = "source_table"
        source_column_dnmo_table = "source_column"
        
        try:
            env = args.env
            aws_profile = args.aws_profile.lower()
            aws_region = args.aws_region
            data_lake_fqn = args.data_lake_fqn.lower()
            output_folder_path = args.output_folder_path
            datasets = args.datasets

            logger.info(f"Env: {env}")
            logger.info(f"AWS Profile: {aws_profile}")
            logger.info(f"AWS Region: {aws_region}")
            logger.info(f"Data Lake FQN: {data_lake_fqn}")
            logger.info(f"Output Folder Path: {output_folder_path}")
            logger.info(f"Datasets: {datasets}")

            output_folder_path = f'{output_folder_path}/athena/ctas/'
            metadata = Metadata(aws_region,aws_service,aws_profile)
            s3_conn = S3(job_name,aws_profile)
        
            ## Retrieve ALL metadata from the datalake entity
            datalake =  metadata.query("datalake","fqn",data_lake_fqn)[0]
            logger.info(json.dumps(datalake, indent=2))
            s3_athena_bucket = datalake["athena_s3_bucket"].replace("_","-")

            if datasets == 'all' or datasets == '' or  datasets == 'all,':
                dataset_list = ['all']
            else:
                dataset_list = datasets.split(",")

            for dataset_name in dataset_list:
                logger.info( f"Inside datasets loop: {dataset_name}")
                response_dataset = metadata.get_metadata("dataset",env,dataset_name) 
                
                for dataset in response_dataset:
                    logger.info(json.dumps(dataset, indent=2))
                    column_name_list = [] 
                    source_database = dataset["source_database"]
                    source_schema = dataset["source_schema"]
                    table_name = dataset["source_table"]
                    target_table_name = dataset["name"]
                    ingestion_location = dataset["ingestion_location"]
                    ingestion_location_list = ingestion_location.split(separater_path)
                    ingestion_bucket = ingestion_location_list[2]
                    ingestion_catalog = dataset["ingestion_catalog"]
                    raw_catalog = dataset["raw_catalog"]
                    raw_location = dataset["raw_location"]
                    raw_location_list = raw_location.split(separater_path)
                    raw_bucket = raw_location_list[2]
                    
                    table_fqn = f"{env}_{source_database}_{source_schema}_{table_name}"           
                    table = metadata.query("source_table","fqn",table_fqn)[0]
                    logger.info(json.dumps(table, indent=2, default=self.json_converter))

                    schema_name = table["table_schema"]
                    table_rows = table["table_rows"]
                    pk_key = table["pk"]

                    s3_ingestion_prefix = f"{source_database}/{schema_name}/{target_table_name}/"
                    s3_raw_prefix = f"{source_database}/{schema_name}/{target_table_name}/"
                    athena_prefix = f"{ingestion_catalog}/tables/{schema_name}/{target_table_name}/date={date_string}/"
                    athena_output = f"s3://{s3_athena_bucket}/{athena_prefix}"

                    response_source_column = metadata.query("source_column", "table", table_fqn) 
                    loop_counter = 0
                    for column in response_source_column:
                        loop_counter += 1
                        column_name = column["column"]
                        if loop_counter != 1:
                            column_name = (f" ,{column_name} \n")
                        else:
                            column_name = (f" \n {column_name}  \n")
                        column_name_list.append(column_name)

                    athena_conn = Athena(job_name, athena_output,aws_profile)

                    ## Build the Athen Drop CTAS query
                    athena_drop_ctas_query = self.build_drop_ctas(raw_catalog, target_table_name)
                    logger.info(f"Athena Drop CTAS: {athena_drop_ctas_query}")
                    
                    ## Drop CTAS table before creating
                    athena_conn.executeSQL(athena_drop_ctas_query)

                    ## Build the Athena CTAS query
                    athena_ctas_query = self.build_ctas_statement(raw_catalog, ingestion_catalog, schema_name, target_table_name, raw_location,column_name_list,cdc_action_column)

                    print(f"Athena CTAS: {athena_ctas_query}")
                    logger.info(f"Athena CTAS: {athena_ctas_query}")

                    ## Check to see if the s3_Ingestion files are there, if not, then we cannot execute the Athena CTAS because this would cause an exception.
                    if  s3_conn.s3PrefixExists(ingestion_bucket, s3_ingestion_prefix) == True:
                        s3_conn.deleteFiles(raw_bucket, s3_raw_prefix)
                        athena_conn.executeSQL(athena_ctas_query)
                    else:
                        s3_raw_location = f'{raw_location}/'
                        exception_msg = f"Exception Occurred Inside this method {function_id} --> no data for  {s3_raw_location}"
                        logger.warning(exception_msg)
                        pass

                    ## BEGIN  write out DDL to a .sql file
                    ## Append the engine name to the output folder path
                    ## Check to see if folder exists, if not then create it.
                    if not os.path.exists(output_folder_path):
                        os.makedirs(output_folder_path)

                    ## Create the Python Transformation script
                    ctas_file_name_with_path = f'{output_folder_path}/{raw_catalog}{separator}{target_table_name}_ctas'
                    logger.info(f"CTAS Path: {ctas_file_name_with_path}")
                    ctas_script_file = f"{ctas_file_name_with_path}{sql_file_extension}"
                    with open(ctas_script_file, "w") as writer:
                            writer.writelines(athena_ctas_query)
                    ## END write out DDL to a .sql file

                    sys.exit() # test just one table

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_msg)
            raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="Please pass in the appropriate --profile")
    parser.add_argument("--aws_profile", required=True, help="Please pass in the appropriate --aws_profile")
    parser.add_argument("--aws_region", required=True, help="Please pass in the appropriate --aws_region")
    parser.add_argument("--data_lake_fqn",required=True,help="Please pass in the appropriate --data_lake_fqn")
    parser.add_argument("--output_folder_path",required=True,help="Please pass in the appropriate --output_folder_path")    
    parser.add_argument("--datasets",required=True,help="Please pass in the appropriate --datasets")  
    args = parser.parse_args()
    IngestCtas().main(args)

