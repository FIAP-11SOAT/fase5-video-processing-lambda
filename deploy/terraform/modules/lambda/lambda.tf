resource "aws_lambda_function" "lambda" {
  function_name = "${var.project_name}-lambda-function"
  package_type  = "Image"
  image_uri     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.region}.amazonaws.com/${var.image_name}:latest"
  role          = aws_iam_role.lambda_exec_role.arn

  memory_size = 512

  lifecycle {
    ignore_changes = [
      image_uri
    ]
  }

  environment {
    variables = var.variables_map
  }
}