output "master_sg" {
  value = "${aws_security_group.emr_master.id}"
}

output "core_sg" {
  value = "${aws_security_group.emr_core.id}"
}

output "service_role" {
  value = "${aws_iam_role.emr_service.arn}"
}

output "instance_profile" {
  value = "${aws_iam_instance_profile.emr_instance.arn}"
}
