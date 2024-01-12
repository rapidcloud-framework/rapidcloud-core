variable "display_name" {
    type = string
}

variable "description" {
    type    = string
    default = ""
}

variable "user_ids" {
    type    = list(string)
    default = []
}