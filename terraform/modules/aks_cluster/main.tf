resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group
  dns_prefix          = replace("${var.name}-aks","_","-")
  automatic_channel_upgrade = var.auto_upgrade ? "patch": "none" #use properties to define upgrade channel
  kubernetes_version  = var.aks_version
  azure_policy_enabled = true

  default_node_pool {
    name                = "default"
    enable_auto_scaling = true
    node_count          = var.desired_size
    max_count           = var.max_size
    min_count           = var.min_size
    vm_size             = var.vm_size
    zones               = var.node_pool_zones
    vnet_subnet_id      = var.azure_cni_enabled ? var.vnet_subnet_id : null
  }

  network_profile {
    network_plugin    = var.azure_cni_enabled || var.network_policy == "azure" ? "azure" : "kubenet"
    load_balancer_sku = "standard"
    network_policy = var.azure_cni_enabled ? var.network_policy : "calico"
    dns_service_ip = var.azure_cni_enabled ? var.dns_service_ip : null
    pod_cidr = !var.azure_cni_enabled ? var.pod_cidr : null
    service_cidr = var.azure_cni_enabled ? var.service_cidr : null
  }

  identity {
    type = "SystemAssigned"
  }

  private_cluster_enabled = var.private_cluster_enabled 

  public_network_access_enabled = !var.private_cluster_enabled

  dynamic "azure_active_directory_role_based_access_control" {
    for_each = var.aad_enabled || length(var.rbac_aad_admin_group_object_ids) > 0 ? ["rbac"] : []

    content {
      admin_group_object_ids = var.rbac_aad_admin_group_object_ids 
      azure_rbac_enabled     = var.azure_rbac_enabled
      managed                = true
      #tenant_id              = var.rbac_aad_tenant_id
    }
  }

  dynamic "api_server_access_profile" {
    for_each = var.private_cluster_enabled == false || var.api_server_vnet_integrated_enabled ? ["api_server_access_profile"] : []

    content {
      authorized_ip_ranges      = var.private_cluster_enabled == false ? var.authorized_ip_ranges != null ? var.authorized_ip_ranges : ["0.0.0.0/32"] : null
      subnet_id                 = var.api_server_vnet_integrated_enabled ? var.api_server_subnet_id : null
      vnet_integration_enabled  = var.api_server_vnet_integrated_enabled
    }
  }

  dynamic "storage_profile" {
    for_each = var.blob_driver_enabled || var.disk_driver_enabled || var.file_driver_enabled ? ["storage_profile"] : []

    content {
      blob_driver_enabled         = var.blob_driver_enabled
      disk_driver_enabled         = var.disk_driver_enabled
      file_driver_enabled         = var.file_driver_enabled
    }
  }

  key_vault_secrets_provider {
    secret_rotation_enabled = true
  }
  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }

  lifecycle {
    ignore_changes = [ default_node_pool[0].node_count ]
  }

  tags = merge(local.rc_tags, var.tags)
  
}

output "id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "client_key" {
  value = azurerm_kubernetes_cluster.aks.kube_config.0.client_key
}

output "client_certificate" {
  value = azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate
}

output "cluster_ca_certificate" {
  value = azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate
}

output "host" {
  value = azurerm_kubernetes_cluster.aks.kube_config.0.host
}