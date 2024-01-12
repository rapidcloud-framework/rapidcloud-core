resource "aws_cloudwatch_log_group" "rds_error" {
  name              = "/aws/rds/instance/${var.instance_name}/error"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

resource "aws_cloudwatch_log_group" "rds_audit" {
  name              = "/aws/rds/instance/${var.instance_name}/audit"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

resource "aws_cloudwatch_log_group" "rds_general" {
  name              = "/aws/rds/instance/${var.instance_name}/general"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

resource "aws_cloudwatch_log_group" "rds_slowquery" {
  name              = "/aws/rds/instance/${var.instance_name}/slowquery"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

