variable "lambda_function_name" {
  description = "The name of the lambda function, will be used for iam sns and s3 resources"
  type        = string
}

variable "lambda_iam_role" {
  description = "The IAM role arn to be used with this Lambda"
  type        = string
}

variable "handler" {
  description = "The lmabda function handler"
  type        = string
}

variable "description" {
  description = "The lmabda function description"
  type        = string
}

variable "runtime" {
  description = "The lambda runtime, see https://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html#SSS-CreateFunction-request-Runtime for values"
  type        = string
}

variable "memory_size" {
  description = "The lambda memory size"
  type        = number
  default     = 128
}

variable "lambda_env_vars" {
  description = "A list of environment variables used by the lambda function"
  type        = map
  default     = null
}

variable "timeout" {
  description = "The lambda timeout in seconds"
  type        = number
  default     = 3
}

variable "reserved_concurrent_executions" {
  description = "The amount of reserved concurrent executions for this lambda function"
  type        = string
  default     = ""
}

# if running in vpc
variable "vpc_id" {
  description = "The AWS vpc this function will run in"
  type        = string
  default     = ""
}

variable "subnets" {
  description = "The VPC subnets this lambda has access to"
  type        = list
  default     = []
}

variable "security_groups" {
  description = "The Security Group ID's attached to this lambda function"
  type        = list
  default     = []
}

variable "lambda_tags" {
  description = "Map of tags to assign to bucket"
  type        = map(string)
  default     = {}
}

variable "source_code_hash" {
  description = "The hash of the function package file"
  type        = string
  default     = ""
}

variable "filename" {
  description = "The path to the function package file"
  type        = string
  default     = ""
}

variable "s3_bucket" {
  description = "Name of s3 bucket that has the source code"
  type        = string
  default     = ""
}

variable "s3_key" {
  description = "Name of the zip/jar/deployment in the bucket"
  type        = string
  default     = ""
}

variable "s3_object_version" {
  description = "Version of the file in the bucket"
  type        = string
  default     = ""
}

variable "publish" {
  description = "Whether to publish creation/change as new Lambda Function Version"
  type        = string
  default     = "false"
}

variable "kms_key_arn" {
  description = "AWS Key Management Service (KMS) key that is used to encrypt environment variables"
  default     = ""
  type        = string
}

variable "layers" {
  description = "A list of layer ARN's to attach to the function"
  default     = []
  type        = list
}
