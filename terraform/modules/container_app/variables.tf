variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "container_app_environment_id" {}

variable "resource_group" {}

variable "revision_mode" {}

variable "container_name" {}
variable "container_image" {}
variable "container_cpu" {}
variable "container_memory" {}
variable "container_args" {
    type = list(string)
    default = []
}
variable "container_probe_path" {
    default = "/"
}
variable "container_probe_port" {
  default = 80
}
variable "container_probe_transport" {
  default = "HTTP"
}

variable "max_replicas" {
    default = 3
}
variable "min_replicas" {
    default = 1
}

variable "identity_type" {
  default = "SystemAssigned"
}

variable "identity_ids" {
  type = list(string)
  default = []
}

variable "ingress_target_port" {
  default = 80
}

variable "ingress_transport" {
  default = "auto"
}

variable "ingress_insecureconnections" {
  default = true
}

variable "registry_server" {
}
variable "registry_managed_identity" {}
variable "registry_password" {}
variable "registry_username" {}

variable "tags" {
    type = map(string)
    default = {}
}