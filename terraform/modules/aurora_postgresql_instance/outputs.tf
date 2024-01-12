output "endpoint" {
  value = aws_rds_cluster.psql.endpoint
}

output "reader_endpoint" {
  value = aws_rds_cluster.psql.reader_endpoint
}

output "port" {
  value = aws_rds_cluster.psql.port
}

output "id" {
  value = aws_rds_cluster.psql.id
}

output "arn" {
  value = aws_rds_cluster.psql.id
}

output "sg_id" {
  value = aws_security_group.psql.id
}

