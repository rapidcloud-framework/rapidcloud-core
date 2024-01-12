variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}
variable "container_app_environment_id" {}

variable "certificate_blob_base64" {}

variable "certificate_password" {}

variable "tags" {
    type = map(string)
    default = {}
}