resource "aws_efs_file_system" "file_system" {
    encrypted                   = var.encrypted
    tags                        = var.tags
}