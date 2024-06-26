

output "api_url" {
  value = aws_api_gateway_deployment.voting_api_deployment.invoke_url
}


