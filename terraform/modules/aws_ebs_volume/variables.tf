variable "disk_size" {
    type    = string
    default = 8
}
variable "availability_zone"{
    type = string
    default = "us-east-1a"
}
variable "tags" {
    type    = map
    default = {
        default_tag_one = "default_value_tag_one",
        default_tag_two = "default_value_tag_two"
    }
}