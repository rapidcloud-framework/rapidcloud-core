# generic 
variable "env" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

################################################################################
# Fargate Profile
################################################################################

variable "cluster_name" {}
variable "profile_name" {}
variable "subnet_ids" {}
variable "selectors" { default = [] }
variable "tags" { default = {} }
