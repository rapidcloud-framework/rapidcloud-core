resource "aws_cloudwatch_log_group" "rds_error" {
  name              = "/aws/rds/cluster/${var.cluster_identifier}/error"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

resource "aws_cloudwatch_log_group" "rds_audit" {
  name              = "/aws/rds/cluster/${var.cluster_identifier}/audit"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

resource "aws_cloudwatch_log_group" "rds_general" {
  name              = "/aws/rds/cluster/${var.cluster_identifier}/general"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

resource "aws_cloudwatch_log_group" "rds_slowquery" {
  name              = "/aws/rds/cluster/${var.cluster_identifier}/slowquery"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

