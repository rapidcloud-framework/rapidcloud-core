resource "aws_s3_bucket" "emr_cluster_logs" {
  bucket = "${var.cluster_name}-emr-logs"
  # region = var.region
  tags   = merge(var.tags, tomap({"Name" = "${var.cluster_name}-logs"}))
}
