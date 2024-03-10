variable "google_map_api_key" {
  type = string
}
variable "lambda_layer" {
  default = "arn:aws:lambda:ap-southeast-1:940443069190:layer:google-map:2"
}
variable "timeout" {
  default = "10" # the unit is in second
}
