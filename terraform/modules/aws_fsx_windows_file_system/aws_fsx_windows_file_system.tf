resource "aws_fsx_windows_file_system" "file_system" {
  active_directory_id = aws_directory_service_directory.aws_ad_service.id
  storage_capacity    = var.storage_capacity
  subnet_ids          = var.subnet_ids
  deployment_type     = var.deployment_type
  throughput_capacity = var.throughput_capacity
  preferred_subnet_id = var.preferred_subnet_id
  tags                = var.tags
}