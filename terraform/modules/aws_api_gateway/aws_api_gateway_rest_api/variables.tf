variable "name" {
    type = string
}

variable "disable_execute_api_endpoint" {
    type    = bool
    default = false
}

variable "endpoint_type" {
    type    = string
    default = "REGIONAL"
}

variable "tags" {
    type    = map
    default = {}
}
