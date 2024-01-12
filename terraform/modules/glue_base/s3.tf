resource "aws_s3_bucket" "glue_temporary" {
  bucket = "${var.prefix}-glue-temporary"

  tags = merge(var.tags, tomap({"Name" = "${var.prefix}-glue-temporary"}))
}
resource "aws_s3_bucket_acl" "s3bucket_glue_temporary_acl" {
  bucket = aws_s3_bucket.glue_temporary.id
  acl    = "private"
  depends_on = [aws_s3_bucket_ownership_controls.ownershipcontrols_glue_temporary]
}
resource "aws_s3_bucket_ownership_controls" "ownershipcontrols_glue_temporary" {
  bucket = aws_s3_bucket.glue_temporary.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "s3bucket_glue_temporary_server_side_configuration" {
  bucket = aws_s3_bucket.glue_temporary.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "glue_temporary_s3_public_access" {
  bucket                  = aws_s3_bucket.glue_temporary.id
  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}

resource "aws_s3_bucket" "glue_scripts" {
  bucket = "${var.prefix}-glue-scripts"

  tags = merge(var.tags, tomap({"Name" = "${var.prefix}-glue-scripts"}))
}
resource "aws_s3_bucket_ownership_controls" "ownershipcontrols_glue_scripts" {
  bucket = aws_s3_bucket.glue_scripts.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
resource "aws_s3_bucket_acl" "s3bucket_glue_scripts_acl" {
  bucket = aws_s3_bucket.glue_scripts.id
  acl    = "private"
  depends_on = [aws_s3_bucket_ownership_controls.ownershipcontrols_glue_scripts]
}
resource "aws_s3_bucket_server_side_encryption_configuration" "s3bucket_glue_scripts_server_side_configuration" {
  bucket = aws_s3_bucket.glue_scripts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "glue_scripts_s3_public_access" {
  bucket                  = aws_s3_bucket.glue_scripts.id
  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}
