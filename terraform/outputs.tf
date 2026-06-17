output "subnet_a_id" {
  value       = aws_subnet.public_a.id
  description = "The ID of the new custom public subnet in AZ 2a"
}

output "subnet_b_id" {
  value       = aws_subnet.public_b.id
  description = "The ID of the new custom public subnet in AZ 2b"
}