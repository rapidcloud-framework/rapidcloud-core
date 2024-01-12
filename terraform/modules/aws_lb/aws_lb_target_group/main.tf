resource "aws_lb_target_group" "g" {
    name                          = var.name
    port                          = var.port
    protocol                      = var.protocol
    target_type                   = var.target_type
    vpc_id                        = var.vpc_id
    load_balancing_algorithm_type = var.load_balancing_algorithm_type
    preserve_client_ip            = var.preserve_client_ip
    ip_address_type               = var.ip_address_type
    protocol_version              = var.protocol_version
    tags                          = var.tags
}

resource "aws_lb_target_group_attachment" "a" {
    for_each         = { for _, v in var.targets:  v => v }
    target_group_arn = aws_lb_target_group.g.arn
    target_id        = each.value
}