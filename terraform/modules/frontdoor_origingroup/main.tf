resource "azurerm_cdn_frontdoor_origin_group" "rc_frontdoor_og" {
    name                        = var.name
    cdn_frontdoor_profile_id    = var.profile_id
    health_probe {
      protocol                  = var.health_probe_protocol
      path                      = var.health_probe_path
      interval_in_seconds       = 30
    }       

    load_balancing {
      additional_latency_in_milliseconds = 0
      sample_size                        = 16
      successful_samples_required        = 3
    }           
}

output "id" {
  value = azurerm_cdn_frontdoor_origin_group.rc_frontdoor_og.id
}