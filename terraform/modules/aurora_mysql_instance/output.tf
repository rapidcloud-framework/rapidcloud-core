#------------------------------------------------------------------------------
# Outputs
#------------------------------------------------------------------------------

output "endpoint" {
  value = aws_rds_cluster.rds.endpoint
}

output "reader_endpoint" {
  value = aws_rds_cluster.rds.reader_endpoint
}

output "id" {
  value = aws_rds_cluster.rds.id
}

output "port" {
  value = aws_rds_cluster.rds.port
}

output "sg_id" {
  value = aws_security_group.mysql.id
}
