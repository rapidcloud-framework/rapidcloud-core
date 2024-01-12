resource "aws_dms_replication_subnet_group" "dms_subnet" {
  replication_subnet_group_description = "Replication subnet group for ${var.replication_instance_id}"
  replication_subnet_group_id          = "${var.replication_instance_id}-replication-subnet"
  subnet_ids                           = var.replication_group_destination_subnets
}
