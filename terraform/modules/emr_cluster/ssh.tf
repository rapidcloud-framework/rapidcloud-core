resource "aws_key_pair" "emr" {
  key_name   = "${var.cluster_name}-key"
  public_key = var.ssh_pub_key
}
