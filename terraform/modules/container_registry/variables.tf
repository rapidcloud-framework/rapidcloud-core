variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "location" {}
variable "resource_group" {}

variable "sku" {}

variable "enable_public_access" {
    type = bool
    default = true
}

variable "enable_encryption" {
    type = bool
    default = true
}

variable "encryption_key_id" {
    type = string
    default = null
}

variable "encryption_client_id" {
    type = string
    default = null
}

variable "identity_ids" {
    type = list(string)
    default = []
}

variable "identity_type" {
    type = string
    default = null
}

variable "enable_admin" { default = false }

variable "geolocations" {
  type = list(string)
  default = []
}

variable "tags" {
    type = map(string)
    default = {}
}