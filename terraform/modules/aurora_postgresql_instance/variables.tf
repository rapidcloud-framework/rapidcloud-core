variable "cluster_identifier" {
  description = "The cluster name"
}

variable "engine_version" {
  description = "The engine version this cluster will use"
}

variable "cluster_instance_size" {
  description = "The RDS instance size"
}

variable "cluster_instance_count" {
  description = "The RDS instance count, use 2 for replication"
  default     = 1
}

variable "azs" {
  description = "A list of EC2 Availability Zones for the DB cluster storage where DB cluster instances can be created"
  type        = list(string)
}

variable "database_name" {
  description = "Name for an automatically created database on cluster creation"
}

variable "master_username" {
  description = "Username for the master DB user"
}

variable "master_password" {
  description = "Password for the master DB user"
}

variable "backup_retention_period" {
  description = "The days to retain backups"
  default     = 7
}

variable "deletion_protection" {
  description = "If the DB instance should have deletion protection enabled, set to true for prod"
  default     = false
}

variable "enabled_cloudwatch_logs_exports" {
  description = "List of log types to export to cloudwatch"
  type        = list(string)
  default     = ["audit", "error", "general", "slowquery"]
}

variable "kms_key_id" {
  description = "Kms key used for encription"
}

variable "param_group_family" {
  description = "The family used for creating the RDS paramter group"
}

variable "vpc_id" {
  description = "The ID of the VPC where the RDS cluster will be created"
}

variable "allowed_ips" {
  description = "A list of IPs or CIDR's which are allowed access to this instance"
  type        = list(string)
  default     = []
}

variable "allowed_sgs" {
  description = "A list of Security Groups which are allowed access to this instance"
  type        = list(string)
  default     = []
}

variable "subnet_ids" {
  description = "The subnets the RDS subnet group will use"
  type        = list(string)
  default     = []
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Map of tags to add to the resources"
}

variable "storage_encrypted" {
  description = "Specifies whether the DB cluster is encrypted"
  default     = true
}

variable "skip_final_snapshot" {
  description = "Determines whether a final DB snapshot is created before the DB cluster is deleted, set to false if you dont need one"
  default     = true
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

variable "monitoring_interval" {
  description = "The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance. To disable collecting Enhanced Monitoring metrics, specify 0. The default is 0. Valid Values: 0, 1, 5, 10, 15, 30, 60. "
  default     = 0
}

variable "port" {
  description = "(Optional) The port on which the DB accepts connections"
  default     = 5432
}

variable "db_logs_retention_in_days" {
  description = "How many days should cloudwatch logs be kept"
  default     = 90
}
