variable "name" {
  type = string
  description = "Name (domain) of the OpenSearch resource"
}

variable "instance_type" {
  type = string
  description = "Set the instance type (r5.large.search, etc.)"
  default     = "r5.large.search"
}

variable "autotune" {
  type = string
  description = "Set to `ENABLED` for OpenSearch to enable auto-tune, or `DISABLED` to disable."
  default     = "ENABLED"
}

variable "high_availability" {
  type        = bool
  description = "Set to `true` for OpenSearch to enable high-avilability."
  default     = true
}

variable "nodes" {
  type        = number
  description = "Set the total number of nodes (if high-availability is disabled, must be a multiple of 2)."
  default     = 2
}

variable "ebs_storage_size" {
  type        = number
  description = "Set the storage capacity (GiB) per node, minimum of 10 and maximum of 2048."
  default     = 10
}

variable "storage_capacity" {
  type        = number
  description = "Set the storage capacity (GiB), minimum of 32 and maximum of 65536."
  default     = 32
}

variable "iops" {
  type        = number
  description = "Set the total provisioned IOPs (MiB/s), minimum of 3000 and maximum of 16000."
  default     = 3000
}

variable "throughput" {
  type        = number
  description = "Set the total provisioned throughput (MiB/s), minimum of 8 and maximum of 2048; Throughput to IOPS ratio should not exceded 1:4."
  default     = 125
}

variable "subnet_ids" {
  type = list
  description = "Set the list of subnet IDs for the group."
  default     = []
}

variable "security_group_ids" {
  type = list
  description = "Set the list of security groups to associate."
  default     = []
}

variable "tags" {
  type    = map
  default = {}
}