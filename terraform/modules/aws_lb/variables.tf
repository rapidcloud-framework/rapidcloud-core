variable "name" {
    type    = string
    default = "lb-default-name"
}
variable "is_internal" {
    type    = bool
    default = true
}
variable "type"{
    type    = string
    default = "application"
}
variable "subnets"{
    type    = list
    default = ["subnet-f6ed56bb", "subnet-89399b87"]
}
variable "security_group_ids" {
  type    = list
  default = []
}
variable "default_tags" {
    type    = map
    default = {
        default_tag_one = "default_value_tag_one",
        default_tag_two = "default_value_tag_two"
    }
}