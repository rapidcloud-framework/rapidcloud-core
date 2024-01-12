variable "waf_name" {
  type    = string
  default = "rc_default_waf_001"
}
variable "waf_scope" {
  type        = string
  default     = "REGIONAL"
  description = "Valid inputs are: REGIONAL"
}
variable "allow_requests_by_default" {
  type        = bool
  description = "Set to `true` for WAF to allow requests by default. Set to `false` for WAF to block requests by default."
  default     = false
}
variable "region" {
  type    = string
  default = "us-east-1"
}
variable "tags" {
  type    = map(any)
  default = {}
}
variable "associated_resources_list" {
  type        = list(string)
  description = "Resource Application ARN list"
  default = [
    ""
  ]
}