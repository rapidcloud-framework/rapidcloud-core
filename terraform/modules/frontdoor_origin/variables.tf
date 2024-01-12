variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "origin_group_id" {}

variable "hostname" {}

variable "certificate_check_enabled" {
    type = bool
    default = false
}