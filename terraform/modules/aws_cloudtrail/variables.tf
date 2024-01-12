variable "s3_bucket_name" {
  type = string
}

variable "name" {
  type = string
}

variable "kms_key_id" {
  type = string
}

variable "include_global_service_events" {
  type = bool
}

variable "enable_log_file_validation" {
  type = bool
}

variable "is_organization_trail" {
  type = bool
}

variable "is_multi_region_trail" {
  type = bool
}