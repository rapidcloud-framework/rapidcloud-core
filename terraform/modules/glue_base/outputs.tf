output "arn" {
  value = aws_iam_role.role.arn
}

output "glue_temporary_bucket_arn" {
  value = aws_s3_bucket.glue_temporary.arn
}

output "glue_temporary_bucket_name" {
  value = aws_s3_bucket.glue_temporary.id
}

output "glue_scripts_bucket_arn" {
  value = aws_s3_bucket.glue_scripts.arn
}

output "glue_scripts_bucket_name" {
  value = aws_s3_bucket.glue_scripts.id
}

