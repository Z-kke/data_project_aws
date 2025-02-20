terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
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
  filename         = "${path.module}/../lambdas/hello_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambdas/hello_lambda.zip")
}

