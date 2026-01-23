module "auth_lambda" {
  source = "./modules/lambda"

  project_name = "${var.project_name}-auth"
  image_name   = "default-lambda-image"
  variables_map = {
    COGNITO_USER_POOL_ID = local.aws_infra_secrets["COGNITO_USER_POOL_ID"]
    COGNITO_USER_POOL_CLIENT_ID = local.aws_infra_secrets["COGNITO_USER_POOL_CLIENT_ID"]
  }
}


# API Gateway Lambda Integration
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = data.aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.auth_lambda.lambda_function_invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "auth_route" {
  api_id    = data.aws_apigatewayv2_api.http_api.id
  route_key = "ANY /auth"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "lambda_permission_api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.auth_lambda.lambda_function_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${data.aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}