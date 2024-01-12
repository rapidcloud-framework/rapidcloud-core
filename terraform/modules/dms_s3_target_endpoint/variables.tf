#####################################
# Required Variables
#####################################

variable "endpoint_id" {
  description = "The database endpoint identifier"
  type        = string
}

variable "s3_bucket_folder" {
  description = "Where the files are created in the s3 bucket"
  type        = string
  default     = ""
}

variable "s3_bucket_name" {
  description = "The Bucket Name"
  type        = string
  default     = ""
}
variable "s3_bucket_arn" {
  description = "The Bucket Arn"
  type        = string
  default     = ""
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
  type        = map(string)
  default     = {}
}

variable "s3_external_table_definition" {
  description = ""
  type        = string
  default     = ""
}

variable "s3_csv_row_delimeter" {
  description = "CSV row delimeter"
  type        = string
  default     = "\\n"
}

variable "s3_csv_delimiter" {
  description = "The CSV field Delimeter"
  type        = string
  default     = ","
}

variable "s3_compression_type" {
  description = "An optional parameter when set to GZIP uses GZIP to compress the target .csv or .parquet files"
  type        = string
  default     = "NONE"
}
