resource "aws_redshift_subnet_group" "redshift" {
  name        = var.cluster_name
  description = "subnet group of ${var.cluster_name}"
  subnet_ids  = var.subnets
  tags        = var.tags
}
