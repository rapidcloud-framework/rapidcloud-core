resource "azurerm_application_gateway" "network" {
  name                       = replace(var.name, "_", "-")
  location                   = var.location
  resource_group_name        = var.resource_group
  zones                      = var.zones
  enable_http2               = var.enable_http2

  sku {
    name      = var.tier
    tier      = var.tier
    capacity  = var.enable_autoscaling ? null : var.capacity
  } 

  gateway_ip_configuration {
    name      = local.gateway_ip_configuration
    subnet_id = var.subnet_id
  } 

  frontend_port {
    name      = local.frontend_port_name
    port      = var.frontend_port
  }   

  frontend_ip_configuration {
    name                  = local.frontend_configuration_name
    public_ip_address_id  = var.public_ip_addr_id
  }

  backend_address_pool {
    name          = local.backend_address_pool_name
    ip_addresses  = var.backend_ips
    fqdns         = var.backend_fqdns
  }

  backend_http_settings {
    name                  = local.backend_http_settings_name
    cookie_based_affinity = "Disabled"
    port                  = var.backend_port
    protocol              = var.backend_protocol
  }   

  http_listener {
    name                            = local.http_listener_name
    frontend_ip_configuration_name  = local.frontend_configuration_name
    frontend_port_name              = local.frontend_port_name
    protocol                        = var.http_listener_protocol
  }     

  request_routing_rule {
    name                        = "rc-gateway-routingrule"
    rule_type                   = var.routing_rule_type
    http_listener_name          = local.http_listener_name
    backend_address_pool_name   = local.backend_address_pool_name
    backend_http_settings_name  = local.backend_http_settings_name
    priority                    = 1
  }

  dynamic "identity" {
    for_each = length(var.identity_ids) > 0 ? ["identity"] : []

    content {
      type          = "UserAssigned"
      identity_ids  = var.identity_ids
    }
  }

  dynamic "autoscale_configuration" {
    for_each = var.enable_autoscaling ? ["autoscale"] : []

    content {
      min_capacity = var.min_capacity
      max_capacity = var.capacity
    }
  }

  dynamic "probe" {
    for_each = var.enable_probe ? ["probe"] : []

    content {
      host          = var.health_probe_host
      interval      = 30
      name          = local.probe_name
      protocol      = var.health_probe_protocol
      path          = var.health_probe_path
      timeout       = 30
      unhealthy_threshold = 5
    } 
  }

  dynamic "waf_configuration" {
    for_each = var.enable_waf ? ["waf"] : []
    
    content {
      enabled             = var.enable_waf
      firewall_mode       = var.firewall_mode
      rule_set_type       = var.rule_set_type
      rule_set_version    = var.rule_set_version
    }
  }

  firewall_policy_id                = var.waf_policy_id
  force_firewall_policy_association = var.waf_policy_id != "" ? true : null

  tags = merge(local.rc_tags, var.tags)

}