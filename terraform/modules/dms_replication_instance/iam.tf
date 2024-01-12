resource "aws_iam_role" "dms_cloudwatch_logs_role" {
  count = var.create_dms_iam_roles ? 1 : 0
  name  = "dms-cloudwatch-logs-role"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "dms.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      },
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "redshift.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "dms_cloudwatch_logs_policy" {
  count      = var.create_dms_iam_roles ? 1 : 0
  role       = aws_iam_role.dms_cloudwatch_logs_role[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonDMSCloudWatchLogsRole"
  depends_on = [aws_iam_role.dms_cloudwatch_logs_role]
}

resource "aws_iam_role" "dms_vpc_role" {
  count = var.create_dms_iam_roles ? 1 : 0
  name  = "dms-vpc-role"

  assume_role_policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
   {
     "Effect": "Allow",
     "Principal": {
        "Service": "dms.amazonaws.com"
     },
   "Action": "sts:AssumeRole"
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "dms_vpc_management_policy" {
  count      = var.create_dms_iam_roles ? 1 : 0
  role       = aws_iam_role.dms_vpc_role[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole"
  depends_on = [aws_iam_role.dms_vpc_role]
}
