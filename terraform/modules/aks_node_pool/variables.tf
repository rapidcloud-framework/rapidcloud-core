variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}
variable "cluster_id" {}
variable "cluster_name" {}
variable "aks_version" {
  default = "1.26"
}

variable "node_count" { default = 2 }
variable "max_size" { default = 5 }
variable "min_size" { default = 0 }
variable "instance_size" { default = "Standard_D2_v2" }

variable "os_sku" {
  default = "Ubuntu"
}

variable "os_type" {
  default = "Linux"
}

variable "node_pool_mode" {
  default = "User"
}

variable "use_spot_instance" {
  default = false
}

variable "eviction_policy" {
  default = "Delete"
}

variable "zones" { default = ["1","2","3"]}

variable "subnet_id" {}

variable "capacity_reservation_group_id" {
    default = null
}

variable "node_labels" {
    type = map(string)
    default = {}
}

variable "node_taints" {
    type = list(string)
    default = []
}

variable "os_disk_size_gb" {
  default = 50
}

variable "tags" {
    type = map(string)
    default = {}
}