# generic 
variable "env" {}
variable "profile" {}
variable "workload" {}
variable "fqn" {}
variable "cmd_id" { default = "" }

# eks cluster
variable "cluster_name" {}
variable "eks_oidc_provider" {}
variable "compute_type" {}
variable "eks_version" {}
variable "subnet_ids" {}
variable "tags" { default = {} }

# eks cluster addons (aws native)
variable "enable_aws_kube_proxy" { default = "true" }
variable "aws_kube_proxy_version" { default = "latest" }

variable "enable_aws_coredns" { default = "true" }
variable "aws_coredns_version" { default = "latest" }
variable "aws_coredns_replica_count" { default = 2 }

variable "enable_aws_vpc_cni" { default = "true" }
variable "aws_vpc_cni_version" { default = "latest" }

variable "enable_aws_ebs_csi" { default = "true" }
variable "aws_ebs_csi_version" { default = "latest" }

