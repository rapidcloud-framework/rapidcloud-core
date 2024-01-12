variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "resource_group" {}

variable "sku_name" {}

variable "tags" {
    type = map(string)
    default = {}
}