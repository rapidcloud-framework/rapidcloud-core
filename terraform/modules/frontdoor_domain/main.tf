resource "azurerm_cdn_frontdoor_custom_domain" "rc_frontdoor_domain" {
    name                        = local.domain_name
    cdn_frontdoor_profile_id    = var.profile_id
    dns_zone_id                 = var.dns_zone_id
    host_name                   = var.host_name

    tls {
      certificate_type          = "ManagedCertificate" #var.tls_cert_type
      minimum_tls_version       = "TLS12"
      #cdn_frontdoor_secret_id   = var.tls_cert_secret_id
    }    
}

# resource "azurerm_cdn_frontdoor_custom_domain_association" "example" {
#   cdn_frontdoor_custom_domain_id = azurerm_cdn_frontdoor_custom_domain.rc_frontdoor_domain.id
#   cdn_frontdoor_route_ids        = var.routes
# }

output "id" {
  value = azurerm_cdn_frontdoor_custom_domain.rc_frontdoor_domain.id
}

