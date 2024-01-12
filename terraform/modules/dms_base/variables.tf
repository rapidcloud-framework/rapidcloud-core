######################################################
### Required Variables
######################################################
#variable "prefix" {
#  description = "prefix used to tag/name resources"
#  type        = string
#}

#variable "env" {
#  description = "Environment name"
#  type        = string
#}

#variable "create_dms_iam_roles" {
#  description = "Needed once per AWS account"
#  type        = bool
#  default     = false
#}

#variable "replication_instance_id" {
#  description = "The replication instance identifier"
#  type        = string
#}

#variable "vpc_id" {
#  description = "The VPC in which to create the DMS instance, subnet and security group"
#  type        = string
#}

#variable "replication_group_destination_subnets" {
#  description = "The VPC subnet used to create the replication subnet group"
#  type        = list(string)
#}

#variable "cidr_ingress_rules" {
#  description = "List of ingress rules, each rule should be from_port,to_port,protocol,cidr"
#  type        = map(string)
#  default     = {}
#}

#variable "cidr_egress_rules" {
#  description = "List of egress rules, each rule should be from_port,to_port,protocol,cidr"
#  type        = map(string)
#  default     = {}
#}

#variable "sg_ingress_rules" {
#  description = "List of ingress rules, each rule should be from_port,to_port,protocol,security_group"
#  type        = map(string)
#  default     = {}
#}

#variable "sg_egress_rules" {
#  description = "List of egress rules, each rule should be from_port,to_port,protocol,security_group"
#  type        = map(string)
#  default     = {}
#}


#variable "availability_zone" {
#  description = "The EC2 Availability Zone that the replication instance will be created in"
#  type        = string
#}

######################################################
## Optional Variables
######################################################

#variable "replication_subnet_group_ids" {
#  description = "A subnet group to associate with the replication instance"
#  type        = list(string)
#  default     = []
#}

#variable "allocated_storage" {
#  description = "The amount of storage (in gigabytes) to be initially allocated for the replication instance"
#  type        = number
#  default     = 50
#}

#variable "apply_immediately" {
#  description = "Indicates whether the changes should be applied immediately or during the next maintenance window."
#  type        = bool
#  default     = false
#}

#variable "auto_minor_version_upgrade" {
#  description = "Indicates that minor engine upgrades will be applied automatically to the replication instance during the maintenance window"
#  type        = bool
#  default     = false
#}

#variable "engine_version" {
#  description = "The engine version number of the replication instance"
#  type        = string
#  default     = "3.1.3"
#}

#variable "kms_key_arn" {
#  description = "The Amazon Resource Name (ARN) for the KMS key that will be used to encrypt the connection parameters"
#  type        = string
#  default     = ""
#}

#variable "multi_az" {
#  description = "Specifies if the replication instance is a multi-az deployment. You cannot set the availability_zone parameter if the multi_az parameter is set to true. "
#  type        = bool
#  default     = false
#}

#variable "preferred_maintenance_window" {
#  description = "The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC)"
#  type        = string
#  default     = "sun:10:30-sun:14:30"
#}

#variable "publicly_accessible" {
#  description = "A value of true represents an instance with a public IP address"
#  type        = bool
#  default     = false
#}

#variable "replication_instance_class" {
#  description = "The compute and memory capacity of the replication instance as specified by the replication instance class"
#  type        = string
#  default     = "dms.t2.micro"
#}

#variable "tags" {
#  type        = map(string)
#  default     = {}
#  description = "Map of tags to add to the resources"
#}

#variable "vpc_security_group_ids" {
#  description = "A list of VPC security group IDs to be used with the replication instance. The VPC security groups must work with the VPC containing the replication instance."
#  type        = list(string)
#  default     = []
#}
