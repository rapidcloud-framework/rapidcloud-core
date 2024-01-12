resource "aws_dms_replication_instance" "dms_instance" {
  allocated_storage          = var.allocated_storage
  apply_immediately          = var.apply_immediately
  auto_minor_version_upgrade = var.auto_minor_version_upgrade
  # availability_zone            = var.availability_zone
  engine_version               = var.engine_version
  kms_key_arn                  = var.kms_key_arn
  multi_az                     = var.multi_az
  preferred_maintenance_window = var.preferred_maintenance_window
  publicly_accessible          = var.publicly_accessible
  replication_instance_class   = var.replication_instance_class
  replication_instance_id      = var.replication_instance_id
  replication_subnet_group_id  = aws_dms_replication_subnet_group.dms_subnet.id
  tags                         = var.tags
  vpc_security_group_ids       = [aws_security_group.dms_security_group.id]

  timeouts {
    create = "60m"
  }
}
