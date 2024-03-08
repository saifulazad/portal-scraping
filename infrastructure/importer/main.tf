terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping/importer"
    region = "ap-southeast-1"
  }
}

#IAM Permission for lamda
resource "aws_iam_role" "lambda_role" {
  name               = "job-importer-lambda-role"
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
