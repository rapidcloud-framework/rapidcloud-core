resource "aws_ecr_repository" "repo" {
    name                 = var.name
    image_tag_mutability = var.image_tag_mutability

    image_scanning_configuration {
        scan_on_push = var.scan_on_push
    }

    encryption_configuration {
        encryption_type = var.encryption_type
        kms_key         = lower(var.encryption_type) == "kms" ? var.kms_key : null
    }

    tags = var.tags
}