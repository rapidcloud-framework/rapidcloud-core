# generic 
variable "env" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

# eks cluster
variable "cluster_name" {}
variable "subnet_ids" { default = "" }
variable "cluster_log_types" { default = "api,audit,authenticator,controllerManager,scheduler" }
variable "cluster_log_retention_period" { default = 7 }
variable "endpoint_public_access" { default = "false" }
variable "endpoint_public_access_cidrs" { default = "" }
variable "eks_version" { default = "1.25" }
variable "tags" { default = {} }
