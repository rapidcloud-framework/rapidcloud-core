resource "aws_cloudfront_distribution" "distribution" {
  web_acl_id = var.web_acl_id
  default_cache_behavior {
    allowed_methods        = var.cf_distro_allowed_methods
    cached_methods         = var.cf_distro_cached_methods
    target_origin_id       = var.origin_id
    viewer_protocol_policy = var.cf_distro_viwer_protocol_policy
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }
  enabled = true

  origin {
    domain_name = var.bucket_regional_domain_name
    origin_id   = var.origin_id

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }
  restrictions {
    geo_restriction {
      restriction_type = var.cf_distro_restriction_type
      locations        = var.cf_distro_geo_restriction_locations_list
    }
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  tags = var.tags
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = var.cf_oai_comment
}