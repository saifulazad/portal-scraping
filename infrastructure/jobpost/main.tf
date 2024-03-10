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
  name                = "lambda_importer_job_post"
  assume_role_policy  = data.aws_iam_policy_document.assume_role.json
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchFullAccess",
  ]
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
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_function.lambda_handler"
  description      = "https://github.com/saifulazad/portal-scraping/tree/master/job_post"
  architectures    = ["arm64"]
  layers           = [var.lambda_layer]
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
  cors {
    allow_origins = ["*"]
    allow_methods = ["POST"]
  }
}
