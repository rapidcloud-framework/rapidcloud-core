output "arn" {
  value       = aws_redshift_cluster.redshift.arn
  description = "Amazon Resource Name (ARN) of cluster"
}

output "id" {
  value       = aws_redshift_cluster.redshift.id
  description = "The Redshift Cluster ID."
}

output "cluster_identifier" {
  value       = aws_redshift_cluster.redshift.cluster_identifier
  description = "The Cluster Identifier"
}

output "endpoint" {
  value       = aws_redshift_cluster.redshift.endpoint
  description = "The connection endpoint"
}

output "dns_name" {
  value       = aws_redshift_cluster.redshift.dns_name
  description = "The DNS name of the cluster"
}

output "port" {
  value       = aws_redshift_cluster.redshift.port
  description = "Port of the cluster"
}

output "sg_id" {
  value = aws_security_group.redshift.id
}
