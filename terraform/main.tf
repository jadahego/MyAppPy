provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "bbog-my-lambda-functions-bucket-jdhg"
}

resource "aws_iam_role" "lambda_exec-jdhg" {
  name = "lambda_exec_role-jdhg"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid    = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_exec-jdhg_policy" {
  role       = aws_iam_role.lambda_exec-jdhg.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "voting_function-jdhg" {
  filename         = "../lambda_function_payload.zip" 
  function_name    = "votingFunctionjdhg"
  role             = aws_iam_role.lambda_exec-jdhg.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("../lambda_function_payload.zip")
  runtime          = "python3.8"
  environment {
    variables = {
      FLASK_ENV = "production"
    }
  }
}

resource "aws_api_gateway_rest_api" "voting_api" {
  name        = "Voting API"
  description = "API for the Voting application"
}

resource "aws_api_gateway_resource" "vote" {
  rest_api_id = aws_api_gateway_rest_api.voting_api.id
  parent_id   = aws_api_gateway_rest_api.voting_api.root_resource_id
  path_part   = "vote"
}

resource "aws_api_gateway_method" "vote_post" {
  rest_api_id   = aws_api_gateway_rest_api.voting_api.id
  resource_id   = aws_api_gateway_resource.vote.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "vote_post" {
  rest_api_id             = aws_api_gateway_rest_api.voting_api.id
  resource_id             = aws_api_gateway_resource.vote.id
  http_method             = aws_api_gateway_method.vote_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.voting_function-jdhg.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.voting_function-jdhg.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.voting_api.execution_arn}/*/*"
}

output "api_url" {
  value = "${aws_api_gateway_rest_api.voting_api.execution_arn}/vote"
}
