variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "image_name" {
  description = "The name of the ECR image for the Lambda function"
  type        = string
}

variable "additional_permissions_json" {
  description = "Additional IAM permissions for the Lambda function in JSON format"
  type        = string
  default     = null
}


variable "variables_map" {
  description = "A map of environment variables to set in the Lambda function"
  type        = map(string)
  default     = {}
}