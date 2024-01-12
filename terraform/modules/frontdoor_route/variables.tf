variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "resource_group" {}

variable "endpoint_id" {}

variable "origin_group_id" {}

variable "origins" {
    type = list(string)
}

variable "patterns_to_match" {
    type = list(string)
    default = [ "/*" ]
}

variable "supported_protocols" {
    type = list(string)
    default = [ "Http", "Https" ]
}

variable "redirect_https" {
    type = bool
    default = true
}

variable "enable_caching" {
  type = bool
  default = false
}

variable "query_string_cache_behavior" {}

variable "forwarding_protocol" {}

variable "domains" {
    type = list(string)
    default = []
}

variable "tags" {
    type = map(string)
    default = {}
}