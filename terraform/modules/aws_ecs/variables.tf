variable "region" {
  type    = string
  default = "us-east-1"
}

variable "name" {
  type = string
  default = "test"
}

variable "image_url" {
  type = string
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "enable_container_insights" {
  type    = bool
  default = false
}

variable "task_cpu_units" {
  type    = number
  default = 1024
}

variable "task_memory" {
  type        = number
  default     = 2048
  description = "Amount (in MiB) of memory used by the task"
}

variable "container_cpu_units" {
  type    = number
  default = 512
}

variable "container_memory" {
  type    = number
  default = 256
}

variable "container_environment_variables" {
  type = list(object({
    name  = string,
    value = string
  }))
  default = []
}

variable "open_ports" {
    type        = list
    default     = [80, 443]
}

variable "desired_count" {
    type        = number
    default     = 1
    description = "The number of instances of the task definition to place and keep running"
}

variable "task_role_arn" {
  type    = string
  default = null
}

variable "assign_public_ip" {
  type        = bool
  default     = false
  description = "Assign a public IP address to the ENI"
}

variable "subnet_ids" {
  type    = list
  default = []
}

variable "security_groups" {
  type    = list
  default = null
}

variable "tags" {
  type    = map
  default = {}
}
