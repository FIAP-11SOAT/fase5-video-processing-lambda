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

data "aws_iam_policy_document" "ecr_allow_lambda" {
  statement {
    sid    = "AllowLambdaPull"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer"
    ]
  }
}

resource "aws_ecr_repository_policy" "allow_lambda" {
  repository = aws_ecr_repository.lambda_repository.name
  policy     = data.aws_iam_policy_document.ecr_allow_lambda.json
}

data "aws_iam_policy_document" "lambda_ecr_access" {
  statement {
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchCheckLayerAvailability"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "lambda_ecr_access" {
  role   = aws_iam_role.lambda_exec_role.id
  policy = data.aws_iam_policy_document.lambda_ecr_access.json
}

resource "aws_ecr_repository_policy" "allow_lambda_to_access_ecr" {
  repository = aws_ecr_repository.lambda_repository.name
  policy     = data.aws_iam_policy_document.ecr_lambda_access_policy.json
}
