variable "name" {}
variable "profile" {}
variable "resource_group" {}
variable "location" { default = "eastus" }

variable "aks_version" { default = "1.26"}
variable "desired_size" { default = 2 }
variable "max_size" { default = 5 }
variable "min_size" { default = 0 }
variable "vm_size" { default = "Standard_D2_v2" }

variable "node_pool_zones" { default = ["1","2","3"]}

variable "azure_cni_enabled" {
  default = true
}

variable "network_policy" {
  default = "azure"
}

variable "auto_upgrade" {
  default = true
}

variable "vnet_subnet_id" {}

variable "dns_service_ip" {}

variable "service_cidr" {}

variable "pod_cidr" {
    default = null
}

variable "private_cluster_enabled" {
    type = bool
  default = true
}

variable "authorized_ip_ranges" {
    type = list(string)
    default = []
}

variable "api_server_vnet_integrated_enabled" {
    type = bool
  default = false
}

variable "api_server_subnet_id" {
    type = string
    default = null
}

variable "aad_enabled" {
  default = true
}

variable "rbac_aad_admin_group_object_ids" {
    type = list(string)
    default = []
}

variable "azure_rbac_enabled" {
    type = bool
  default = true
}

variable "blob_driver_enabled" {
        type = bool
  default = true
}

variable "disk_driver_enabled" {
        type = bool
  default = true
}

variable "file_driver_enabled" {
        type = bool
  default = true
}


variable "log_analytics_workspace_id" {}

variable "tags" {
    type = map(string)
    default = {}
}
#variable "eviction_policy" { default = "Delete" }
# variable "node_labels" {
#   default = {
#     "kubernetes.azure.com/scalesetpriority" = "spot"
#   }
# }
# variable "node_taints" {
#   default = [
#         "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"
#   ]
# }