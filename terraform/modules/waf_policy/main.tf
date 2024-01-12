resource "azurerm_web_application_firewall_policy" "waf_policy" {
    name                = var.name
    resource_group_name = var.resource_group
    location            = var.location
    managed_rules {
      managed_rule_set {
        version         = var.rule_set_version
      }
    }
}

output "id" {
    value = azurerm_web_application_firewall_policy.waf_policy.id
}