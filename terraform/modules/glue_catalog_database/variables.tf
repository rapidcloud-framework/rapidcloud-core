#####################################
# required variables
####################################

variable "name" {
  description = "The catalog name"
}

variable "description" {
  description = "The catalog description"
  default     = "None"
}

variable "location_uri" {
  description = "The location of the database (for example, an HDFS path). "
  default     = ""
}
