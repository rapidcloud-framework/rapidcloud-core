# data "aws_s3_bucket" "destination_bucket" {
#   bucket = var.destination_bucket_name
# }

# data "aws_kinesis_stream" "stream" {
#   name = var.kinesis_stream_name
# }

resource "aws_kinesis_firehose_delivery_stream" "stream" {
  name        = var.name
  destination = "extended_s3"

  dynamic "kinesis_source_configuration" {
    for_each = compact([var.kinesis_stream_arn])
    content {
      role_arn           = aws_iam_role.firehose.arn
      kinesis_stream_arn = var.kinesis_stream_arn
    }
  }

  depends_on = [aws_iam_role.firehose]
  extended_s3_configuration {
    role_arn            = aws_iam_role.firehose.arn
    bucket_arn          = var.destination_bucket_arn
    error_output_prefix = var.s3_error_event_prefix
    prefix              = var.s3_prefix
    buffer_size         = var.buffer_size
    buffer_interval     = var.buffer_interval
    compression_format  = var.compression_format
  }
}
