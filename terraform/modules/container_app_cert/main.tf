resource "azurerm_container_app_environment_certificate" "containerappenvcert" {
  name                         = replace(var.name,"_","-")
  container_app_environment_id = var.container_app_environment_id
  certificate_blob_base64      = <<EOF
   ${var.certificate_blob_base64}
  EOF
  certificate_password         = var.certificate_password

  tags = merge(local.rc_tags, var.tags)
}