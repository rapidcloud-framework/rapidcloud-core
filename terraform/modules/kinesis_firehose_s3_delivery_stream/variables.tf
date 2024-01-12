variable "name" {
  description = "The name used for all the resources"
}

variable "destination_bucket_arn" {
  description = "The destination bucket"
}

variable "kinesis_stream_arn" {
  description = "The source kinesis stream"
  default     = ""
}

variable "region" {}
variable "account_id" {}

variable "s3_prefix" {
  description = "Optional s3 prefix"
  default     = ""
}

variable "s3_error_event_prefix" {
  description = "Optional s3 error prefix"
  default     = "errors"
}

variable "buffer_size" {
  default = 5
}

variable "buffer_interval" {
  default = 300
}

variable "compression_format" {
  default = "UNCOMPRESSED"
}
