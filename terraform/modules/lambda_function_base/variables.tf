variable "prefix" {
  description = "The prefix for this IAM role"
  type        = string
}

variable "account" {
  description = "The AWS account id"
  type        = string
}

variable "region" {
  description = "The AWS region"
  type        = string
}

variable "vpc_id" {
  description = "The AWS vpc where this sec group will be created"
  type        = string
}

variable "tags" {
  description = "Additional tags"
  type        = map
}

variable "cidr_ingress_rules" {
  description = "List of ingress rules, each rule should be from_port,to_port,protocol,cidr"
  type        = map(string)
  default     = {}
}

variable "cidr_egress_rules" {
  description = "List of egress rules, each rule should be from_port,to_port,protocol,cidr"
  type        = map(string)
  default     = {}
}

variable "sg_ingress_rules" {
  description = "List of ingress rules, each rule should be from_port,to_port,protocol,security_group"
  type        = map(string)
  default     = {}
}

variable "sg_egress_rules" {
  description = "List of egress rules, each rule should be from_port,to_port,protocol,security_group"
  type        = map(string)
  default     = {}
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
