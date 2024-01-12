resource "aws_db_subnet_group" "psql" {
  name       = var.cluster_identifier
  subnet_ids = var.subnet_ids
  tags       = var.tags
}

