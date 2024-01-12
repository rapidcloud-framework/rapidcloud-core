variable "encrypted" {
    type    = bool
    default = true 
}
variable "tags" {
    type    = map
    default = {
        default_tag_one = "default_value_tag_one",
        default_tag_two = "default_value_tag_two"
    }
}