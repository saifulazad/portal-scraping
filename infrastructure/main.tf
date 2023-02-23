terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping"
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
  source_dir  = "../extractor"
  output_path = "extractor.zip"
}

# Creating Lambda resource
resource "aws_lambda_function" "test_lambda" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_iam.arn
  handler          = "${var.handler_name}.lambda_handler"
  description      = "https://github.com/saifulazad/portal-scraping/tree/master/infrastructure"
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
resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.test_lambda.arn
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
resource "aws_lambda_function" "scraper_js_function" {
  function_name    = "scraper_js_function"
  role             = aws_iam_role.lambda_iam.arn
  description      = "https://github.com/saifulazad/portal-scraping/tree/master/scraper"
  handler          = "index.handler"
  runtime          = "nodejs12.x"
  timeout          = var.timeout
  memory_size      = 1024
  architectures    = ["arm64"]
  layers           = ["arn:aws:lambda:ap-southeast-1:940443069190:layer:puppeteer-chrome:2"]
  filename         = data.archive_file.archive_scraper.output_path
  source_code_hash = data.archive_file.archive_scraper.output_base64sha256
}



// Allow CloudWatch to invoke our function
resource "aws_lambda_permission" "allow_cloudwatch_to_invoke" {
  function_name = aws_lambda_function.scraper_js_function.function_name
  statement_id  = "CloudWatchInvoke"
  action        = "lambda:InvokeFunction"

  source_arn = aws_cloudwatch_event_rule.every_day.arn
  principal  = "events.amazonaws.com"
}

// Create the "cron" schedule
resource "aws_cloudwatch_event_rule" "every_day" {
  name                = "Scraping"
  schedule_expression = var.schedule
}

resource "aws_cloudwatch_event_target" "invoke_lambda" {
  rule = aws_cloudwatch_event_rule.every_day.name
  arn  = aws_lambda_function.scraper_js_function.arn
}