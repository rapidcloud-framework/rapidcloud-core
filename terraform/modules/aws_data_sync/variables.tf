variable "ip_address" {
  type        = string
  description = "(Required) DataSync Agent IP address to retrieve activation key during resource creation. Conflicts with activation_key. DataSync Agent must be accessible on port 80 from where Terraform is running."
  default     = "3.214.144.151"
}
variable "agent_name" {
  type        = string
  description = "(Required) Name of the DataSync Agent."
  default     = "default_agent_name_002"
}
variable "server_hostname" {
  type        = string
  description = "(Required) Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server."
  default     = "ec2-3-214-144-151.compute-1.amazonaws.com"
}
variable "nfs_subdirectory" {
  type        = string
  description = "(Required) Subdirectory to perform actions as source or destination. Should be exported by the NFS server."
  default     = "/d/"
}
variable "s3_bucket_arn" {
  type        = string
  description = "(Required) Amazon Resource Name (ARN) of the S3 Bucket."
  default     = ""
}
variable "s3_subdirectory" {
  type        = string
  description = "(Required) Prefix to perform actions as source or destination."
  default     = ""
}
variable "bucket_access_role_arn" {
  type        = string
  description = "(Required) ARN of the IAM Role used to connect to the S3 Bucket."
  default     = ""
}
variable "vpc_id" {
  type        = string
  description = "(Required) The ID of the VPC in which the endpoint will be used."
  default     = ""
}
variable "security_group_ids" {
  type        = list(string)
  description = "(Required) The ID of one or more security groups to associate with the network interface."
  default     = [""]
}
variable "subnet_ids" {
  type        = list(string)
  description = "(Required) The ID of one or more subnets in which to create a network interface for the endpoint."
  default     = [""]
}
variable "security_groups_arns" {
  type        = list(string)
  description = "(Required) The ARNs of the security groups used to protect your data transfer task subnets."
  default     = [""]
}
variable "subnet_arns" {
  type        = list(string)
  description = "(Required) The Amazon Resource Names (ARNs) of the subnets in which DataSync will create elastic network interfaces for each data transfer task."
  default     = [""]
}
variable "s3_location_name" {
  type = string
  description = "Specify a name for the location"
  default = "s3_location_default_name"
}
variable "nfs_location_name" {
  type = string
  description = "Specify a name for the location"
  default = "nfs_location_default_name"
}
variable "tags" {
  type = map
  default = {
    "author"    = "rapid-cloud"
  }
}