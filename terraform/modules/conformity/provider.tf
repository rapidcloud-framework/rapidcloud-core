terraform {
  required_version = "=1.3.4"
  required_providers {
    conformity = {
      version = "~> 0.5.0"
      source  = "trendmicro/conformity"
    }
  }
}