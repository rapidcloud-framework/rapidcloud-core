
# generic 
variable "env" {}
variable "account" {}
variable "region" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

# eks cluster
variable "cluster_name" {}
variable "eks_oidc_provider" {}
variable "file_system_id" {}
# variable "eks_version" {}
# variable "subnet_ids" {}
# variable "tags" { default = {} }
