locals {
  gateway_ip_configuration = "rc-gateway-ip"
  frontend_configuration_name = "rc-gateway-feip"
  frontend_port_name = "rc-gateway-feport"
  http_listener_name = "rc-gateway-listener"
  backend_address_pool_name = "rc-gateway-be"
  backend_http_settings_name = "rc-gateway-behttp"
  waf_policy_name = "rc-gateway-waf-policy"
  probe_name = "rc-gateway-probe"
  rc_tags = {
    Name        = var.name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
}