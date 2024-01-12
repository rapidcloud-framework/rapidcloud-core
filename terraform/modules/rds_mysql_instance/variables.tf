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
  default = "mysql"
}

variable "engine_version" {
  default = "5.7.22"
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
  default = ["audit", "error", "general", "slowquery"]
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
  default = 3306
}

variable "sg_enable_self" {
  default = false
}

variable "param_group_family" {
  default = "mysql5.7"
}

