#------------------------------------------------------------------------------
# Data Section
#------------------------------------------------------------------------------
# Define and associate subnets to db subnets group
resource "aws_db_subnet_group" "rds" {
  name        = var.cluster_identifier
  description = "Allowed subnets for Aurora DB cluster instances"
  subnet_ids  = var.db_subnets

  tags = {
    Name        = var.cluster_identifier
    Environment = var.env
  }
}

#------------------------------------------------------------------------------
# RDS Cluster
#------------------------------------------------------------------------------
resource "aws_rds_cluster" "rds" {
  cluster_identifier              = var.cluster_identifier
  database_name                   = var.database_name
  master_username                 = var.master_username
  master_password                 = var.master_password
  engine_version                  = var.engine_version
  engine                          = var.engine
  backup_retention_period         = var.backup_retention_period
  enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery"]
  preferred_backup_window         = "02:00-03:00"
  preferred_maintenance_window    = "wed:03:00-wed:04:00"
  db_subnet_group_name            = aws_db_subnet_group.rds.name
  final_snapshot_identifier       = var.cluster_identifier
  vpc_security_group_ids          = [aws_security_group.mysql.id]
  deletion_protection             = var.deletion_protection
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.rds_cluster.name

  tags = merge(
    var.tags,
    {
      "Name" = var.cluster_identifier
    },
  )

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_cloudwatch_log_group.rds_audit]
}
