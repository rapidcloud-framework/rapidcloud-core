# General Requirements

`aws account`: you aws account must have the correct IAM policies to create all the resources needed

`vpc`: this code assumes you have an existing vpc and it is updated in the `profile` dynamo table

`subnets`: the resource created in using this code all reside in internal (none public facing) and they contain `prv` in the name tag


# Python Requirements
The following pip modules are needed:

  - boto3
  - jinja2
  - argparse

# Terraform

### Install Terraform
Follow the instructions on this page: https://learn.hashicorp.com/terraform/getting-started/install.html

### Create Terraform Infrastructure

The following is needed for terraform state file management

- a dynamoDB table with a `LockID` primary key, the table name needs to be in `profile.state_lock_table`
- an s3 bucket with encryption and versioning turned on, the bucket name needs to be in `profile.state_bucket`

### Access to kinect bitbucket for module downloads

Terraform will need to do a git pull on several generic modules consumed by this code

### AWS credentials

Terraform will need a valid AWS key/secret to use for creating the resources

# Code Deployment

Once all of the above is set, you can create the AWS infra using the commands below, the code
uses **relative** paths and should be run from the `terraform` folder
In the examples below, substitute ${p} with the profile name

## INIT
The init phase creates the infra code, you should run init before any other terraform action

## kc init

This command consumes the `aws_infra` defined resources and creates the terraform resources.

`./bin/kc-init.py --table aws_infra --profile ${p}`

## terraform init

This command will download all the terraform modules, and init a state in the s3 bucket

`terraform init`
## DEPLOY

### terraform plan

This command outputs all the changes that will be applied to the AWS infra

`terraform plan`

### terraform apply

This command will create all the resource outlined in the plan, it will prompt the user for a yes/no

`terraform apply  -parallelism=1`

### terraform destroy

This command will **DESTROY** all the resource outlined in the plan, it will prompt the user for a yes/no

**ALWAYS RUN A PLAN BEFORE DESTROY !!!**

`terraform destroy  -parallelism=1`

