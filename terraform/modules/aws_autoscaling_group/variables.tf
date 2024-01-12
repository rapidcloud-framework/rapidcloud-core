variable "launch_template_name"{
    type    = string
    default = "default_launch_template_name"
}
variable "launch_template_version" {
    type    = string
    default = "$Latest"
}
variable "ami_id" {
    type    = string
    default = "ami-0022f774911c1d690" #Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
}
variable "instance_type" {
    type    = string
    default = "t2.micro"
}
variable "subnets_ids" {
    type    = list
    default = ["subnet-0c3afc2ff96a4fd14", "subnet-0f9adfd0b166faeaa"]
}
variable "desired_capacity" {
    type    = number
    default = 2
}
variable "max_size" {
    type    = number
    default = 3
}
variable "min_size" {
    type    = number
    default = 2
}
variable "placement_group_name" {
    type    = string
    default = "default_placemente_group"
}
variable "placement_group_strategy" {
    type = string
    default = "spread"
}
variable "tags" {
    type    = map
    default = {
        default_tag_one = "default_value_tag_one",
        default_tag_two = "default_value_tag_two"
    }
}