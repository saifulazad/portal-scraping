terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping/importer"
    region = "ap-southeast-1"
  }
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
  source_dir  = "../job_post"
  output_path = "jobpost.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "extractor_lambda_handler" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_iam.arn
  handler          = "${var.handler_name}.lambda_handler"
  description      = ""
  runtime          = var.runtime
  timeout          = var.timeout
  architectures    = ["arm64"]
  layers           = [var.lambda_layers]
  filename         = data.archive_file.archive_zip_validate.output_path
  source_code_hash = data.archive_file.archive_zip_validate.output_base64sha256
}

# Creating s3 resource for invoking to lambda function
resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}

# Adding S3 bucket as trigger to my lambda and giving the permissions
resource "aws_s3_bucket_notification" "aws_lambda_trigger" {
  bucket = aws_s3_bucket.bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.extractor_lambda_handler.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "joblinksfile/"
  }
  depends_on = [aws_lambda_permission.lambda_permission]
}
data "archive_file" "archive_scraper" {
  type        = "zip"
  source_dir  = "../scraper"
  output_path = "scraper.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "scraper_lambda_handler" {
  function_name    = "scraper-lambda-handler"
  role             = aws_iam_role.lambda_iam.arn
  description      = "https://github.com/saifulazad/portal-scraping"
  handler          = "index.handler"
  runtime          = "nodejs12.x"
  timeout          = var.timeout
  memory_size      = 1024
  architectures    = ["x86_64"]
  layers           = ["arn:aws:lambda:ap-southeast-1:940443069190:layer:puppeteer-chrome:2"]
  filename         = data.archive_file.archive_scraper.output_path
  source_code_hash = data.archive_file.archive_scraper.output_base64sha256
}



// Allow CloudWatch to invoke our function
resource "aws_lambda_permission" "allow_cloudwatch_to_invoke" {
  function_name = aws_lambda_function.scraper_lambda_handler.function_name
  statement_id  = "CloudWatchInvoke"
  action        = "lambda:InvokeFunction"
  source_arn = aws_cloudwatch_event_rule.scraper_lambda_event.arn
  principal  = "events.amazonaws.com"
}

// Create the "cron" schedule
resource "aws_cloudwatch_event_rule" "scraper_lambda_event" {
  name                = "bd-jobs-cron"
  description = "trigger lambda function"
  schedule_expression = var.schedule
}

resource "aws_cloudwatch_event_target" "invoke_scraper_lambda_handler" {
  rule = aws_cloudwatch_event_rule.scraper_lambda_event.name
  arn  = aws_lambda_function.scraper_lambda_handler.arn
}
