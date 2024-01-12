output "nfs_location_arn" {
  value = aws_datasync_location_nfs.source.arn
}
output "s3_location_arn" {
  value = aws_datasync_location_s3.destination.arn
}