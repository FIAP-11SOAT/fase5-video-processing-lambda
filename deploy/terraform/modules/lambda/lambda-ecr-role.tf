data "aws_iam_policy_document" "ecr_lambda_access_policy" {
  statement {
    sid    = "LambdaECRImageRetrievalPolicy"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.lambda_exec_role.arn]
    }

    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability"
    ]
  }
}

resource "aws_ecr_repository_policy" "allow_lambda_to_access_ecr" {
  repository = aws_ecr_repository.lambda_repository.name
  policy     = data.aws_iam_policy_document.ecr_lambda_access_policy.json
}
