variable "load_balancer_arn" {
    type = string
}

variable "protocol" {
    type = string
}

variable "alpn_policy" {
    type    = string #valid if protocol is tls
    default = null
}

variable "ssl_policy" {
    type = string
    default = null #required if protocol is https/tls
}

variable "certificate_arn" {
    type = string
    default = null #valid if protocol is https
}

variable "port" {
    type = number
}

variable "target_group_arn" {
    type = string
}

variable "tags" {
    type = map
    default = {}
}