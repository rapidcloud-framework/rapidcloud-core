variable "ad_service_name" {
    type = string
    default = "kinect-consulting.com"
    description = "The directory name must be between 2 and 64 characters, and can only contain alphanumeric characters, periods (.). or minus signs (-). Also, the directory name must begin and end with an alphanumeric character."
}
variable "ad_admin_password" {
    type = string
    default = "@Th1$1$4Te$TPa$$"
}
variable "ad_size" {
    type = string
    default = "Small"
    description = "Small or Large are accepted values"
}
variable "vpc_id" {
    type = string
    default = "vpc-05b3ddb6314da834c"
}
variable "subnet_ids" {
    type = list
    default = ["subnet-0c3afc2ff96a4fd14", "subnet-0f9adfd0b166faeaa"]
}
variable "storage_capacity" {
    type = number
    default = "300"
}
variable "throughput_capacity" {
    type = number
    default = "1024"
}
variable "deployment_type" {
    type = string
    default = "MULTI_AZ_1"
    description = "Values can be MULTI_AZ_1, SINGLE_AZ_1 OR SINGLE_AZ_2"
}
variable "preferred_subnet_id" {
    type = string
    default = "subnet-0c3afc2ff96a4fd14"
}
variable "subnets_availability_zone" {
    type = list
    default = ["us-east-1a","us-east-1b"]
}
variable "ad_type" {
    type = string
    default = "MicrosoftAD"
    description = "Accepted values are SimpleAD, ADConnector or MicrosoftAD"
}
variable "tags" {
    type    = map
    default = {
        default_tag_one = "default_value_tag_one",
        default_tag_two = "default_value_tag_two"
    }
}