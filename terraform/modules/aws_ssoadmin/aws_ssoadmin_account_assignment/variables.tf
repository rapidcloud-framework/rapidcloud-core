variable "permission_set_arn" {
    type = string
}

variable "principal_type" {
    type        = string
    description = "USER | GROUP"
}

variable "principal_ids" {
    type    = list(string)
    default = []
}

variable "account_id" {
    type = string
}