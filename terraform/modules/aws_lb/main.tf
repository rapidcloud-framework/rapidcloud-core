resource "aws_lb" "lb" {
    name                = var.name
    internal            = var.is_internal
    load_balancer_type  = var.type
    subnets             = var.subnets
    security_groups     = var.security_group_ids
    tags                = var.default_tags   
}

##add security group