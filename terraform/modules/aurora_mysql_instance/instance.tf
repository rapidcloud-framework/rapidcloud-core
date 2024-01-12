#------------------------------------------------------------------------------
# RDS Cluster Instance
#------------------------------------------------------------------------------
resource "aws_rds_cluster_instance" "rds" {
  # Instance count; perhaps in prod one per az
  # count                 = "${length(var.aws_subnet_db_prv_ids)}"
  count = var.cluster_instance_count

  engine_version = var.engine_version
  engine         = "aurora-mysql"

  identifier              = "${var.cluster_identifier}-${count.index}"
  cluster_identifier      = aws_rds_cluster.rds.id
  instance_class          = var.cluster_instance_size
  db_subnet_group_name    = aws_db_subnet_group.rds.name
  monitoring_interval     = var.monitoring_interval
  monitoring_role_arn     = var.monitoring_interval > 0 ? aws_iam_role.rds.arn : ""
  publicly_accessible     = false
  db_parameter_group_name = aws_db_parameter_group.rds_db.name

  tags = merge(
    var.tags,
    {
      "Name" = var.cluster_identifier
    },
  )

  lifecycle {
    create_before_destroy = true
  }
}
