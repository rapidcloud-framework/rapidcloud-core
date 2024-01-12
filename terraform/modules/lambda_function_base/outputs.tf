output "arn" {
  value = aws_iam_role.role.arn
}
output "name" {
  value = aws_iam_role.role.name
}
output "id" {
  value = aws_iam_role.role.id
}
output "sg_id" {
  value = aws_security_group.security_group.id
}
