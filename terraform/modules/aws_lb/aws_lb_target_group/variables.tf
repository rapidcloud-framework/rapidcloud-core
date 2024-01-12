variable "name" {
    type = string
}

variable "port" {
    type  = number
}

variable "protocol" {
    type  = string
}

variable "target_type" {
    type = string #instance or ip
}

variable "vpc_id" {
    type = string
}

variable "load_balancing_algorithm_type" {
    type    = string
    default = null #only valid for alb
}

variable "preserve_client_ip" {
    type    = bool
    default = null #only valid for nlb
}

variable "ip_address_type" {
    type    = string
    default = null #only valid for ip target type
}

variable "protocol_version" {
    type    = string
    default = null #only valid for http/https protocol
}

variable "tags" {
    type = map
    default = {}
}

variable "targets" {
    type    = list(string)
    default = []
}