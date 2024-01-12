resource "azurerm_cdn_frontdoor_endpoint" "rc_frontdoor_ep" {
    name                     = var.name
    cdn_frontdoor_profile_id = var.profile_id

    tags = merge(local.rc_tags, var.tags)
}

output "id" {
  value = azurerm_cdn_frontdoor_endpoint.rc_frontdoor_ep.id
}