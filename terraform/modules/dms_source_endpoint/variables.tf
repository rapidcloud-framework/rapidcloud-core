#####################################
# Required Variables
#####################################

variable "endpoint_id" {
  description = "The database endpoint identifier"
  type        = string
}

variable "engine_name" {
  description = "The type of engine for the endpoint. Can be one of aurora | azuredb | docdb | dynamodb | mariadb | mongodb | mysql | oracle | postgres | redshift | s3 | sqlserver | sybase."
  type        = string
}

variable "username" {
  description = "The user name to be used to login to the endpoint database."
  type        = string
}

variable "password" {
  description = "The password to be used to login to the endpoint database."
  type        = string
}

variable "server_name" {
  description = "The server name to connect to"
  type        = string
}

variable "database_name" {
  description = "The database to connect to"
  type        = string
}

variable "port" {
  description = "The database server port to connect to"
  type        = string
}

###################################/
# Optional Variables
#####################################
variable "certificate_arn" {
  description = " The Amazon Resource Name (ARN) for the certificate."
  type        = string
  default     = ""
}

variable "kms_key_arn" {
  description = "The Amazon Resource Name (ARN) for the KMS key that will be used to encrypt the connection parameters"
  type        = string
  default     = ""
}

variable "extra_connection_attributes" {
  description = "Additional attributes associated with the connection"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags ..."
  type        = map
  default     = {}
}

variable "s3_csv_row_delimeter" {
  description = "CSV row delimeter"
  type        = string
  default     = "\n"
}

variable "s3_csv_delimiter" {
  description = "The CSV field Delimeter"
  type        = string
  default     = ","
}

variable "s3_compression_type" {
  description = "An optional parameter when set to GZIP uses GZIP to compress the target .csv or .parquet files"
  type        = string
  default     = "none"
}

variable "ssl_mode" {
  description = "(Optional, Default: none) The SSL mode to use for the connection. Can be one of none | require | verify-ca | verify-full"
  type        = string
  default     = "none"
}
