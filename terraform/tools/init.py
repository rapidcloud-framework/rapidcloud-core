#!/usr/bin/env python3

import json
import argparse
from jinja2 import Template

"""
make sure to install jinja2 in your python environment:

    `pip install jinja2`


example:

    ./terraform/tools/init.py --template ./terraform/custom_templates/lambda_function.j2 --module_dir ./terraform/modules/lambda_function --output_file ./terraform/init/lambda-function.tf --params ./terraform/tools/sample_lambda_params.json 
"""

parser = argparse.ArgumentParser()
parser.add_argument('--template', required=True, help="Jinja Template location")
parser.add_argument('--module_dir', required=True, help="Terraform module location")
parser.add_argument('--output_file', required=True, help="Generated terraform file full path")
parser.add_argument('--params', required=False, help="Json file with dynamic params/configuration")
args = parser.parse_args()

with open(args.template, "r") as template_file:
    try:
        template_file_contents = template_file.read()
        if template_file_contents:
            params = {}
            if args.params:
                with open(args.params, "r") as params_file:
                    params = json.load(params_file)
            for object in params:
                parts = args.output_file.split('/')
                base_filename = parts[-1].split('.')[0]
                resource_file = open(f"./{object['resource_name']}_{base_filename}.tf", 'a')
                object['module_source'] = args.module_dir
                jinja_template = Template(template_file_contents)
                rendered_jinja_template = jinja_template.render(object)
                resource_file.write(rendered_jinja_template)
                resource_file.close()
                print(f"saved: {object['resource_name']}_{base_filename}.tf")
    except Exception as e:
        print(e)