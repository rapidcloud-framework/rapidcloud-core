variable "prefix" {}
variable "account_id" {}
variable "region" {}

variable "block_public_acls" {
  default = true
}

variable "block_public_policy" {
  default = true
}

variable "ignore_public_acls" {
  default = true
}

variable "restrict_public_buckets" {
  default = true
}

variable "tags" {
  description = "Map of tags to assign to this bucket"
  type        = map
}

variable "additional_buckets" {
  type        = list
  description = "A list of additional buckets this role has access to OTHER then the base s3 buckets"
  default     = []
}

variable "arn_prefix" {
  description = "arn prefixes"
  default = {
    us-east-1      = "arn:aws"
    us-east-2      = "arn:aws"
    us-west-1      = "arn:aws"
    us-west-2      = "arn:aws"
    ca-central-1   = "arn:aws"
    eu-west-1      = "arn:aws"
    eu-central-1   = "arn:aws"
    eu-west-2      = "arn:aws"
    ap-northeast-1 = "arn:aws"
    ap-northeast-2 = "arn:aws"
    ap-southeast-1 = "arn:aws"
    ap-southeast-2 = "arn:aws"
    ap-south-1     = "arn:aws"
    sa-east-1      = "arn:aws"
    us-gov-east-1  = "arn:aws-us-gov"
    us-gov-west-1  = "arn:aws-us-gov"
  }
}
