locals {
  node_pool_name            = "${var.name}"
  registry_password_name    = "docker-password"
  is_userassigned           = length(regexall("UserAssigned", var.identity_type)) > 0
  enable_registry_identity  = var.registry_managed_identity != null && var.registry_managed_identity != ""
  enable_registry_creds     = !local.enable_registry_identity && var.registry_username != null && var.registry_username != ""
  rc_tags = {
    Name        = var.name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
}