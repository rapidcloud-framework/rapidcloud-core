variable "name" {
    type = string
}

variable "description" {
    type    = string
    default = null
}

variable "relay_state" {
    type        = string
    default     = null
    description = "The relay state URL used to redirect users within the application during the federation authentication process."
}

variable "session_duration" {
    type        = string
    default     = null
    description = "The length of time that the application user sessions are valid in the ISO-8601 standard. Default: PT1H"
}

variable "aws_managed_policy_arns" {
    type    = list(string)
    default = []
}

variable "customer_managed_policies" {
    type    = list(object({
        name = string
        path = string
    }))
    default = []
}

variable "inline_policy" {
    type    = string
    default = ""
}

variable "tags" {
    type    = map
    default = {}
}