variable "name" {
  type = string
}

variable "email" {
    type = string
}

variable "tags" {
    type    = map
    default = {}
}

variable "parent_id" {
  type        = string
  description = "ID of parent OU or root org"
}

variable "scps" {
  type    = list
  default = []
}