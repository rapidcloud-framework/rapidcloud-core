variable "env" {
  default = ""
}

variable "cluster_identifier" {
  description = "The cluster name"
}

variable "cluster_instance_count" {
  default = 1
}

variable "monitoring_interval" {
  default = 0
}
variable "deletion_protection" {
  default = false
}

variable "vpc_id" {
}

variable "db_subnets" {
  type = list(any)
}

variable "cluster_instance_size" {
  default = "db.t2.micro"
}

variable "engine" {
  default = "aurora-mysql"
}

variable "param_group_family" {
  description = "The family used for creating the RDS paramter group"
  default     = "aurora-mysql5.7"
}

variable "engine_version" {
  default = "5.7.22"
}

variable "database_name" {
  default = "test"
}

variable "master_username" {
}

variable "master_password" {
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

variable "server_audit_events" {
  default = "CONNECT,QUERY,QUERY_DCL,QUERY_DDL,QUERY_DML"
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

variable "port" {
  default = 3306
}
