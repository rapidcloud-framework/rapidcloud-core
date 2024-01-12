variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "profile_id" {}

variable "tags" {
    type = map(string)
    default = {}
}