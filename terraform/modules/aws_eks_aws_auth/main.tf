locals {
  map_roles = concat(
    [for role_arn in var.node_group_roles : {
      rolearn  = role_arn
      username = "system:node:{{EC2PrivateDNSName}}"
      groups = [
        "system:bootstrappers",
        "system:nodes",
      ]
      }
    ],

    [for role_arn in var.fargate_profile_roles : {
      rolearn  = role_arn
      username = "system:node:{{247654790127}}"
      groups = [
        "system:node-proxier",
        "system:bootstrappers",
        "system:nodes",
      ]
      }
    ],
    var.map_roles
  )
  map_users = var.map_users

}

resource "kubernetes_config_map_v1_data" "aws_auth" {
  count = length(var.node_group_roles) > 0 || length(var.fargate_profile_roles) > 0 ? 1 : 0
  metadata {
    name      = "aws-auth"
    namespace = "kube-system"
  }
  data = {
    mapRoles = yamlencode(local.map_roles)
    mapUsers = yamlencode(var.map_users)
  }
  force = true
}
