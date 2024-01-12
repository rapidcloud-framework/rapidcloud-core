resource "azurerm_container_app_environment" "containerappenv" {
  name                       = replace(var.name, "_", "-")
  location                   = var.location
  resource_group_name        = var.resource_group
  log_analytics_workspace_id = var.log_analytics_workspace_id
  infrastructure_subnet_id   = var.infrastructure_subnet_id
  internal_load_balancer_enabled = var.internal_load_balancer_enabled
  tags = merge(local.rc_tags, var.tags)

}

output "id" {
  value = azurerm_container_app_environment.containerappenv.id
}