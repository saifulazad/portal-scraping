variable "config" {
  default = "/home/muazzem/.aws/config"
}
variable "credentials" {
  default = "/home/muazzem/.aws/credentials"
}
variable "profile" {
  default = "default"
}
variable "function_name" {
  default = "extractor-lambda-handler"
}
variable "handler_name" {
  default = "lambda_handler"
}
variable "runtime" {
  default = "python3.8"
}
variable "timeout" {
  default = "10"
}
variable "lambda_role_name" {
  default = "extractor-lambda-handler-role"
}

variable "lambda_iam_policy_name" {
  default = "extractor-lambda-handler-policy"
}

variable "bucket_name" {
  default = "extractor-service"
}

variable "environment" {
  default = "dev"
}
variable "zip_file" {
  default = "/extractor.zip"
}