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
import sqlparse
from  data_scripts.kc_athena_access import Athena
from  data_scripts.kc_s3 import S3
from  data_scripts.kc_metadata import Metadata

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IngestDDL():

    def build_drop_dll(self,ingestion_catalog, target_table_name):
        return f"""
            DROP TABLE IF EXISTS {ingestion_catalog}.{target_table_name};
        """


    def build_parquet_ddl(self,ingestion_location,ingestion_catalog,schema_name,target_table_name,table_rows,format,compression,column_name_and_data_type_list):
        
        if (compression.upper() != 'NONE' or compression == ''):
            table_properties = f'tblproperties ("parquet.compression"="{compression}") '
        else:
            table_properties = ''
        format = format.upper()
        compression = compression.upper()
        
        sql_create_table_header = f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS `{ingestion_catalog}.{target_table_name}`(
        """

        sql_create_table_footer = f"""  
            )
            STORED AS {format}
            LOCATION '{ingestion_location}/'
            {table_properties} ;
        """        

        column_data_type_sql = "".join(column_name_and_data_type_list)  
        return_sql = (
            f"{sql_create_table_header}{column_data_type_sql}{sql_create_table_footer}"
        )
        return return_sql


    def build_ddl(self,ingestion_location,ingestion_catalog,schema_name,target_table_name,table_rows,format,compression,column_name_and_data_type_list):

        if (format.upper() == 'CSV'):
            delimiter = ','
        elif (format.upper() == 'PIPE'):
            delimiter = '|'
        elif (format.upper() == '\t'):
            delimiter = '\t'
        else:
            delimiter = ','

        if (compression.upper() != 'NONE' or compression == ''):
            compression_type = f"compressionType'='{compression},"
        else:
            compression_type = ''

        sql_create_table_header = f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS `{ingestion_catalog}.{target_table_name}`(
        """

        sql_create_table_footer = f"""  
            )
                ROW FORMAT DELIMITED 
                FIELDS TERMINATED BY ',' 
                STORED AS INPUTFORMAT 
                'org.apache.hadoop.mapred.TextInputFormat' 
                OUTPUTFORMAT 
                'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
                LOCATION
                '{ingestion_location}/'
                TBLPROPERTIES (
                'CrawlerSchemaDeserializerVersion'='1.0', 
                'CrawlerSchemaSerializerVersion'='1.0', 
                'areColumnsQuoted'='false', 
                'classification'='csv', 
                'columnsOrdered'='true', 
                '{compression_type}'
                'delimiter'='{delimiter}', 
                'recordCount'='{table_rows}', 
                'skip.header.line.count'='1', 
                'typeOfData'='file'
            ) ;
        """        
        column_data_type_sql = "".join(column_name_and_data_type_list)  
        return_sql = (
            f"{sql_create_table_header}{column_data_type_sql}{sql_create_table_footer}"
        )
        return return_sql


    def json_converter(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


    def create_glue_table(self, athena_conn, athena_ddl, ddl_script_file):
        logger.info(f"Athena DDL: {athena_ddl}")

        # create Glue catalog table
        athena_conn.executeSQL(athena_ddl)

        # save DDL
        with open(ddl_script_file, "w") as writer:
            formatted_ddl = sqlparse.format(athena_ddl, keyword_case='upper')
            writer.writelines(formatted_ddl)


    def main(self,args):        
        function_id = sys._getframe().f_code.co_name
        job_name = function_id  
        now = datetime.now()  # current date and time
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")
        athena_data_type = ""    

        try:
            env = args.env.lower()
            aws_profile = args.aws_profile.lower()
            aws_region = args.aws_region
            data_lake_fqn = args.data_lake_fqn.lower()
            output_folder_path = args.output_folder_path
            datasets = args.datasets

            logger.debug(f"Env: {env}")
            logger.debug(f"AWS Profile: {aws_profile}")
            logger.debug(f"AWS Region: {aws_region}")
            logger.debug(f"Data Lake FQN: {data_lake_fqn}")
            logger.debug(f"Output Folder Path: {output_folder_path}")
            logger.debug(f"Datasets: {datasets}")

            output_folder_path = f'{output_folder_path}/athena/ddl/'
            metadata = Metadata(aws_region,"dynamodb",aws_profile)
            s3_conn = S3(job_name,aws_profile)

            ## Retrieve ALL metadata from the datalake entity
            datalake =  metadata.query("datalake","fqn",data_lake_fqn)[0]
            logger.debug(json.dumps(datalake, indent=2))
            s3_athena_bucket = datalake["athena_s3_bucket"].replace("_","-")

            if datasets == 'all' or datasets == '' or  datasets == 'all,':
                dataset_list = ['all']
            else:
                dataset_list = datasets.split(",")

            for dataset_name in dataset_list:
                logger.debug( f"Inside datasets loop: {dataset_name}")
                response_dataset = metadata.get_metadata("dataset",env,dataset_name) 
                
                for dataset in response_dataset:
                    logger.debug(json.dumps(dataset, indent=2))

                    column_name_and_data_type_list = []
                    source_database = dataset["source_database"]
                    source_schema = dataset["source_schema"]
                    table_name = dataset["source_table"]
                    target_table_name = dataset["name"]
                    ingestion_location = dataset["ingestion_location"]
                    raw_location = dataset["raw_location"]
                    ingestion_catalog = dataset["ingestion_catalog"]
                    raw_catalog = dataset["raw_catalog"]
                    compression = dataset['compression']
                    format = dataset['format']

                    table_fqn = f"{env}_{source_database}_{source_schema}_{table_name}".lower()  
                    logger.debug(f"fqn: {table_fqn}")        
                    table = metadata.query("source_table","fqn", table_fqn)[0]
                    logger.debug(json.dumps(table, indent=2, default=self.json_converter))
                    
                    schema_name = table["table_schema"]
                    table_rows = table["table_rows"]
                    engine = table["engine"]
                    pk_key = table["pk"]

                    athena_prefix = f"{ingestion_catalog}/tables/{schema_name}/{target_table_name}/date={date_string}/"
                    athena_output = f"s3://{s3_athena_bucket}/{athena_prefix}"

                    s3_conn.deleteFiles(s3_athena_bucket, athena_prefix)
                    athena_conn = Athena(job_name, athena_output,aws_profile)

                    ## BEGIN retrieve source column metadata
                    ## Set the loop_counter value
                    datatype_mappings =  metadata.query("data_type_translation", "fqn", f"{engine}_athena")

                    loop_counter = 0
                    response_source_column = metadata.query("source_column", "table", table_fqn) 
                    for column in response_source_column:

                        ## increment the loop_counter. This is used to determine if what is the first column, so that we can not include a comma in the SELECT column.
                        loop_counter += 1
                        column_name = column["column"].lower()
                        source_data_type = column["data_type"]
                        
                        source_column_type = column["column_type"]
                        if not source_column_type: # oracle, mssql
                            data_length = column["data_length"]
                            data_precision = column["data_precision"]
                            data_scale = column["data_scale"]
                            if data_precision and data_precision != 0:
                                if data_scale is not None:
                                    source_column_type = f"{source_data_type}({data_precision},{data_scale})"
                                else:
                                    source_column_type = f"{source_data_type}({data_precision})"
                            else:
                                source_column_type = f"{source_data_type}({data_length})"
                        source_column_type = source_column_type.lower()

                        logger.debug(f"mapping: {table_name}.{column_name} / {source_data_type} / {source_column_type}")
                        ## END retrieve source column metadata

                        ##for key, value in metadata_datatype.items():
                        for key in datatype_mappings:
                            cast_from = key["cast_from"]
                            cast_to = key["cast_to"]
                            # logger.debug(f"mapping: {source_column_type} -> {cast_from} -> {cast_to}")
                            if fnmatch.fnmatch(source_column_type, cast_from):
                                athena_data_type = cast_to
                            elif source_column_type in (cast_from):
                                athena_data_type = cast_to

                        ## Check to see if the athena_data_type does NOT have a value, if true, then raise an exception
                        if (athena_data_type is None):
                            exception_msg = f"Exception Occurred Inside this method {function_id} --> Data Type {source_data_type} not regeristered in metadata"
                            raise Exception(exception_msg)

                        logger.debug(f"mapping: athena: {athena_data_type}")

                        ## BEGIN build out the columns and data type list object
                        if loop_counter != 1:
                            column_name_and_data_type = (f",\n  `{column_name}` {athena_data_type}")
                        else:
                            column_name_and_data_type = (f"\n  `{column_name}` {athena_data_type}")
                        
                        ## Append to the list object
                        column_name_and_data_type_list.append(column_name_and_data_type)
                        ## END build out the columns and data type list object

                    ## Build the Athena Drop DDL query
                    athena_drop_ddl = self.build_drop_dll(ingestion_catalog, target_table_name)
                    logger.debug(f"Athena Drop DDL: {athena_drop_ddl}")

                    athena_conn.executeSQL(athena_drop_ddl)

                    # generate local output dir for DDL
                    if not os.path.exists(output_folder_path):
                        os.makedirs(output_folder_path)

                    # -------------------------------------------------------
                    # Ingestion
                    # -------------------------------------------------------

                    ## Build the Athena DDL query
                    if format.upper() == 'PARQUET':
                        athena_ddl = self.build_parquet_ddl(ingestion_location,ingestion_catalog,schema_name,target_table_name,table_rows,format,compression,column_name_and_data_type_list)
                    else:
                        athena_ddl = self.build_ddl(ingestion_location,ingestion_catalog,schema_name,target_table_name,table_rows,format,compression,column_name_and_data_type_list)

                    ddl_script_file = f'{output_folder_path}{ingestion_catalog}_{target_table_name}_ddl.sql'                    
                    self.create_glue_table(athena_conn, athena_ddl, ddl_script_file)

                    # -------------------------------------------------------
                    # Raw
                    # -------------------------------------------------------

                    ## Build the Athena DDL query
                    column_name_and_data_type_list.append(f",\n  `cdc_action` string")
                    if format.upper() == 'PARQUET':
                        athena_ddl = self.build_parquet_ddl(raw_location,raw_catalog,schema_name,target_table_name,table_rows,format,compression,column_name_and_data_type_list)
                    else:
                        athena_ddl = self.build_ddl(raw_location,raw_catalog,schema_name,target_table_name,table_rows,format,compression,column_name_and_data_type_list)

                    ddl_script_file = f'{output_folder_path}{raw_catalog}_{target_table_name}_ddl.sql'
                    self.create_glue_table(athena_conn, athena_ddl, ddl_script_file)

                    # sys.exit() # to test one table and exit

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error(exception_msg)
            raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, help="Please pass in the appropriate --env")
    parser.add_argument("--aws_profile", required=True, help="Please pass in the appropriate --aws_profile")
    parser.add_argument("--aws_region", required=True, help="Please pass in the appropriate --aws_region")
    parser.add_argument("--data_lake_fqn",required=True,help="Please pass in the appropriate --data_lake_fqn")
    parser.add_argument("--output_folder_path",required=True,help="Please pass in the appropriate --output_folder_path")    
    parser.add_argument("--datasets",required=True,help="Please pass in the appropriate --datasets")  
    args = parser.parse_args()
    IngestDDL().main(args)

