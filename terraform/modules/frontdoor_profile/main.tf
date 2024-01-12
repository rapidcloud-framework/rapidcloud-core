resource "azurerm_cdn_frontdoor_profile" "rc_frontdoor_profile" {
    name                = var.name
    resource_group_name = var.resource_group
    sku_name            = var.sku_name

    tags = merge(local.rc_tags, var.tags)
}

output "id" {
  value = azurerm_cdn_frontdoor_profile.rc_frontdoor_profile.id
}