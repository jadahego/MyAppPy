output "lambda_function_arn" {
  value = aws_lambda_function.voting_function-jdhg.arn
}

output "api_url" {
  value = aws_api_gateway_deployment.voting_api_deployment.invoke_url
}


