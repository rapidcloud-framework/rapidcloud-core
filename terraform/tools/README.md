## Generate Terraform resources using templates and dynamic variables

This script generates terraform resources using Jinja template, underlying terraform code and dynamic parameters.

Make sure to install jinja2 in your python environment:

`pip install jinja2`

Create jinja template for each target terraform resource. See example for a Lambda Function here:

https://github.com/rapid-cloud/community/blob/main/examples/aws/terraform/custom_templates/lambda_function.j2

Create Terraform modules for your target terraform resource. See example for a Lambda Function here:

https://github.com/rapid-cloud/community/tree/main/examples/aws/terraform/modules/lambda_function

Run this command line tool to merge template and module into final terraform resource:

```./terraform/tools/init.py --template ./terraform/custom_templates/lambda_function.j2 --module_dir ./terraform/modules/lambda_function --output_file ./terraform/init/lambda-function.tf --params ./terraform/tools/sample_lambda_params.json```

Here is an example of dynamic paremeters: https://github.com/rapid-cloud/community/blob/main/examples/aws/terraform/tools/sample_lambda_params.json
