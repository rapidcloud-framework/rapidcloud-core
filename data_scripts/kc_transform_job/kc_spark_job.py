__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import os
import json
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sqlparse
import argparse
import logging
from  data_scripts.kc_metadata import Metadata

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SparkJob():
        
    def __init__(self, args):
        self.args = args

    def build_glue_spark_job(self,glue_job_template,analysis_bucket, env_prefix, dataset_name,cte_query_list):

        cte_query = "".join(cte_query_list).strip('')
        ## The sqlparse will provide the desired SQL formatting
        cte_query_final = sqlparse.format(cte_query, reindent=True, keyword_case='upper',comma_first=True)
        glue_job_spark_output = f"""
        {glue_job_template}
        """.format(
            "{}", ## s3_analysis_bucket  
            "{}", ## table
            "{}",                   
            "{}",
            cte_query_final,
            "{}", ## write_path
            "{}", ## job_name
            "{}", ## e
        )
        return glue_job_spark_output.strip()

    def  build_main_cte(self,target_dataset_name,transform_query,list_length):

            base_sql = f"""

            --  BEGIN CTE for {target_dataset_name} 
            WITH cte_{target_dataset_name} 
            AS
                (
                    {transform_query}            
            """
            if list_length == 1:
                sql = f"""
                            {base_sql} 
                            ) 

                            -- END CTE for {target_dataset_name} 
                            
                            -- SELECT from the single CTE here
                            SELECT * FROM cte_{target_dataset_name} 
                        """        
            else:
                sql = f"""
                            {base_sql}                        
                            )
                            
                            --  END CTE for {target_dataset_name} 
                        """            
            return sql

    def  build_secondary_cte(self,target_dataset_name,transform_query):

            sql = f"""

            --  BEGIN CTE for {target_dataset_name} 
            ,cte_{target_dataset_name} 
            AS
                (
                    {transform_query}    
                    )
                --  END CTE for {target_dataset_name}                             
            """
                                
            return sql

    def build_transform_query(self,raw_catalog,target_dataset_name,pk_key,column_name_list,update_timestamp,max_length, dataset_type):
            
            ## If pk is empty, then use the column_name_list in the PARTITION BY and the ORDER BY in the window function below.
            if (pk_key is None or pk_key == ''):
                pk_key = column_name_list

            ## Building out the following:
            ## 1. WHERE clause predicate in the NOT EXISTS query. These are built based upon the PK's, and if there are no PK's, then we build this on all of the columns in the table.
            ## 2. Build the window function PARTION and ORDER BY clauses, which are based upon the PK's for a table. If there are no PK's, then we use all of the columns in the table.
            window_column_list = []
            where_clause_list = []
            pk_sub_query = []
            
            logger.info(f"pk: {pk_key}")
            for pk in pk_key.split(","):
                if not pk_sub_query:
                    window_column_list.append(f's.{pk}')                        
                    where_clause_list.append(f'WHERE s2.{pk} = s.{pk} \n')
                else:
                    window_column_list.append(f',s.{pk}')
                    where_clause_list.append(f'AND s2.{pk} = s.{pk} \n')       
                pk_sub_query.append(f"COALESCE(CAST(s.{pk} AS VARCHAR({max_length})),'~') || ")

            if dataset_type == 'dataset':
                where_clause_list.append(f"AND lower(s2.cdc_action) = 'd'")
    
            where_clause = "".join(where_clause_list)
            window_partition_by = "".join(window_column_list)
            pk_sub_query = "".join(pk_sub_query).strip()
            logger.info("pk_sub_query:")
            logger.info(pk_sub_query)

            ## If there is a double pipe at the end of business key, replace it
            if pk_sub_query.endswith('||'):
                pk_sub_query = pk_sub_query[:-2]

            list_length = len(column_name_list)
            loop_count = 1
            column_append_list = []

            for column in column_name_list:
                if not column_append_list:
                    column_append_list.append(f' s.{column} ')
                else:
                    column_append_list.append(f' ,s.{column}')    
            column_append_list.append(f',s.cdc_action') 

            ## These columns have an alias with each of the select column list,, such as s.<<column_name>>.
            ##sub_query_select_list = "".join(column_append_list)
            ## These columns do not have an alias for each of the select column list. 
            main_query_select_list = "".join(column_name_list)  + ',cdc_action'

            ## Add in the update_timestamp if there is a value in the dataset metadata
            if update_timestamp.lower() != 'n/a':
                window_order_by = f'{window_partition_by} ,s.{update_timestamp} DESC'
            else:
                window_order_by = window_partition_by
            
            ## I removed the sub_query_select_list in the inner query and replaced it with s.* instead.
            ## {sub_query_select_list}
            # concat_business_key
            # {main_query_select_list}
            sql = f"""
                SELECT 
                concat_business_key
                ,{main_query_select_list}
                FROM 
                (
                    SELECT
                        {pk_sub_query} AS concat_business_key
                        ,s.*
                        ,ROW_NUMBER() OVER (PARTITION BY {window_partition_by} ORDER BY  {window_order_by}) AS top_slice
                    FROM {raw_catalog}.{target_dataset_name} s
                    WHERE NOT EXISTS
                        (  
                            SELECT 1
                            FROM  {raw_catalog}.{target_dataset_name} s2
                            {where_clause}    
                        )
                    )
                WHERE top_slice = 1 
            """
            return sql.strip()


    def json_converter(self, obj):
        return str(obj)
        

    def main(self,args):
        try:
            profile = args.profile.lower()
            aws_profile = args.aws_profile.lower()
            aws_region = args.aws_region
            env_prefix = args.env_prefix.lower()
            output_folder_path = args.output_folder_path
            datasets = args.datasets

            logger.info(f"Env: {profile}")
            logger.info(f"AWS Profile: {aws_profile}")
            logger.info(f"AWS Region: {aws_region}")
            logger.info(f"Env Prefix: {env_prefix}")
            logger.info(f"Output Folder Path: {output_folder_path}")
            logger.info(f"Transformation Fqn: {datasets}")

            metadata = Metadata(aws_region, "dynamodb", aws_profile)
            max_length = metadata.query_property("property",profile,"athena_varchar_max_length")[0]['value']

            # Build the output path for storing generated transformation template
            output_folder_path = f"{output_folder_path}/glue/transform/{env_prefix}/"

            # Get transformation items
            transformations = []
            if datasets == "all":
                transformations = metadata.get_metadata("transformation", profile, "all") 
            else:
                for dataset in datasets.split(","):
                    transformations.append(metadata.get_metadata("transformation", profile, dataset))

            # process each transformation and generate code template
            for transform in transformations:

                # get Glue job template    
                glue_template_file = f"data_scripts/job_templates/kc_transform_job_template.py"
                with open(glue_template_file,mode='r') as glue_template_file:
                    glue_job_template = glue_template_file.read()

                logger.info("Transformation:")
                logger.info(json.dumps(transform, indent=2))

                dataset_name = transform["name"]  
                analysis_bucket = transform["analysis_bucket"]

                cte_query_list = []              
                column_name_list = []
                table_id_list = []
                update_timestamp_list = []

                # get base datasets
                datasets_count = len(transform['base_datasets'])
                base_datasets = []
                for dataset in transform['base_datasets']:  
                    # try dataset 
                    fqn = f"{profile}_{dataset}"           
                    response_dataset = metadata.query("dataset", "fqn", fqn) 
                    if len(response_dataset) == 0:
                        # try dataset_semi_structured
                        response_dataset = metadata.query("dataset_semi_structured", "fqn", fqn)
                        if len(response_dataset) == 0:
                            continue

                    base_datasets.append(response_dataset[0])

                logger.info("Base Datasets:")
                logger.info(json.dumps(base_datasets, indent=2))
              
                # process each base dataset
                cte_query_list = []
                for base_dataset in base_datasets:
                    
                    col_list = []

                    # dataset for rdbms source
                    if 'source_database' in base_dataset:
                        table_fqn = f"{profile}_{base_dataset['source_database']}_{base_dataset['source_schema']}_{base_dataset['source_table']}"
                        
                        # get source_table info for base dataset from dynamodb metadata
                        source_table = metadata.query("source_table", "fqn", table_fqn)
                        if len(source_table) > 0:
                            dataset_type = "dataset"
                            source_table = source_table[0]
                            logger.info("source_table:")
                            logger.info(json.dumps(source_table, indent=2, default=self.json_converter))
                            base_table_name = source_table['table_name']
                            pk = source_table['pk']
                            update_timestamp = base_dataset['update_timestamp']

                            # build column list for source_table
                            source_columns = metadata.query("source_column", "table", table_fqn)
                            for column in source_columns:
                                if not col_list:
                                    col_list.append(f"{column['column']} \n")
                                else:
                                    col_list.append(f",{column['column']} \n")
                        else:
                            continue

                    # dataset for csv or json source
                    elif 'source_location' in base_dataset:
                        # try Glue catalog to get source table info
                        glue_table = metadata.get_glue_table_info(transform['raw_catalog'], base_dataset['name']) 
                        if glue_table:
                            dataset_type = "dataset_semi_structured"
                            logger.info("glue table:")
                            logger.info(json.dumps(glue_table, indent=2, default=self.json_converter))
                            base_table_name = base_dataset['name']
                            pk = base_dataset['pk']
                            # update_timestamp = glue_table['update_timestamp']

                            # build column list for source_table
                            for column in glue_table['Table']['StorageDescriptor']['Columns']:
                                if not col_list:
                                    col_list.append(f"{column['Name']} \n")
                                else:
                                    col_list.append(f",{column['Name']} \n")

                        else:
                            continue

                    logger.info("col_list:")
                    logger.info(json.dumps(col_list, indent=2))

                    # build transform query
                    transform_query = self.build_transform_query(transform['raw_catalog'], base_table_name, pk, col_list, update_timestamp, max_length, dataset_type)

                    # build CTE query
                    if not cte_query_list:
                        cte_query = self.build_main_cte(base_table_name, transform_query, datasets_count)
                    else:
                        cte_query = self.build_secondary_cte(base_table_name, transform_query)
                    cte_query_list.append(cte_query)

                # build final Spark job query
                glue_spark_job = self.build_glue_spark_job(glue_job_template, analysis_bucket, env_prefix, dataset_name, cte_query_list)

                # This is done for each transformation
                # Check to see if folder exists, if not then create it. 
                output_folder_path = output_folder_path.replace("//","/")           
                if not os.path.exists(output_folder_path):
                    logger.info(f"creating {output_folder_path}")
                    os.makedirs(output_folder_path)

                ## Create the Python Transformation script
                python_script = f"{output_folder_path}/{transform['fqn']}.py".replace("//","/")
                with open(python_script, "w") as writer:
                    logger.info(f"writing {python_script}")
                    writer.writelines(glue_spark_job)

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {sys._getframe().f_code.co_name} --> Here is the exception Message {msg}"
            logger.exception(exception_msg)
            raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="Please pass in the appropriate --profile")
    parser.add_argument("--aws_profile", required=True, help="Please pass in the appropriate --aws_profile")
    parser.add_argument("--aws_region", required=True, help="Please pass in the appropriate --aws_region")
    parser.add_argument("--env_prefix", required=True,help="Please pass in the appropriate --env_prefix")
    parser.add_argument("--output_folder_path", required=True,help="Please pass in the appropriate --output_folder_path")
    parser.add_argument("--datasets",required=True,help="Please pass in the appropriate --datasets")
    args = parser.parse_args()
    TransformationJob().main(args)