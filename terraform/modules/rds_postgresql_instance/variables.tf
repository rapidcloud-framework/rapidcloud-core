variable "instance_name" {
  description = "The db instance name"
}

variable "database_name" {
  description = "Database name"
  default     = "test"
}

variable "database_username" {
  description = "The DB username"
}

variable "database_password" {
  description = "The DB Password"
}

variable "monitoring_interval" {
  default = 15
}

variable "deletion_protection" {
  default = false
}

variable "vpc_id" {
}

variable "db_subnets" {
  type = list(any)
}

variable "multi_az" {
  default = false
}

variable "instance_class" {
  default = "db.t2.micro"
}

variable "engine" {
  default = "posgresql"
}

variable "engine_version" {
  default = "11.6-r1"
}

variable "allowed_ips" {
  type    = list(any)
  default = []
}

variable "allowed_sgs" {
  type    = list(any)
  default = []
}

variable "cloudwatch_logs_retention_in_days" {
  default = 30
}
variable "enabled_cloudwatch_logs_exports" {
  default = ["postgresql"]
}

variable "backup_retention_period" {
  default = 30
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Map of tags to add to the resources"
}

variable "parameters" {
  # example usage
  # parameters = [
  #   {
  #     name  = "enable_hashjoin"
  #     value = true
  #   },
  #   {
  #     name  = "enable_hashagg"
  #     value = true
  #   },
  # ]
  description = "A list of value to apply to the paramter group"

  type    = list(map(string))
  default = []
}

variable "allocated_storage" {
  default = ""
}

variable "max_allocated_storage" {
  default = ""
}

variable "storage_type" {
  default = "gp2"
}

variable "port" {
  default = 5432
}

variable "sg_enable_self" {
  default = false
}

variable "param_group_family" {
  default = "postgresql11"
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
