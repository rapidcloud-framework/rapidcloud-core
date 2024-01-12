variable "name" {}
variable "profile" {}
variable "env" {}
variable "cmd_id" {}
variable "workload" {}

variable "location" {}
variable "resource_group" {}

variable "tier" {}
variable "enable_autoscaling" {
    type = bool
    default = false
}

variable "min_capacity" {}
variable "capacity" {}

variable "zones" {}

variable "enable_http2" {}

variable "subnet_id" {}

#variable "private_ip_addr" {}
variable "public_ip_addr_id" {}

variable "frontend_port" {}

variable "enable_waf" {
  type = bool
  default = false
}

variable "firewall_mode" {
  type = string
}

variable "rule_set_type" {
  type = string
}

variable "rule_set_version" {
  type = string
}

variable "waf_policy_id" {
  type = string
  default = null
}

#variable "backend_pools" {}

#variable "backend_http_settings" {}
variable "backend_ips" {
  type = list(string)
  default = []
}
variable "backend_fqdns" {
  type = list(string)
  default = []
}
variable "backend_port" {}
variable "backend_protocol" {}

#variable "frontend_configurations" {}

#variable "http_listeners" {}
variable "http_listener_protocol" {}


#variable "request_routing_rules" {}
variable "routing_rule_type" {}

variable "identity_ids" {
    type = list(string)
    default = []
}

variable "enable_probe" {
  type = bool
  default = false
}

variable "health_probe_host" {
  type = string
}

variable "health_probe_path" {
  type = string
}

variable "health_probe_protocol" {
  type = string
}

variable "tags" {
    type = map(string)
    default = {}
}