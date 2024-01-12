resource "aws_dms_endpoint" "source_endpoint" {
  certificate_arn             = var.certificate_arn
  kms_key_arn                 = var.kms_key_arn
  endpoint_id                 = var.endpoint_id
  endpoint_type               = "source"
  engine_name                 = var.engine_name
  extra_connection_attributes = var.extra_connection_attributes
  password                    = var.password
  username                    = var.username
  port                        = var.port
  server_name                 = var.server_name
  database_name               = var.database_name
  tags                        = var.tags
  ssl_mode                    = var.ssl_mode
}
