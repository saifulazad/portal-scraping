variable "typesense_api_key" {
  type    = string
}

variable "function_name" {
  default = "job-import"
}
variable "runtime" {
  default = "python3.8"
}
variable "timeout" {
  default = "300" # the unit is in second
}
variable "lambda_role_name" {
  default = "job-post-lambda-handler-role"
}

variable "lambda_layer" {
  default = "arn:aws:lambda:ap-southeast-1:940443069190:layer:job-post:1"
}
variable "schedule" {
  # The default value represents a cron expression scheduling a task to run every day at 12:00 AM (UTC). https://crontab.cronhub.io
  default = "cron(0 0 * * ? *)"
}
