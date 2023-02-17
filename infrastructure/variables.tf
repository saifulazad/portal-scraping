variable "aws_access_key" {
  type = string

}
variable "aws_secret_key" {
  type = string

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
  default = "extractor-service-dev"
}

variable "environment" {
  default = "dev"
}
variable "zip_file" {
  default = "/extractor.zip"
}