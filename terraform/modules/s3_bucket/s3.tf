resource "aws_s3_bucket" "s3" {
  bucket = var.bucket_name
  tags = merge(var.tags, tomap({"Name" = var.bucket_name}))
}

resource "aws_s3_bucket_server_side_encryption_configuration" "s3_server_side_ecryption_configuration" {
  bucket = aws_s3_bucket.s3.id
  rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }    
  }
  
}

resource "aws_s3_bucket_acl" "s3_bucket_acl" {
  bucket = aws_s3_bucket.s3.id
  acl = "private"
  depends_on = [aws_s3_bucket_ownership_controls.ownershipcontrols_s3]
  
}
resource "aws_s3_bucket_ownership_controls" "ownershipcontrols_s3" {
  bucket = aws_s3_bucket.s3.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "s3_public_access" {
  bucket = aws_s3_bucket.s3.id

  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}
