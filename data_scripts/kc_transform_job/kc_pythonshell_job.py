__license__ = "MIT"

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

class PythonshellJob():
        
    def __init__(self, args):
        self.args = args

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