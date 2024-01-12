# generic 
variable "env" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

# eks cluster
variable "cluster_name" {}
variable "eks_oidc_provider" {}
variable "map_roles" {}
variable "map_users" {}
variable "node_group_roles" { default = [] }
variable "fargate_profile_roles" { default = [] }
