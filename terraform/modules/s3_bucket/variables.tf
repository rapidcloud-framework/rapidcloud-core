variable "bucket_name" {
  description = "The name of the s3 bucket to create"
  type        = string
}

variable "tags" {
  description = "Map of tags to assign to this bucket"
  type        = map(string)
}

variable "kms_key_arn" {
  description = "ARN of the kms key used to encrypt the bucket"
  type        = string
}

variable "enable_bucket_policy" {
  description = "Enable bucket policy"
  type        = bool
  default     = true
}

variable "block_public_acls" {
  type    = bool
  default = true
}

variable "block_public_policy" {
  type    = bool
  default = true
}

variable "ignore_public_acls" {
  type    = bool
  default = true
}

variable "restrict_public_buckets" {
  type    = bool
  default = true
}
