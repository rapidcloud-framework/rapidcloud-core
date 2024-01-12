variable "cluster_name" {
  description = "cluster name, will be used to tag all resources"
}

variable "kafka_version" {
  description = "the cluster kafka version"
  default     = "2.2.1"
}

variable "encryption_in_transit" {
  description = "encryption setting for data in transit between clients and brokers TLS|TLS_PLAINTEXT|PLAINTEXT"
  default     = "TLS"
}

variable "number_of_broker_nodes" {
  description = "number of broker nodes PER az"
  default     = 1
}

variable "instance_type" {
  description = "cluster broker size"
  default     = "kafka.t3.small"
}

variable "volume_size" {
  description = "the broker volume size"
  default     = 10
}

variable "log_retention_in_days" {
  description = "log retention preiod for cloudwatch logs"
  default     = 7
}

variable "server_properties" {
  description = "map of server properties"
  type        = string
  default     = ""
}

variable "kms_key_id" {
  description = "kms key used for data at rest"
}

variable "broker_subnets" {
  description = "private vpc subnets the cluster will reside on"
  type        = list(any)
}

variable "vpc_id" {
  description = "vpc the cluster will reside on"
}

variable "allowed_cidrs" {
  description = "cidrs listed here will be allowed access to ports 2181,9092,9094"
  type        = list(any)
  default     = []
}

variable "allowed_sgs" {
  description = "security group ids listed here will be allowed access to ports 2181,9092,9094"
  type        = list(any)
  default     = []
}

variable "enhanced_monitoring" {
  description = "PER_TOPIC_PER_PARTITION|PER_TOPIC_PER_BROKER|PER_BROKER|DEFAULT"
  default     = "DEFAULT"
}

variable "tags" {
  description = "Map of tags to assign to this bucket"
  type        = map(any)
  default     = {}
}

# monitoring
# variable "jmx_exporter" { default = true }
# variable "node_exporter" { default = true }

