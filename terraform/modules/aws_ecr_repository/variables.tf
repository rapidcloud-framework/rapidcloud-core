variable "name" {
    type = string
}

variable "image_tag_mutability" {
    type        = string
    default     = "MUTABLE"
    description = "IMMUTABLE | MUTABLE"
}

# deprecated in newer versions of aws provider
# use aws_ecr_registry_scanning_configuration instead
variable "scan_on_push" {
    type        = bool
    default     = false
    description = "indicates whether images are scanned after being pushed to the repository"
}

variable "encryption_type" {
    type        = string
    default     = "AES256"
    description = "AES256 | KMS"
}

variable "kms_key" {
    type        = string
    default     = null
    description = "The ARN of the KMS key to use when encryption_type is KMS. If not specified, uses the default AWS managed key for ECR."
}

variable "tags" {
    type    = map
    default = {}
}