resource "aws_redshift_cluster" "redshift" {
  cluster_identifier     = "${var.cluster_name}-redshift-cluster"
  database_name          = var.database_name
  master_username        = var.master_username
  master_password        = var.master_password
  node_type              = var.node_type
  number_of_nodes        = var.node_count
  cluster_type           = var.node_count > 1 ? "multi-node" : "single-node"
  port                   = var.cluster_port
  vpc_security_group_ids = [aws_security_group.redshift.id]

  cluster_subnet_group_name    = aws_redshift_subnet_group.redshift.id
  cluster_parameter_group_name = aws_redshift_parameter_group.redshift.id

  # this module assumes we're in a vpc, always
  publicly_accessible = false

  # maintenanc
  preferred_maintenance_window = var.preferred_maintenance_window
  allow_version_upgrade        = var.allow_version_upgrade

  # Snapsshots
  snapshot_identifier                 = var.snapshot_identifier
  snapshot_cluster_identifier         = var.snapshot_cluster_identifier
  final_snapshot_identifier           = var.cluster_name
  skip_final_snapshot                 = var.skip_final_snapshot
  automated_snapshot_retention_period = var.automated_snapshot_retention_period

  encrypted  = var.encrypted
  kms_key_id = var.kms_key_id

  logging {
    enable        = var.enable_logging
    bucket_name   = "${var.cluster_name}-logging"
    s3_key_prefix = "${var.cluster_name}/"
  }

  tags      = var.tags
  iam_roles = var.iam_roles

  lifecycle {
    ignore_changes = [master_password]
  }

  timeouts {
    create = "60m"
  }
}

