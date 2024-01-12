variable "path_part" {
  type = string
}

variable "rest_api_id" {
  type = string
}

variable "parent_resource_id" {
  type = string
}

variable "lambda_integrations" {
  type = list(object({ http_method = string, lambda_name = string }))
}

variable "region" {
  type = string
}
