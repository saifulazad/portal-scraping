variable "typesense_api_key" {
  type    = string
}
variable "google_map_api_key" {
  type = string
}
variable "function_name" {
  default = "job-post-lambda-handler"
}
variable "handler_name" {
  default = "lambda_function"
}

variable "runtime" {
  default = "python3.8"
}
variable "timeout" {
  default = "300"
}
variable "lambda_role_name" {
  default = "job-post-lambda-handler-role"
}

variable "lambda_iam_policy_name" {
  default = "job-post-lambda-handler-policy"
}
variable "lambda_layers" {
  default = "arn:aws:lambda:ap-southeast-1:940443069190:layer:job-post:1"
}
variable "job_importer_lambda_layers" {
  default = "arn:aws:lambda:ap-southeast-1:940443069190:layer:google-map:2"
}
variable "environment" {
  default = "dev"
}
variable "zip_file" {
  default = "job-post.zip"
}
variable "schedule" {
  default = "cron(20 18 * * ? *)"
}
