terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping/importer"
    region = "ap-southeast-1"
  }
}
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Creating Lambda IAM resource
resource "aws_iam_role" "iam_for_lambda" {
  name                = "lambda_importer_job_import"
  assume_role_policy  = data.aws_iam_policy_document.assume_role.json
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchFullAccess",
  ]
}

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.job_post_lambda_handler.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::extractor-service-dev"
}
data "archive_file" "archive_zip_validate" {
  type        = "zip"
  source_dir  = "../../job_post"
  output_path = "job_post.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "job_post_lambda_handler" {
  function_name    = var.function_name
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "${var.handler_name}.lambda_handler"
  description      = "https://github.com/saifulazad/portal-scraping/tree/master/job_importer"
  runtime          = var.runtime
  timeout          = var.timeout
  architectures    = ["arm64"]
  layers           = [var.lambda_layer]
  filename         = data.archive_file.archive_zip_validate.output_path
  source_code_hash = data.archive_file.archive_zip_validate.output_base64sha256
  environment {
    variables = {
      TYPESENSE_API_KEY = var.typesense_api_key
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
