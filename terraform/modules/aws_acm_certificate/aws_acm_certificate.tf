resource "aws_acm_certificate" "aws_acm_cert" {
  domain_name       = var.acm_cert_domain_name
  validation_method = var.acm_cert_validation_method
  lifecycle {
    create_before_destroy = true 
  }
  tags = var.tags
}

resource "aws_route53_record" "certificate_validation" {
    for_each = {
        for dvo in aws_acm_certificate.aws_acm_cert.domain_validation_options : dvo.domain_name => {
            name = dvo.resource_record_name
            record = dvo.resource_record_value
            type = dvo.resource_record_type
        }
    }
    allow_overwrite = true
    name            = each.value.name
    records         = [each.value.record]
    ttl             = 60
    type            = each.value.type
    zone_id         = data.aws_route53_zone.r53_zone.zone_id
}

resource "aws_acm_certificate_validation" "acm_cert_validation" {
  certificate_arn         = aws_acm_certificate.aws_acm_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.certificate_validation : record.fqdn]
}

data "aws_route53_zone" "r53_zone" {
    name = var.r53_zone_name
}
