/**
 * Auth Lambda Configuration
 */

# IAM Role for Auth Lambda
resource "aws_iam_role" "auth_lambda_role" {
  name = "${var.project_name}-auth-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-auth-lambda-role"
    Environment = var.environment
  }
}

# IAM Policy for Auth Lambda
resource "aws_iam_role_policy" "auth_lambda_policy" {
  name = "${var.project_name}-auth-lambda-policy"
  role = aws_iam_role.auth_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "cognito-idp:SignUp",
          "cognito-idp:InitiateAuth",
          "cognito-idp:GetUser",
          "cognito-idp:ListUsers"
        ]
        Resource = aws_cognito_user_pool.auth_pool.arn
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "auth_lambda" {
  filename         = "../../lambda-packages/auth_lambda.zip"
  function_name    = "${var.project_name}-auth-lambda"
  role            = aws_iam_role.auth_lambda_role.arn
  handler         = "src.auth_lambda.presentation.handlers.main_handler"
  source_code_hash = fileexists("../../lambda-packages/auth_lambda.zip") ? filebase64sha256("../../lambda-packages/auth_lambda.zip") : ""
  runtime         = var.lambda_runtime
  memory_size     = var.lambda_memory_size
  timeout         = var.lambda_timeout

  environment {
    variables = {
      COGNITO_USER_POOL_ID = aws_cognito_user_pool.auth_pool.id
      COGNITO_CLIENT_ID    = aws_cognito_user_pool_client.auth_client.id
      ENVIRONMENT          = var.environment
    }
  }

  tags = {
    Name        = "${var.project_name}-auth-lambda"
    Environment = var.environment
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "auth_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.auth_lambda.function_name}"
  retention_in_days = 7

  tags = {
    Name        = "${var.project_name}-auth-lambda-logs"
    Environment = var.environment
  }
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "auth_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth_lambda.function_name
  principal     = "apigateway.amazonaws.com"
}

# Outputs
output "auth_lambda_arn" {
  description = "ARN of the Auth Lambda function"
  value       = aws_lambda_function.auth_lambda.arn
}

output "auth_lambda_name" {
  description = "Name of the Auth Lambda function"
  value       = aws_lambda_function.auth_lambda.function_name
}
