data "aws_partition" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_iam_role" "eks_nodes" {
  name = "${local.node_group_name}EKSNodesRole"
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "ec2_container_registry_readonly" {
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_policy" "autoscaling" {
  name   = "${local.cluster_name}-${local.node_group_name}-autoscaling"
  policy = data.aws_iam_policy_document.autoscaling.json
}

resource "aws_iam_role_policy_attachment" "autoscaling" {
  role       = aws_iam_role.eks_nodes.id
  policy_arn = aws_iam_policy.autoscaling.arn
}

data "aws_iam_policy_document" "autoscaling" {
  statement {
    sid       = "Read"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:DescribeAutoScalingInstances",
      "autoscaling:DescribeLaunchConfigurations",
      "autoscaling:DescribeScalingActivities",
      "autoscaling:DescribeTags",
      "ec2:DescribeLaunchTemplateVersions",
      "ec2:DescribeInstanceTypes",
      "ec2:DescribeLaunchTemplateVersions",
      "ec2:DescribeImages",
      "ec2:GetInstanceTypesFromInstanceRequirements",
      "eks:DescribeNodegroup",
    ]
  }
  statement {
    sid    = "Write"
    effect = "Allow"

    actions = [
      "autoscaling:SetDesiredCapacity",
      "autoscaling:TerminateInstanceInAutoScalingGroup",
      "autoscaling:UpdateAutoScalingGroup",
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "autoscaling:ResourceTag/kubernetes.io/cluster/${var.cluster_name}"
      values   = ["owned"]
    }

    condition {
      test     = "StringEquals"
      variable = "autoscaling:ResourceTag/k8s.io/cluster-autoscaler/enabled"
      values   = ["true"]
    }
  }
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name         = local.cluster_name
  node_group_name      = local.node_group_name
  node_role_arn        = aws_iam_role.eks_nodes.arn
  version              = var.eks_version
  force_update_version = var.force_update_version == "true" ? true : false

  subnet_ids = local.subnet_ids

  capacity_type  = var.capacity_type
  instance_types = toset(split(",", var.instance_types))

  scaling_config {
    desired_size = var.desired_size
    max_size     = var.max_size
    min_size     = var.min_size
  }

  update_config {
    max_unavailable = 1
  }

  tags = merge(local.rc_tags,
    {
      "Name"                                 = "${local.cluster_name}-${var.node_group_name}",
      "k8s.io/cluster/${local.cluster_name}" = "owned",
      # "k8s.io/cluster-autoscaler/${local.cluster_name}" = "owned",
      "k8s.io/cluster-autoscaler/enabled" = true,
    },
  var.tags)
  labels = var.labels


  launch_template {
    name    = aws_launch_template.eks_nodes.name
    version = aws_launch_template.eks_nodes.latest_version
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.ec2_container_registry_readonly
  ]
}

resource "aws_launch_template" "eks_nodes" {
  name = local.node_group_name
  tag_specifications {
    resource_type = "instance"
    tags = merge(local.rc_tags,
      {
        "Name"                                 = "${local.cluster_name}-${var.node_group_name}",
        "k8s.io/cluster/${local.cluster_name}" = "owned",
        # "k8s.io/cluster-autoscaler/${local.cluster_name}" = "owned",
        "k8s.io/cluster-autoscaler/enabled" = true,
      },
    var.tags)
  }

  block_device_mappings {
    device_name = "/dev/xvdb"

    ebs {
      volume_size = var.volume_size
      volume_type = var.volume_type
    }
  }
}
