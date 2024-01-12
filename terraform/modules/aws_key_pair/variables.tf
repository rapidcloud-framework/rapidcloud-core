variable "key_name" {
    type = string
    default = "default_key_name"
}
variable "public_key" {
    type = string
    default = ""
}
variable "tags" {
  type = map
  default = {
    "author"    = "rapid-cloud"
  }
}