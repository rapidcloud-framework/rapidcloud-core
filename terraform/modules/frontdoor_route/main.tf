resource "azurerm_cdn_frontdoor_route" "rc_frontdoor_route" {
  name                          = var.name
  cdn_frontdoor_endpoint_id     = var.endpoint_id
  cdn_frontdoor_origin_group_id = var.origin_group_id
  cdn_frontdoor_origin_ids      = var.origins
  #cdn_frontdoor_rule_set_ids    = []
  enabled                       = true

  forwarding_protocol           = var.forwarding_protocol
  https_redirect_enabled        = var.redirect_https
  patterns_to_match             = var.patterns_to_match
  supported_protocols           = var.supported_protocols

  cdn_frontdoor_custom_domain_ids = var.domains
  #link_to_default_domain          = false

  dynamic "cache" {
    for_each = var.enable_caching ? ["cache"] : []

    content {
        query_string_caching_behavior = var.query_string_cache_behavior
    }
  }
}

output "id" {
  value = azurerm_cdn_frontdoor_route.rc_frontdoor_route.id
}
