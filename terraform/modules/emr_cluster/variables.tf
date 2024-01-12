variable "vpc_id" {
  description = "The VPC ID where this cluster will reside"
}

variable "region" {
  description = "The VPC ID where this cluster will reside"
}

variable "subnet_id" {
  description = "The subnet where the cluster nodes will reside"
}

variable "cluster_name" {
  description = "The cluster name, will be used to tag/name resources"
}

variable "access_type" {
  description = "Set to public to allow non vpc access"
  default     = "private"
}

variable "ssh_pub_key" {
  description = "The rsa pub key used to ssh into cluster nodes, needs to be generate via ssh-keygen -t rsa"
  default     = ""
}

variable "release_label" {
  description = "The release label for the Amazon EMR release "
  default     = "emr-5.26.0"
}

variable "applications" {
  description = "A list of applications for the cluster. Valid values are: Flink, Hadoop, Hive, Mahout, Pig, Spark, and JupyterHub (as of EMR 5.14.0). Case insensitive"
  type        = list
  # default     = ["Hadoop", "Hive", "Pig"]
  default = ["Hadoop"]
}

variable "configuration_json_file_name" {
  description = "A json file containing extra configuration for the cluster"
  default     = "none.json"
}

variable "tags" {
  description = "Map of tags to assign to this bucket"
  type        = map
}

##############################################
# instance group configutation options
##############################################
variable "master_instance_size" {
  description = "The instance size used for master nodes"
  default     = "m5.xlarge"
}

variable "master_instance_count" {
  description = "The number of master nodes to build, can be 1 or 3 only"
  default     = 1
}

variable "core_instance_size" {
  description = "The instance size used for core nodes"
}

variable "core_instance_count" {
  description = "The number of core nodes to build"
}

variable "core_instance_bid_price" {
  description = "Optional, if specificed will use spot instances"
  default     = ""
}

##############################################
# security group extra rules
##############################################

variable "master_cidr_ingress_rules" {
  description = "A list of INGRESS cidr's to add to the masters security group"
  type        = list
  default     = []
}

variable "master_sg_ingress_rules" {
  description = "A list of INGRESS sg's to add to the masters security group"
  type        = list
  default     = []
}

variable "core_cidr_ingress_rules" {
  description = "A list of INGRESS cidr's to add to the slaves security group"
  type        = list
  default     = []
}

variable "core_sg_ingress_rules" {
  description = "A list of INGRESS sg's to add to the slaves security group"
  type        = list
  default     = []
}
