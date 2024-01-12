output "arn" {
  value = aws_dms_replication_instance.dms_instance.replication_instance_arn
}

output "sg_id" {
  value = aws_security_group.dms_security_group.id
}
