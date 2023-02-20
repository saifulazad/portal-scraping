terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping"
    region = "ap-southeast-1"
  }
}

provider "aws" {
  region     = "ap-southeast-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_iam_role_policy" "revoke_keys_role_policy" {
  name = var.lambda_iam_policy_name
  role = aws_iam_role.lambda_iam.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*",
        "logs:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
data "archive_file" "archive_zip_validate" {
  type        = "zip"
  source_dir  = "../extractor"
  output_path = "extractor.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "test_lambda" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_iam.arn
  handler          = "${var.handler_name}.lambda_handler"
  runtime          = var.runtime
  timeout          = var.timeout
  layers           = [var.lambda_layers]
  filename         = data.archive_file.archive_zip_validate.output_path
  source_code_hash = data.archive_file.archive_zip_validate.output_base64sha256
}

# Creating s3 resource for invoking to lambda function
resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}

# Adding S3 bucket as trigger to my lambda and giving the permissions
resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.test_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "joblinksfile/"
  }
depends_on = [aws_lambda_permission.lambda_permission]
}
