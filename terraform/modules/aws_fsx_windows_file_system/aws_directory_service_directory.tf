resource "aws_directory_service_directory" "aws_ad_service" {
  name     = var.ad_service_name
  password = var.ad_admin_password
  size     = var.ad_size
  type     = var.ad_type
  vpc_settings {
    vpc_id     = var.vpc_id
    subnet_ids = var.subnet_ids
  }

  tags = var.tags
}