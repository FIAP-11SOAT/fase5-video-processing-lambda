output "lambda_function_name" {
  description = "The name of the Lambda function."
  value       = aws_lambda_function.lambda.function_name
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function."
  value       = aws_lambda_function.lambda.arn
}

output "lambda_function_invoke_arn" {
  description = "The invoke ARN of the Lambda function."
  value       = aws_lambda_function.lambda.invoke_arn
}

output "lambda_log_group_name" {
  description = "The name of the CloudWatch log group for the Lambda function."
  value       = aws_cloudwatch_log_group.lambda_log_group.name
}
