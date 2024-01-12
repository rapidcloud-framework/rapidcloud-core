output "acm_cert_arn" {
    value = aws_acm_certificate.aws_acm_cert.arn
}
output "acm_cert_domain_name" {
    value = aws_acm_certificate.aws_acm_cert.domain_name
}
output "acm_cert_dvo" {
    value = aws_acm_certificate.aws_acm_cert.domain_validation_options
}