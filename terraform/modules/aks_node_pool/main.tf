resource "azurerm_kubernetes_cluster_node_pool" "aksnodepool" {
  name                  = replace(var.name,"_","-")
  kubernetes_cluster_id = var.cluster_id
  orchestrator_version  = var.aks_version
  vm_size               = var.instance_size
  node_count            = var.node_count
  max_count             = var.max_size
  min_count             = var.min_size
  enable_auto_scaling   = true
  os_sku                = var.os_sku
  os_type               = var.node_pool_mode == "System" ? "Linux" : var.os_type
  priority              = var.use_spot_instance ? "Spot" : "Regular"
  eviction_policy       = var.eviction_policy
  zones                 = var.zones
  vnet_subnet_id        = var.subnet_id
  mode                  = var.node_pool_mode
  capacity_reservation_group_id = var.capacity_reservation_group_id
  node_labels           = var.node_labels
  node_taints           = var.node_taints
  os_disk_size_gb       = var.os_disk_size_gb

  tags = merge(local.rc_tags, var.tags)
}