resource "aws_glue_catalog_database" "catalog" {
  name         = var.name
  description  = var.description
  location_uri = var.location_uri
}

output "name" {
  value = aws_glue_catalog_database.catalog.name
}

output "catalog_name" {
  value = aws_glue_catalog_database.catalog.name
}
