terraform {
  backend "s3" {
    bucket = "fractalslab-terraform-state"
    key    = "states/portal-scraping/importer"
    region = "ap-southeast-1"
  }
}
provider "aws" {
  region = "ap-southeast-1"
}
#IAM Permission for lamda
resource "aws_iam_role" "lambda_role" {
  name = "my-lambda-role-2"

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

#Create Lambda
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

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3FullAccess",
  "arn:aws:iam::aws:policy/CloudWatchFullAccess", ]
}

data "archive_file" "archive_zip_validate" {
  type        = "zip"
  source_dir  = "../../job_post"
  output_path = "job_post.zip"
}

resource "aws_lambda_function" "test_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "job_post.zip"
  function_name = "job_importer"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.archive_zip_validate.output_base64sha256

  runtime = "python3.9"

  environment {
    variables = {
      foo = "bar"
    }
  }
}
