
data "aws_iam_policy_document" "efs_csi" {
  statement {
    actions = [
      "elasticfilesystem:DescribeAccessPoints",
      "elasticfilesystem:DescribeFileSystems",
      "elasticfilesystem:DescribeMountTargets",
      "ec2:DescribeAvailabilityZones"
    ]
    resources = ["*"]
    effect    = "Allow"
  }

  statement {
    actions = [
      "elasticfilesystem:CreateAccessPoint"
    ]
    resources = ["*"]
    effect    = "Allow"
    condition {
      test     = "StringLike"
      variable = "aws:RequestTag/efs.csi.aws.com/cluster"
      values   = ["true"]
    }
  }

  statement {
    actions = [
      "elasticfilesystem:DeleteAccessPoint"
    ]
    resources = ["*"]
    effect    = "Allow"
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceTag/efs.csi.aws.com/cluster"
      values   = ["true"]
    }
  }

  statement {
    actions = [
      "elasticfilesystem:TagResource",
    ]
    resources = ["*"]
    effect    = "Allow"
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceTag/efs.csi.aws.com/cluster"
      values   = ["true"]
    }
  }
}

resource "aws_iam_policy" "efs_csi" {
  name   = "${local.cluster_name}-AmazonEKS_EFS_CSI_Driver_Policy"
  policy = data.aws_iam_policy_document.efs_csi.json
}

data "aws_iam_policy_document" "efs_csi_sts" {

  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.eks_oidc_provider.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(var.eks_oidc_provider.url, "https://", "")}:sub"

      values = [
        "system:serviceaccount:kube-system:efs-csi-controller-sa"
      ]
    }

    effect = "Allow"
  }
}

resource "aws_iam_role" "efs_csi" {
  name               = "${local.cluster_name}-AmazonEKS_EFS_CSI_DriverRole"
  assume_role_policy = data.aws_iam_policy_document.efs_csi_sts.json
}

resource "aws_iam_role_policy_attachment" "efs_csi" {
  role       = aws_iam_role.efs_csi.name
  policy_arn = aws_iam_policy.efs_csi.arn
}

resource "kubernetes_service_account_v1" "efs_csi" {
  metadata {
    name      = "efs-csi-controller-sa"
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name" = "efs-csi-controller-sa"
    }
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.efs_csi.arn
    }
  }
}

# https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/master/examples/kubernetes/dynamic_provisioning/specs/storageclass.yaml
resource "kubernetes_storage_class" "efs_csi" {
  metadata {
    name = "efs-sc"
  }
  storage_provisioner = "efs.csi.aws.com"
  parameters = {
    provisioningMode = "efs-ap"
    fileSystemId     = "${var.file_system_id}"
    directoryPerms   = "700"
  }
}


resource "helm_release" "aws_efs_csi_driver" {
  chart      = "aws-efs-csi-driver"
  name       = "aws-efs-csi-driver"
  namespace  = "kube-system"
  repository = "https://kubernetes-sigs.github.io/aws-efs-csi-driver/"
  # deploy options
  atomic          = false
  cleanup_on_fail = false
  timeout         = 1200
  wait            = false

  set {
    name  = "controller.serviceAccount.create"
    value = false
  }

  set {
    name  = "controller.serviceAccount.name"
    value = "efs-csi-controller-sa"
  }

  set {
    name  = "image.repository"
    value = "602401143452.dkr.ecr.${var.region}.amazonaws.com/eks/aws-efs-csi-driver"
  }
}
