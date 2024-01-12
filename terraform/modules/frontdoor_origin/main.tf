resource "azurerm_cdn_frontdoor_origin" "rc_frontdoor_origin" {
    name                            = var.name
    cdn_frontdoor_origin_group_id   = var.origin_group_id
    enabled                         = true
    certificate_name_check_enabled  = var.certificate_check_enabled
    host_name                       = var.hostname
}

output "id" {
  value = azurerm_cdn_frontdoor_origin.rc_frontdoor_origin.id
}