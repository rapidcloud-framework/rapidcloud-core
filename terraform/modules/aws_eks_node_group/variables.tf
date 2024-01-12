# generic 
variable "env" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

# eks nodes
variable "node_group_name" {}
variable "cluster_name" {}
variable "eks_version" {}
variable "subnet_ids" {}
variable "instance_types" { default = "t3.medium,t3a.medium" }
variable "capacity_type" { default = "ON_DEMAND" }
variable "volume_size" { default = "10" }
variable "volume_type" { default = "gp3" }
variable "force_update_version" { default = false }
variable "ssh_key" { default = "" }
variable "tags" { default = {} }
variable "labels" { default = {} }
variable "desired_size" { default = 2 }
variable "max_size" { default = 5 }
variable "min_size" { default = 0 }
