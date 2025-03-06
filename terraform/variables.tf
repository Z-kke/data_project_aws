variable "aws_region" {
  description = "AWS region to deploy"
  type        = string
  default     = "eu-north-1"
}

variable "db_table_name" {
  description = "The name of the DynamoDB table for storing API data."
  type        = string
  default     = "DataIngestionTable"
}
