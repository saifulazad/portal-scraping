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
data "archive_file" "archive_zip_validate" {
  type        = "zip"
  source_dir  = "../../job_importer"
  output_path = "job_importer.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "lambda_handler" {
  function_name    = var.function_name
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_function.lambda_handler"
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
  function_name = aws_lambda_function.lambda_handler.function_name
  statement_id  = "CloudWatchInvoke"
  action        = "lambda:InvokeFunction"
  source_arn    = aws_cloudwatch_event_rule.job_post_lambda_event.arn
  principal     = "events.amazonaws.com"
}

// Create the "cron" schedule
resource "aws_cloudwatch_event_rule" "job_post_lambda_event" {
  name                = "job-importer-cron"
  description         = "Allow to run lambda function in cron job"
  schedule_expression = var.schedule
}

resource "aws_cloudwatch_event_target" "invoke_scraper_lambda_handler" {
  rule = aws_cloudwatch_event_rule.job_post_lambda_event.name
  arn  = aws_lambda_function.lambda_handler.arn
}
