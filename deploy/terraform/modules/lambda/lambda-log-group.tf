resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = 30

  tags = {
    Name = "${var.project_name}-${data.aws_region.current.region}-lambda-log-group"
  }
}
