/**
 * AWS Cognito User Pool Configuration
 * Simple username/password authentication
 */

resource "aws_cognito_user_pool" "auth_pool" {
  name = "${var.project_name}-user-pool"

  # Username configuration
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  # Password policy
  password_policy {
    minimum_length                   = 8
    require_lowercase                = true
    require_uppercase                = true
    require_numbers                  = true
    require_symbols                  = true
    temporary_password_validity_days = 7
  }

  # Account recovery
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # User pool add-ons
  user_pool_add_ons {
    advanced_security_mode = "ENFORCED"
  }

  # Schema attributes
  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true

    string_attribute_constraints {
      min_length = 5
      max_length = 256
    }
  }

  # Tags
  tags = {
    Name        = "${var.project_name}-user-pool"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cognito_user_pool_client" "auth_client" {
  name         = "${var.project_name}-client"
  user_pool_id = aws_cognito_user_pool.auth_pool.id

  # Authentication flows
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  # Token validity
  access_token_validity  = 1  # hours
  id_token_validity      = 1  # hours
  refresh_token_validity = 30 # days

  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }

  # Security
  prevent_user_existence_errors = "ENABLED"
  enable_token_revocation       = true

  # Read and write attributes
  read_attributes = [
    "email",
    "email_verified"
  ]

  write_attributes = [
    "email"
  ]
}

# Outputs
output "cognito_user_pool_id" {
  description = "The ID of the Cognito User Pool"
  value       = aws_cognito_user_pool.auth_pool.id
}

output "cognito_user_pool_arn" {
  description = "The ARN of the Cognito User Pool"
  value       = aws_cognito_user_pool.auth_pool.arn
}

output "cognito_user_pool_endpoint" {
  description = "The endpoint of the Cognito User Pool"
  value       = aws_cognito_user_pool.auth_pool.endpoint
}

output "cognito_client_id" {
  description = "The ID of the Cognito User Pool Client"
  value       = aws_cognito_user_pool_client.auth_client.id
  sensitive   = true
}
