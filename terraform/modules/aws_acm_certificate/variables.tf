variable "acm_cert_domain_name" {
    type = string
    default = "example.com"
}
variable "acm_cert_validation_method" {
    type = string
    default = "DNS"
}
variable "r53_zone_name" {
    type = string
    description = "Name of and existing zone in route 53"
}
variable "tags" {
    type    = map
    default = {
        default_tag_one = "default_value_tag_one",
        default_tag_two = "default_value_tag_two"
    }
}