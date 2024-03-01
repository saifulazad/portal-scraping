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
  default = "lambda_function"
}
variable "lambda_layers" {
  default = "arn:aws:lambda:ap-southeast-1:940443069190:layer:bd-jobs-mapper:4"
}
variable "runtime" {
  default = "python3.11"
}
variable "timeout" {
  default = "300"
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
variable "schedule" {
  default = "cron(0 0 * * ? *)"
}
