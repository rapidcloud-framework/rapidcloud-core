resource "aws_cloudtrail" "main" {
  name                          = var.name
  s3_bucket_name                = var.s3_bucket_name
  include_global_service_events = var.include_global_service_events
  enable_log_file_validation    = var.enable_log_file_validation
  is_organization_trail         = var.is_organization_trail
  is_multi_region_trail         = var.is_multi_region_trail
  kms_key_id                    = var.kms_key_id
}