resource "aws_lb_listener" "l" {
    load_balancer_arn = var.load_balancer_arn
    protocol          = var.protocol
    alpn_policy       = var.alpn_policy
    ssl_policy        = var.ssl_policy
    certificate_arn   = var.certificate_arn
    port              = var.port

    default_action {
        type = "forward"
        forward {
            target_group {
                arn = var.target_group_arn
            }
        }
    }

    tags = var.tags
}