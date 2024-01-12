variable "bucket_name" {
  default = "default-bucket-name"
}
variable "bucket_regional_domain_name" {
  default = "default-bucket-name.s3.us-east-1.amazonaws.com"
}
variable "origin_id" {
  default = "default-origin-id"
}
variable "tags" {
  default = {
    environment = "sandbox"
  }
}
variable "cf_distro_allowed_methods" {
  default = ["GET", "HEAD"]
  type    = list(any)
}
variable "cf_distro_cached_methods" {
  default = ["GET", "HEAD"]
  type    = list(any)
}
variable "cf_distro_viwer_protocol_policy" {
  default = "allow-all"
}
variable "cf_oai_comment" {
  default = "Rapid-Cloud rocks!"
}

variable "cf_distro_geo_restriction_locations_list" {
  default = ["US"]
  type    = list(any)
}
variable "cf_distro_restriction_type" {
  default = "whitelist"
  type    = string
}
variable "web_acl_id" {
  default = null
  type    = string
}