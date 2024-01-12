resource "azurerm_container_registry" "containerreg" {
  name                       = replace(var.name, "_", "-")
  location                   = var.location
  resource_group_name        = var.resource_group
  sku                        = var.sku
  public_network_access_enabled = var.enable_public_access
  admin_enabled              = var.enable_admin
  
  dynamic "encryption" {
    for_each = var.enable_encryption ? ["encryption"] : []

    content {
      enabled                  = var.enable_encryption
      key_vault_key_id         = var.encryption_key_id
      identity_client_id       = var.encryption_client_id
    }
  }

  dynamic "identity" {
    for_each = var.encryption_client_id != null || var.identity_type != null ? ["identity"] : []

    content {
      type                   = var.identity_type != null ? var.identity_type : "UserAssigned"
      identity_ids           = var.identity_ids
    }
  }

  dynamic "georeplications" {
    for_each = length(var.geolocations) < 1 ? toset([]) : var.geolocations
    iterator = item

    content {
      location          = item.value
    }
  }

  tags = merge(local.rc_tags, var.tags)

}

output "id" {
  value = azurerm_container_registry.containerreg.id
}