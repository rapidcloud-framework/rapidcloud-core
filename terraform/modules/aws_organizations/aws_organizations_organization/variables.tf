variable "enabled_policy_types" {
  type        = list(string)
  description = "List of policy types enabled for root org"
  default     = [
    "SERVICE_CONTROL_POLICY",
    "TAG_POLICY"
  ]
}

variable "aws_service_access_principals" {
  type        = list(string)
  description = "List of service principals for root org"
  default     = [
    "sso.amazonaws.com",
    "access-analyzer.amazonaws.com",
    "aws-artifact-account-sync.amazonaws.com",
    "cloudtrail.amazonaws.com",
    "ram.amazonaws.com",
    "securityhub.amazonaws.com",
    "config.amazonaws.com"
  ]
}