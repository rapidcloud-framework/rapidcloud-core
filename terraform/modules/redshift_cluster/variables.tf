variable "cluster_name" {
  description = "The Cluster Name"
}

variable "tags" {
  description = "A map of tags to attach to resources"
  type        = map(string)
}

variable "subnets" {
  description = "The subnets where the cluster will reside"
  type        = list(string)
}

variable "iam_roles" {
  description = "A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time."
  type        = list(string)
  default     = []
}

variable "vpc_id" {
  description = "The VPC where the cluster will reside"
  type        = string
}

variable "cluster_port" {
  description = "Redhsift Cluster Port"
  type        = number
  default     = 5439
}

variable "allowed_cidr" {
  description = "This CIDR is allowed ingress access to the Redshift port ( 5439 by default )"
  type        = list(string)
}

variable "parameters" {
  description = "A map containing a list of desired paramaters"
  type        = map(string)
  default     = {}
}

variable "database_name" {
  description = "The name of the first database to be created when the cluster is created. If you do not provide a name, Amazon Redshift will create a default database called dev"
  type        = string
  default     = "dev"
}

variable "master_username" {
  description = "(Required unless a snapshot_identifier is provided) Username for the master DB user"
  type        = string
  default     = ""
}

variable "master_password" {
  description = "(Required unless a snapshot_identifier is provided) Password for the master DB user, DO NOT USE PLAIN TEXT HERE"
  type        = string
  default     = ""
}

variable "node_count" {
  description = "The number of compute nodes in the cluster, setting this to more then the default 1 will create a multi-node cluste"
  type        = number
  default     = 1
}

variable "node_type" {
  description = "Size of the compute nodes, https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html"
  type        = string
  default     = "dc2.large"
}

variable "availability_zone" {
  description = "The EC2 Availability Zone (AZ) in which you want Amazon Redshift to provision the cluster"
  type        = string
  default     = ""
}

variable "preferred_maintenance_window" {
  description = "The weekly time range (in UTC) during which automated cluster maintenance can occur. Format: ddd:hh24:mi-ddd:hh24:mi"
  type        = string
  default     = "sat:10:00-sat:10:30"
}

variable "allow_version_upgrade" {
  description = "If true , major version upgrades can be applied during the maintenance window to the Amazon Redshift engine that is running on the cluster"
  type        = bool
  default     = true
}

variable "snapshot_identifier" {
  description = "The name of the snapshot from which to create the new cluster"
  type        = string
  default     = ""
}

variable "snapshot_cluster_identifier" {
  description = "The name of the cluster the source snapshot was created from"
  type        = string
  default     = ""
}

variable "final_snapshot_identifier" {
  description = "The name of the snapshot from which to create the new cluster"
  type        = string
  default     = ""
}

variable "skip_final_snapshot" {
  description = "Determines whether a final snapshot of the cluster is created before Amazon Redshift deletes the cluster, if true a snapshot will be created"
  type        = bool
  default     = true
}

variable "automated_snapshot_retention_period" {
  description = "The number of days that automated snapshots are retained. If the value is 0, automated snapshots are disabled"
  type        = number
  default     = 1
}

variable "encrypted" {
  description = "If true , the data in the cluster is encrypted at rest"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "The ARN for the KMS encryption key. When specifying kms_key_id, encrypted needs to be set to true"
  type        = string
}

variable "enable_logging" {
  description = "Enables logging"
  type        = bool
  default     = false
}

variable "sg_enable_self" {
  default = false
}
