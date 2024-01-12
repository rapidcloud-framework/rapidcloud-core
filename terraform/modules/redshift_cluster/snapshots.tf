# resource "aws_redshift_snapshot_schedule" "default" {
#     identifier = "tf-redshift-snapshot-schedule"
#     definitions = [
#         "rate(12 hours)",
#     ]
# }

# resource "aws_redshift_snapshot_schedule_association" "default" {
#       cluster_identifier  = "${aws_redshift_cluster.default.id}"
#     schedule_identifier = "${aws_redshift_snapshot_schedule.default.id}"
# }
