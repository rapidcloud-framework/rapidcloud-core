variable "stack_name" {
  type = string
}

variable "conformity_aws_account_name" {
  type = string
  description = "This is the AWS name to be linked with Conformity"
}

variable "conformity_environment" {
  type = string
  description = "This is the corresponding environment for the aws account to be linked"
}

variable "tags" {
    type = list(string)
}