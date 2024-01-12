__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import os
import json
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
import argparse
import logging 

from  data_scripts.kc_metadata import Metadata

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PublishRdsJob():

    def build_glue_mysql_python_job(self,glue_job_template,replace_from,replace_to):

            glue_job_python_shell  =  f"""
            {glue_job_template}
            """.format(
            "{}", ##schema_target
                "{}", ##schema_stage
                "{}", ##table
                "{}", ##schema_stage
                "{}", ##table
                "{}", ##table_target
                "{}", ##job_name
                "{}", ##catalog_database
                "{}", ##catalog_dataset
                "{}", ##jdbc_connection
                "{}", ##database_target
                "{}", ##schema_target
                "{}", ##schema_stage
                "{}", ##table_stage
                "{}", ##table_target
                "{}", ##secret
                "{}", ##functionID
                "{}", ##functionID
                "{}", ##secret_json
                "{}", ##truncate_table_target
                "{}", ##job_name
                "{}", ##e
                "{}", ##table_target
                "{}", ##database_target
                "{}", ##connection_option_string
                "{}", ##table_target
                "{}", ##table_stage
                "{}", ##replace_insert_sql
                "{}", ##job_name
                "{}", ##e
                "{}", ##job_name
                "{}", ##e
                "{}",
            )

            glue_job_output = glue_job_python_shell.replace(replace_from,replace_to).strip()
            glue_job_output = glue_job_output.replace('!','{')
            glue_job_output = glue_job_output.replace('^','}')
            return glue_job_output

    def build_glue_postgresql_python_job(self,glue_job_template,replace_from,replace_to):

                glue_job_python_shell  =  f"""
                {glue_job_template}
                """.format(
                    "{}", ##schema_target
                    "{}", ##schema_stage
                    "{}", ##table
                    "{}", ##schema_stage
                    "{}", ##table
                    "{}", ##table_target
                    "{}", ##job_name
                    "{}", ##catalog_database
                    "{}", ##catalog_dataset
                    "{}", ##jdbc_connection
                    "{}", ##database_target
                    "{}", ##schema_target
                    "{}", ##schema_stage
                    "{}", ##table_stage
                    "{}", ##table_target
                    "{}", ##secret
                    "{}", ##functionID
                    "{}", ##functionID
                    "{}", ##secret_json
                    "{}", ##truncate_table_target
                    "{}", ##job_name
                    "{}", ##e
                    "{}", ##table_target
                    "{}", ##database_target
                    "{}", ##connection_option_string
                    "{}", ##table_target
                    "{}", ##table_stage
                    "{}", ##truncate_table_target
                    "{}", ##e
                    "{}", ##job_name
                    "{}", ##replace_insert_sql
                    "{}", ##job_name
                    "{}", ##e
                    "{}", ##job_name
                    "{}", ##e
                    "{}",
                )

                glue_job_output = glue_job_python_shell.replace(replace_from,replace_to).strip()
                glue_job_output = glue_job_output.replace('!','{')
                glue_job_output = glue_job_output.replace('^','}')
                return glue_job_output
                
    def main(self,args):

        ## DECLARATION SECTION
        function_id = sys._getframe().f_code.co_name
        aws_service = "dynamodb"
        dynamo_table = "publishing"       
        separator_comma = ','
        separator_dataset = ","
        python_file_extension = '.py'
        # db_engine = 'mysql'
        # publish_folder = db_engine
        glue_job_template_folder = 'modules/job_templates'
        glue_job_template_file_prefix = 'kc_publishing_job_'
        ##glue_job_template_file = f"{glue_job_template_file_prefix}{python_file_extension}"
        replace_from = '~~~'
        replace_to =  '"""'
        has_built_output_folder_path = False

        try:

            
            if args.profile:
                profile = args.profile.lower()
            if args.aws_profile:
                 aws_profile = args.aws_profile.lower()
            if args.aws_region:
                aws_region = args.aws_region
            if args.env_prefix:
                env_prefix = args.env_prefix.lower()
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
            # if args.output_folder_path is None:
            #     output_folder_path = 'output'
            # if args.datasets is None:
            #     datasets =  'all' ## 'heartbeat_stats,service_endpoints_with_heartbeats' ## 'inbound_call' ## 'all'

            logger.info(f"Profile: {profile}")
            logger.info(f"AWS Profile: {aws_profile}")
            logger.info(f"AWS Region: {aws_region}")
            logger.info(f"Env Prefix: {env_prefix}")
            logger.info(f"Output Folder Path: {output_folder_path}")
            logger.info(f"Datasets: {datasets}")
        
            ## Instantiate the  Metadata Class
            metadata = Metadata(aws_region,aws_service,aws_profile)

            if datasets.lower() == 'all' or datasets == '' or  datasets.lower() == 'all,':
                datasets = 'all,'
                dataset_list =  datasets.split(separator_dataset)
            else:
                ## Evaluate if the last character has a comma, and if not, then add in a comma at the end of the datasets variable.
                if datasets.endswith(separator_comma):
                    dataset_list = datasets.split(separator_dataset)
                else:
                    ## Adding in a comma at the tail end of the datasets variable
                    datasets = f'{datasets},'
                    dataset_list = datasets.split(separator_dataset)

            loop_count = 0
            ## Note: We are no longer creating a Glue PythonShell job template for each dataset, instead we will ONLY write 1 per profile.
            while loop_count <=1:
                loop_count += 1
                for dataset in dataset_list:

                    ## If there are no more elements in the list array then do NOT process. We are adding in an extra comma at the tail end of the datasets variable, so this will give us an 
                    ## empty array element, so this would NOT process into the for loop.
                    if not dataset:
                        pass
                    else:

                        ## Retrieve ALL metadata from the transformation
                        response_publishing = metadata.get_publishing_metadata(profile,dataset)  ## metadata.get_publishing(profile,db_engine,dataset)  ## get_publishing(session, aws_service, profile,dataset)
                        ##response_publishing = metadata.get_metadata("publishing",profile,dataset) ## get_publishing(session, aws_service, profile,dataset)

                        ## Evaluate if the response object is empty
                        if len(response_publishing) == 0:
                            exception_msg = f"Exception Occurred Inside this method {function_id} --> No metadata returned for {dynamo_table} no value for {dataset}"
                            logger.warning(exception_msg)
                            pass

                        for publish in response_publishing:
                            db_engine = publish["db_engine"]
                            publish_folder = db_engine
                            if has_built_output_folder_path == False:
                                ## Build the output path
                                output_folder_path = f'{output_folder_path}/glue/publish/{publish_folder}/{env_prefix}/'
                                has_built_output_folder_path = True
                            glue_job_template_file = f"{glue_job_template_file_prefix}{db_engine}_template{python_file_extension}"
                            
                            glue_template_file = f"{glue_job_template_folder}/{glue_job_template_file}"
                            with open(glue_template_file,mode='r') as glue_template_file:
                                    # read all lines at once
                                    glue_job_template = glue_template_file.read()

                                    if db_engine.lower() == 'mysql':
                                        glue_job = self.build_glue_mysql_python_job(glue_job_template,replace_from,replace_to)
                                        print(glue_job)
                                        logger.info(glue_job)
                                    elif db_engine.lower() == 'postgresql':
                                        glue_job = self.build_glue_postgresql_python_job(glue_job_template,replace_from,replace_to)
                                        print(glue_job)
                                        logger.info(glue_job)                                    

                                    ## Append the engine name to the output folder path
                                    ## Check to see if folder exists, if not then create it.
                                    if not os.path.exists(output_folder_path):
                                        os.makedirs(output_folder_path)

                                    ## Create the Python Transformation script
                                    glue_publish_job_template = f'{profile}_publish_job_template'
                                    ##python_script = f"{output_folder_path}/{glue_string_name_prefix}{python_file_extension}"
                                    python_script = f"{output_folder_path}/{glue_publish_job_template}{python_file_extension}"
                                    with open(python_script, "w") as writer:
                                        writer.writelines(glue_job)

        except Exception as e:
            msg = e.args
            exception_msg = f"Exception Occurred Inside this method {function_id} --> Here is the exception Message {msg}"
            logger.error( exception_msg)
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
    PublishRdsJob().main(args)    




