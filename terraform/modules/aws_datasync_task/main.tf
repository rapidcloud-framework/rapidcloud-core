resource "aws_datasync_task" "ds_task" {
  destination_location_arn = var.dst_loc_destination_arn
  name                     = var.ds_task_name
  source_location_arn      = var.dst_loc_source_arn
  tags = var.tags

  excludes {
    filter_type = var.dst_exclude_filter_type
    value       = var.dst_exclude_value
  }

  includes {
    filter_type = var.dst_include_filter_type
    value       = var.dst_include_value
  }
  schedule {
    schedule_expression = var.dst_schedule_expression
  }
}