resource "aws_rds_cluster_instance" "psql" {
  count                = var.cluster_instance_count
  identifier           = "${var.cluster_identifier}-${count.index + 1}"
  cluster_identifier   = aws_rds_cluster.psql.id
  instance_class       = var.cluster_instance_size
  engine               = "aurora-postgresql"
  engine_version       = var.engine_version
  db_subnet_group_name = aws_db_subnet_group.psql.name
  tags = merge(
    var.tags,
    {
      "Name" = "${var.cluster_identifier}-${count.index + 1}"
    },
  )
}

