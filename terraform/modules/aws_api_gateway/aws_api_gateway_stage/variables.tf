variable "rest_api_id" {
    type = string
}

variable "stage_name" {
    type    = string
    default = "dev"
}

variable "triggers" {
    type    = list
    default = []
}