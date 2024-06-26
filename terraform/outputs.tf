output "lambda_function_arn" {
  value = aws_lambda_function.voting_function-jdhg.arn
}

output "api_gateway_url" {
  value = aws_api_gateway_rest_api.voting_api.execution_arn
}


