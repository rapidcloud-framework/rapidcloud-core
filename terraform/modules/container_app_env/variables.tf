variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "location" {}
variable "resource_group" {}

variable "infrastructure_subnet_id" {}

variable "log_analytics_workspace_id" {}

variable "internal_load_balancer_enabled" { default = false }

variable "tags" {
    type = map(string)
    default = {}
}