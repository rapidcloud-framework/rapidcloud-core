resource "aws_placement_group" "placement_group" {
  name      = var.placement_group_name
  strategy  = var.placement_group_strategy
}

resource "aws_launch_template" "launch_template" {
  name_prefix   = var.launch_template_name
  image_id      = var.ami_id
  instance_type = var.instance_type
}

resource "aws_autoscaling_group" "auto_scaling_group" {
  vpc_zone_identifier = var.subnets_ids
  desired_capacity    = var.desired_capacity
  max_size            = var.max_size
  min_size            = var.min_size
  placement_group     = aws_placement_group.placement_group.id
  force_delete        = true

  launch_template {
    id      = aws_launch_template.launch_template.id
    version = var.launch_template_version
  }
}