resource "azurerm_container_app" "containerapp" {
  name                         = replace(var.name,"_","-")
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = var.resource_group
  revision_mode                = var.revision_mode

  template {
    container {
      name   = var.container_name
      image  = var.container_image # "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = var.container_cpu # 0.25
      memory = var.container_memory # "0.5Gi"
      args   = var.container_args

      liveness_probe {
        path = var.container_probe_path
        port = var.container_probe_port
        transport = var.container_probe_transport
      }
    }
    max_replicas = var.max_replicas
    min_replicas = var.min_replicas
  }

  identity {
    type           = var.identity_type
    identity_ids   = local.is_userassigned ? var.identity_ids : null
  }

  ingress {
    allow_insecure_connections = var.ingress_insecureconnections
    external_enabled           = true
    target_port                = var.ingress_target_port
    transport                  = var.ingress_transport

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
#   dynamic "traffic_weight" {
#     for_each = var.revision_mode == "Multiple" ? ["multiple"] : []

#     content {
#       revision_suffix        = var.traffic_revision_suffix
#       percentage             = var.traffic_percentage
#     }
#   }

  dynamic "secret" {
    for_each = var.registry_password != null && var.registry_password != "" ? ["secret"] : []

    content {
      name      = local.registry_password_name
      value     = var.registry_password
    }
  }

  dynamic "registry" {
    for_each = var.registry_server != null && var.registry_server != "" ? ["registry"] : []

    content {
        server               = var.registry_server
        identity             = local.enable_registry_identity ? var.registry_managed_identity : null
        password_secret_name = local.enable_registry_creds ? var.registry_password_name : null
        username             = local.enable_registry_creds ? var.registry_username : null
    }
  }

  tags = merge(local.rc_tags, var.tags)
}