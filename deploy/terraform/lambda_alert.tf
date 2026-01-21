/**
 * Alert Lambda Configuration
 */

# IAM Role for Alert Lambda
resource "aws_iam_role" "alert_lambda_role" {
  name = "${var.project_name}-alert-lambda-role"

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
    Name        = "${var.project_name}-alert-lambda-role"
    Environment = var.environment
  }
}

# IAM Policy for Alert Lambda
resource "aws_iam_role_policy" "alert_lambda_policy" {
  name = "${var.project_name}-alert-lambda-policy"
  role = aws_iam_role.alert_lambda_role.id

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
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "alert_lambda" {
  filename         = "../../lambda-packages/alert_lambda.zip"
  function_name    = "${var.project_name}-alert-lambda"
  role            = aws_iam_role.alert_lambda_role.arn
  handler         = "src.alert_lambda.handler.handler"
  source_code_hash = fileexists("../../lambda-packages/alert_lambda.zip") ? filebase64sha256("../../lambda-packages/alert_lambda.zip") : ""
  runtime         = var.lambda_runtime
  memory_size     = var.lambda_memory_size
  timeout         = var.lambda_timeout

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  tags = {
    Name        = "${var.project_name}-alert-lambda"
    Environment = var.environment
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "alert_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.alert_lambda.function_name}"
  retention_in_days = 7

  tags = {
    Name        = "${var.project_name}-alert-lambda-logs"
    Environment = var.environment
  }
}

# SNS Topic for CloudWatch Alarms
resource "aws_sns_topic" "cloudwatch_alarms" {
  name = "${var.project_name}-cloudwatch-alarms"

  tags = {
    Name        = "${var.project_name}-cloudwatch-alarms"
    Environment = var.environment
  }
}

# SNS Topic Subscription to Alert Lambda
resource "aws_sns_topic_subscription" "alert_lambda_subscription" {
  topic_arn = aws_sns_topic.cloudwatch_alarms.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.alert_lambda.arn
}

# Lambda Permission for SNS
resource "aws_lambda_permission" "alert_lambda_sns_permission" {
  statement_id  = "AllowSNSInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.alert_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.cloudwatch_alarms.arn
}

# Outputs
output "alert_lambda_arn" {
  description = "ARN of the Alert Lambda function"
  value       = aws_lambda_function.alert_lambda.arn
}

output "alert_lambda_name" {
  description = "Name of the Alert Lambda function"
  value       = aws_lambda_function.alert_lambda.function_name
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for CloudWatch alarms"
  value       = aws_sns_topic.cloudwatch_alarms.arn
}
