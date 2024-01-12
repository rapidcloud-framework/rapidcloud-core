resource "aws_instance" "instance" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  availability_zone      = var.availability_zone
  tags                   = var.tags
  key_name               = var.key_name
  user_data              = var.user_data
  vpc_security_group_ids = var.vpc_security_group_ids
  subnet_id              = var.subnet_id
  iam_instance_profile   = var.iam_instance_profile

  lifecycle {
    ignore_changes = [user_data]
  }

}