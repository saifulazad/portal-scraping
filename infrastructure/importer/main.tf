terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping/importer"
    region = "ap-southeast-1"
  }
}

# Creating Lambda IAM resource
resource "aws_iam_role" "lambda_iam" {
  name = var.lambda_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}
resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.job_post_lambda_handler.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::extractor-service-dev"
}

resource "aws_iam_role_policy" "job_importer_keys_role_policy" {
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
  source_dir  = "../../job_post"
  output_path = "job_post.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "job_post_lambda_handler" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_iam.arn
  handler          = "${var.handler_name}.lambda_handler"
  description      = "https://github.com/saifulazad/portal-scraping/tree/master/job_post"
  runtime          = var.runtime
  timeout          = var.timeout
  architectures    = ["arm64"]
  layers           = [var.lambda_layers]
  filename         = data.archive_file.archive_zip_validate.output_path
  source_code_hash = data.archive_file.archive_zip_validate.output_base64sha256
  environment {
    variables = {
      API_KEY = var.typesense_api_key
    }
  }
}

data "archive_file" "archive_job_importer_zip_validate" {
  type        = "zip"
  source_dir  = "../../job_importer"
  output_path = "job_importer.zip"
}

# Lambda resource for import job
resource "aws_lambda_function" "job_importer_lambda_handler" {
  filename         = "job_importer.zip"
  function_name    = "job-importer"
  role             = aws_iam_role.lambda_iam.arn
  handler          = "lambda_function.lambda_handler"
  architectures    = ["x86_64"]
  layers           = [var.job_importer_lambda_layers]
  source_code_hash = data.archive_file.archive_job_importer_zip_validate.output_base64sha256
  runtime          = "python3.9"
  environment {
    variables = {
      GOOGLE_MAP_API_KEY = var.google_map_api_key
    }
  }
}

resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.job_importer_lambda_handler.function_name
  authorization_type = "NONE"
}

// Allow CloudWatch to invoke our function
resource "aws_lambda_permission" "allow_cloudwatch_to_invoke" {
  function_name = aws_lambda_function.job_post_lambda_handler.function_name
  statement_id  = "CloudWatchInvoke"
  action        = "lambda:InvokeFunction"
  source_arn    = aws_cloudwatch_event_rule.job_post_lambda_event.arn
  principal     = "events.amazonaws.com"
}

// Create the "cron" schedule
resource "aws_cloudwatch_event_rule" "job_post_lambda_event" {
  name                = "importer-cron"
  description         = "trigger lambda function"
  schedule_expression = var.schedule
}

resource "aws_cloudwatch_event_target" "invoke_scraper_lambda_handler" {
  rule = aws_cloudwatch_event_rule.job_post_lambda_event.name
  arn  = aws_lambda_function.job_post_lambda_handler.arn
}
