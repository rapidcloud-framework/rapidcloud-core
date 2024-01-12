resource "aws_rds_cluster" "psql" {
  cluster_identifier              = var.cluster_identifier
  port                            = var.port
  engine                          = "aurora-postgresql"
  engine_version                  = var.engine_version
  availability_zones              = var.azs
  database_name                   = var.database_name
  master_username                 = var.master_username
  master_password                 = var.master_password
  backup_retention_period         = var.backup_retention_period
  preferred_backup_window         = "07:00-09:00"
  copy_tags_to_snapshot           = true
  vpc_security_group_ids          = [aws_security_group.psql.id]
  db_subnet_group_name            = aws_db_subnet_group.psql.name
  deletion_protection             = var.deletion_protection
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.psql.name
  final_snapshot_identifier       = "${var.cluster_identifier}-final-snapshot"
  skip_final_snapshot             = var.skip_final_snapshot
  # psql doesn't support this yes
  # enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports
  kms_key_id        = var.kms_key_id
  storage_encrypted = var.storage_encrypted
  tags = merge(
    var.tags,
    {
      "Name" = var.cluster_identifier
    },
  )

  # RDS automatically assigns 3 AZs if less than 3 AZs are configured,
  # which will show as a difference requiring resource recreation next Terraform apply.
  # It is recommended to specify 3 AZs or use the lifecycle configuration block ignore_changes argument if necessary
  lifecycle {
    ignore_changes = [availability_zones]
  }

  depends_on = [aws_cloudwatch_log_group.psql]
}

