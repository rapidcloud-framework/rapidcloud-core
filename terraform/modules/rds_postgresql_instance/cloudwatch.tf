resource "aws_cloudwatch_log_group" "psql" {
  name              = "/aws/rds/instance/${var.instance_name}/postgresql"
  retention_in_days = var.cloudwatch_logs_retention_in_days
}

