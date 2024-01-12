data "aws_eks_addon_version" "ebs_csi" {
  addon_name         = "aws-ebs-csi-driver"
  kubernetes_version = var.eks_version
}

data "aws_eks_cluster" "eks" {
  name = var.cluster_name
}

resource "aws_iam_role" "ebs_csi" {
  count              = var.compute_type != "fargate" && var.enable_aws_ebs_csi == "true" ? 1 : 0
  name               = "${local.cluster_name}-eks-csi-addon"
  description        = "Role for Amazon to manage volumes"
  assume_role_policy = data.aws_iam_policy_document.ebs_csi.json
}

data "aws_iam_policy_document" "ebs_csi" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(var.eks_oidc_provider.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:ebs-csi-controller-sa"]
    }

    principals {
      identifiers = [var.eks_oidc_provider.arn]
      type        = "Federated"
    }
  }
}

data "aws_iam_policy_document" "ebs_csi_vol" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:CreateSnapshot",
      "ec2:AttachVolume",
      "ec2:DetachVolume",
      "ec2:ModifyVolume",
      "ec2:DescribeAvailabilityZones",
      "ec2:DescribeInstances",
      "ec2:DescribeSnapshots",
      "ec2:DescribeTags",
      "ec2:DescribeVolumes",
      "ec2:DescribeVolumesModifications",
    ]
    resources = ["*"]
  }

  statement {
    effect  = "Allow"
    actions = ["ec2:CreateTags"]
    resources = [
      "arn:aws:ec2:*:*:volume/*",
      "arn:aws:ec2:*:*:snapshot/*"
    ]
    condition {
      test     = "StringEquals"
      variable = "ec2:CreateAction"
      values = [
        "CreateVolume",
        "CreateSnapshot"
      ]
    }
  }

  statement {
    effect  = "Allow"
    actions = ["ec2:DeleteTags"]
    resources = [
      "arn:aws:ec2:*:*:volume/*",
      "arn:aws:ec2:*:*:snapshot/*"
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["ec2:CreateVolume"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "aws:RequestTag/ebs.csi.aws.com/cluster"
      values   = ["true"]
    }
  }

  statement {
    effect    = "Allow"
    actions   = ["ec2:CreateVolume"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "aws:RequestTag/CSIVolumeName"
      values   = ["*"]
    }
  }

  statement {
    effect    = "Allow"
    actions   = ["ec2:DeleteVolume"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "ec2:ResourceTag/CSIVolumeName"
      values   = ["*"]
    }
  }

  statement {
    effect    = "Allow"
    actions   = ["ec2:DeleteVolume"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "ec2:ResourceTag/ebs.csi.aws.com/cluster"
      values   = ["true"]
    }
  }

  statement {
    effect    = "Allow"
    actions   = ["ec2:DeleteSnapshot"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "ec2:ResourceTag/CSIVolumeSnapshotName"
      values   = ["*"]
    }
  }

  statement {
    effect    = "Allow"
    actions   = ["ec2:DeleteSnapshot"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "ec2:ResourceTag/ebs.csi.aws.com/cluster"
      values   = ["true"]
    }
  }
}


resource "aws_iam_policy" "ebs_csi_vol" {
  count       = var.compute_type != "fargate" && var.enable_aws_ebs_csi == "true" ? 1 : 0
  name_prefix = "${var.cluster_name}-eks-csi-addon"
  description = "EKS EBS CSI driver controller policy for cluster ${var.cluster_name}"
  policy      = data.aws_iam_policy_document.ebs_csi_vol.json
}

resource "aws_iam_role_policy_attachment" "ebs_csi_vol" {
  count      = var.compute_type != "fargate" && var.enable_aws_ebs_csi == "true" ? 1 : 0
  role       = aws_iam_role.ebs_csi[0].name
  policy_arn = aws_iam_policy.ebs_csi_vol[0].arn
}

resource "aws_eks_addon" "ebs_csi" {
  count                    = var.compute_type != "fargate" && var.enable_aws_ebs_csi == "true" ? 1 : 0
  addon_name               = "aws-ebs-csi-driver"
  addon_version            = var.aws_ebs_csi_version != "latest" ? var.aws_ebs_csi_version : data.aws_eks_addon_version.ebs_csi.version
  cluster_name             = var.cluster_name
  resolve_conflicts        = "OVERWRITE"
  service_account_role_arn = aws_iam_role.ebs_csi[0].arn
  tags = merge(
    {
      "eks_addon" = "aws-ebs-csi-driver"
    }
  )
}

