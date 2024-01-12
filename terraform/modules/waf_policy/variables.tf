variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "location" {}
variable "resource_group" {}

variable "rule_set_version" {}

variable "tags" {
    type = map(string)
    default = {}
}