variable "ami_id" {
  type    = string
  default = "ami-0022f774911c1d690" #Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
}
variable "instance_type" {
  type    = string
  default = "t2.micro"
}
variable "availability_zone" {
  type    = string
  default = "us-east-1a"
}
variable "tags" {
  type = map
  default = {
    default_tag_one = "default_value_tag_one",
    default_tag_two = "default_value_tag_two"
  }
}
variable "volume_size" {
  type    = number
  default = 0
}
variable "instance_key_name" {
  type        = string
  default     = "d_key_name"
  description = "The name of the key pair to be created to access the image"
}
variable "instance_public_key" {
  type    = string
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGZV/lPsmEYrF0kwpImxfLOtwq9yCR62Hu09chj1s5ipV8FkCRwXEhvC68watYf80qGI+ZGP6jAkXcTIksSBCz/JD4cbevqUqLtBGX/r3emF5U2Q/LUtaxGhiZ3CnBioDcQs0i0vuCHcWyYS+GmxOZfXoFogfHWERF6x/qNMqFKrmn8AfcvlInRrCCoWTs5Utz6H2F+Vf763UxqJ35HRRh1W3DAy69Fg1LixB9hbZw8F+WwTTZysqFVlxEepnj3ftMA417bHaHX+oE1F+xmHtGZUmD5kkdwxMK4Rv0Jeah7tQ/nsHb1h2xfyxlaWrVZh9RRanTdibL4sEmTQ4zd/xrsHIa+tyurwY/CxmrdXvgXuyxediMNTaIovYyjlygDtATSO/1zngtXlXLaHBjt0Lrb153mp38xtc7h+sKnLmv6uDmLYMSt/aeKuWps8Kevs95YBUDrjVr9bB+OwoG2iu46/lIxTt7PNJoubLIWdskxUENQKHXrrqCuolK0cFocO0= JoMartinez@WFS-C02GQ1NLQ05N"
}
variable "user_data" {
  type    = string
  default = ""
}
variable "vpc_security_group_ids" {
  type    = list
  default = []
}
variable "subnet_id" {
  type    = string
  default = ""
}
variable "iam_instance_profile" {
  type    = string
  default = ""
}
variable "key_name" {
  type    = string
  default = ""
}