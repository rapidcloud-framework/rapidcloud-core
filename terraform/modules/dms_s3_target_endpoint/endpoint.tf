resource "aws_dms_endpoint" "s3_target_endpoint" {
  certificate_arn             = var.certificate_arn
  kms_key_arn                 = var.kms_key_arn
  endpoint_id                 = var.endpoint_id
  endpoint_type               = "target"
  engine_name                 = "s3"
  extra_connection_attributes = var.extra_connection_attributes
  tags                        = var.tags

  s3_settings {
    service_access_role_arn   = aws_iam_role.dms_endpoint.arn
    external_table_definition = var.s3_external_table_definition
    csv_row_delimiter         = var.s3_csv_row_delimeter
    csv_delimiter             = var.s3_csv_delimiter
    bucket_folder             = var.s3_bucket_folder
    bucket_name               = var.s3_bucket_name
    compression_type          = var.s3_compression_type
  }
}
