resource "aws_wafv2_web_acl" "rc_waf" {
  name  = var.waf_name
  scope = var.waf_scope
  default_action {
    dynamic "allow" {
      for_each = var.allow_requests_by_default ? [1] : []
      content {}
    }

    dynamic "block" {
      for_each = var.allow_requests_by_default ? [] : [1]
      content {}
    }
  }
  rule {
    name     = "RC-AWSManagedRulesCommonRuleSet"
    priority = 0

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RC-AWSManagedRulesCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }
  rule {
    name     = "RC-AWSManagedRulesAdminProtectionRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAdminProtectionRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RC-AWSManagedRulesAdminProtectionRuleSet"
      sampled_requests_enabled   = true
    }
  }
  rule {
    name     = "RC-AWSManagedRulesKnownBadInputsRuleSet"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RC-AWSManagedRulesKnownBadInputsRuleSet"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = var.waf_name
    sampled_requests_enabled   = true
  }
  tags = var.tags
}