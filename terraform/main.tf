terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  backend "s3" {
    bucket         = "terraform-state-bucket-534"
    key            = "terraform.tfstate" # Path within the bucket to store state
    region         = "eu-north-1"
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region
}

# Create an IAM role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Define the Lambda function resource
resource "aws_lambda_function" "hello_lambda" {
  function_name    = "hello_lambda"
  handler          = "hello_lambda.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec.arn
  filename         = "${path.module}/../src/lambdas/hello_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../src/lambdas/hello_lambda.zip")
}

# This rule schedules your Lambda to run every 5 minutes.
# A 5-minute interval is free-tier friendly.
resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "hello_lambda_schedule"
  schedule_expression = "rate(60 minutes)"
}

# This connects the schedule (event rule) to your Lambda function.
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  target_id = "hello_lambda_target"
  arn       = aws_lambda_function.hello_lambda.arn
}

# This grants CloudWatch Events permission to invoke your Lambda.
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
}

# Create a DynamoDB table in on-demand (PAY_PER_REQUEST) mode,
resource "aws_dynamodb_table" "data_table" {
  name         = var.db_table_name
  billing_mode = "PAY_PER_REQUEST" # Should be free tier friendly
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
