resource "aws_cloudwatch_log_group" "psql" {
  name              = "/aws/rds/instance/${var.cluster_identifier}/postgresql"
  retention_in_days = var.db_logs_retention_in_days
}

