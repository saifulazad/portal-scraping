resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.job_post_lambda_handler.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::extractor-service-dev"
}