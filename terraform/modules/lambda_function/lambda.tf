# data archive_file lambda {
#   type        = zip
#   source_dir  = ${path.module}/source/${var.runtime}/function
#   output_path = ${path.module}/zip/function.zip
# }

locals {
  environment_map = var.lambda_env_vars == null ? [] : [var.lambda_env_vars]
}

#create the function
resource aws_lambda_function function {
  function_name    = var.lambda_function_name
  role             = var.lambda_iam_role
  handler          = var.handler
  description      = var.description
  runtime          = var.runtime
  filename         = var.filename != "" ? var.filename : null
  kms_key_arn      = var.kms_key_arn != "" ? var.kms_key_arn : null
  source_code_hash = var.source_code_hash != "" ? var.source_code_hash : null

  #use deployment from s3 bucket (This conflicts with providing filename and source_code_hash)
  s3_bucket         = var.s3_bucket != "" ? var.s3_bucket : null
  s3_key            = var.s3_key != "" ? var.s3_key : null
  s3_object_version = var.s3_object_version != "" ? var.s3_object_version : null

  memory_size                    = var.memory_size
  timeout                        = var.timeout
  publish                        = var.publish
  reserved_concurrent_executions = var.reserved_concurrent_executions != "" ? var.reserved_concurrent_executions : null

  vpc_config {
    subnet_ids         = var.subnets
    security_group_ids = var.security_groups
  }

  dynamic environment {
    for_each = local.environment_map
    content {
      variables = environment.value
    }
  }

  lifecycle {
    ignore_changes = [filename, description]
  }

  layers = var.layers

  tags = var.lambda_tags
}
