resource "aws_emr_cluster" "emr_cluster" {
  name                              = "${var.cluster_name}-emr"
  release_label                     = var.release_label
  applications                      = var.applications
  service_role                      = aws_iam_role.emr_service.arn
  termination_protection            = false
  keep_job_flow_alive_when_no_steps = true

  ec2_attributes {
    key_name         = aws_key_pair.emr.key_name
    subnet_id        = var.subnet_id
    instance_profile = aws_iam_instance_profile.emr_instance.arn

    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_core.id
    service_access_security_group     = var.access_type == "private" ? aws_security_group.emr_service_access.0.id : ""
  }

  master_instance_group {
    instance_type  = var.master_instance_size
    instance_count = var.master_instance_count
    name           = "${var.cluster_name}-master-group"
  }

  core_instance_group {
    instance_type  = var.core_instance_size
    instance_count = var.core_instance_count
    bid_price      = var.core_instance_bid_price
    name           = "${var.cluster_name}-core-group"
  }

  # debugging
  step {
    action_on_failure = "TERMINATE_CLUSTER"
    name              = "Setup Hadoop Debugging"

    hadoop_jar_step {
      jar  = "command-runner.jar"
      args = ["state-pusher-script"]
    }
  }

  log_uri             = "s3n://${aws_s3_bucket.emr_cluster_logs.bucket}/logs/"
  tags                = merge(var.tags, tomap({"Name" = "${var.cluster_name}"}))
  configurations_json = file("${path.module}/configs/${var.configuration_json_file_name}")
  depends_on          = [aws_security_group.emr_master, aws_security_group.emr_core]
  lifecycle {
    ignore_changes = [step]
  }
}
