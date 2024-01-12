data "aws_kms_alias" "env" {
  name = "alias/${var.profile}"
}

resource "aws_cloudwatch_log_group" "fluentbit" {
  count             = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  name              = "/aws/eks/${var.cluster_name}/logs"
  retention_in_days = var.fluentbit_log_retention_in_days
  tags              = merge(local.rc_tags, var.tags)
}

data "aws_iam_policy_document" "fluentbit_sts" {
  count = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.eks_oidc_provider.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(var.eks_oidc_provider.url, "https://", "")}:sub"
      values = [
        "system:serviceaccount:kube-system:fluent-bit"
      ]
    }
  }
}

resource "aws_iam_role" "fluentbit" {
  count              = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  assume_role_policy = data.aws_iam_policy_document.fluentbit_sts[0].json
  name               = "${var.cluster_name}-fluent-bit"
  tags               = merge(local.rc_tags, var.tags)
}

resource "aws_iam_policy" "fluentbit" {
  count  = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  name   = "${var.cluster_name}-fluent-bit"
  policy = data.aws_iam_policy_document.fluentbit[0].json
  tags   = merge(local.rc_tags, var.tags)
}

resource "aws_iam_role_policy_attachment" "fluentbit" {
  count      = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  role       = aws_iam_role.fluentbit[0].id
  policy_arn = aws_iam_policy.fluentbit[0].arn
}

data "aws_iam_policy_document" "fluentbit" {
  count = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  statement {
    effect    = "Allow"
    resources = ["arn:aws:logs:${var.region}:${var.account}:*:*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "cloudwatch:PutMetricData",
      "logs:PutLogEvents",
      "logs:PutRetentionPolicy",
      "ec2:DescribeVolumes",
      "ec2:DescribeTags",
    ]
  }
}


resource "helm_release" "fluentbit" {
  count      = tobool(var.install_fluentbit_cloudwatch) ? 1 : 0
  name       = "fluent-bit"
  namespace  = "kube-system"
  chart      = "aws-for-fluent-bit"
  repository = "https://aws.github.io/eks-charts"
  values = [templatefile("${path.module}/fluentbit.yaml",
    {
      cluster_name                    = var.cluster_name
      fluentbit_log_retention_in_days = var.fluentbit_log_retention_in_days
      region                          = var.region
      role                            = aws_iam_role.fluentbit[0].arn
  })]
}
