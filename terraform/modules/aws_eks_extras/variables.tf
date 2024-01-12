
# generic 
variable "env" {}
variable "account" {}
variable "region" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

# eks cluster
variable "eks_oidc_provider" {}
variable "cluster_name" {}
variable "cluster_version" {}
variable "vpc_id" {}
variable "tags" { default = {} }

# extras
variable "install_efs_csi" {}
variable "file_system_id" {}

variable "install_metrics_server" {}
variable "install_cluster_autoscaler" {}
variable "install_ingress_alb" {}
variable "install_fluentbit_cloudwatch" {}
variable "fluentbit_log_retention_in_days" {}

