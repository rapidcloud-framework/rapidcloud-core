variable "dst_loc_destination_arn" {
  default     = "arn:aws:datasync:us-east-1:247654790127:location/loc-0ad5ce2be3fe366f8"
  description = "value"
  type        = string
}
variable "ds_task_name" {
  default     = "dst_default_name"
  description = "value"
  type        = string
}
variable "dst_loc_source_arn" {
  default     = "arn:aws:datasync:us-east-1:247654790127:location/loc-0b71671213a3d41ab"
  description = "value"
  type        = string
}
variable "dst_exclude_filter_type" {
  default     = "SIMPLE_PATTERN"
  description = "value"
  type        = string
}
variable "dst_exclude_value" {
  default     = "/folder1|/folder2"
  description = "value"
  type        = string
}
variable "dst_include_filter_type" {
  default     = "SIMPLE_PATTERN"
  description = "value"
  type        = string
}
variable "dst_include_value" {
  default     = "/folder1|/folder2"
  description = "value"
  type        = string
}
variable "dst_schedule_expression" {
  default     = "cron(0 12 ? * SUN,WED *)"
  description = "value"
  type        = string
}
variable "tags" {
}