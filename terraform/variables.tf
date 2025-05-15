variable "bucket_name" {
  type        = string
  default     = "nt532-bucket"
  description = "Name of S3 bucket"
}

variable "dynamodb_table_name" {
  type = string
  default = "nt532_collection"
  description = "Name of DynamoDB table"
}

variable "hash_key" {
  type = string
  default = "RekognitionId"
  description = "Hash key of DynamoDB table"
}

variable "attribute_name" {
  type = string
  default = "RekognitionId"
  description = "Attribute name"
}

variable "attribute_type" {
  type = string
  default = "S"
  description = "Attribute type"
}

variable "read_capacity" {
  type = number
  default = 1
  description = "Read capacity unit of table"
}

variable "write_capacity" {
  type = number
  default = 1
  description = "Write capacity unit of table"
}

variable "rekognition_collection_id" {
  type = string
  default = "nt532_collection"
  description = "Name of Rekognition Collection"
}

variable "access_policy_name" {
  type = string
  default = "access_policy"
}

variable "iam_role_name" {
  type = string
  default = "LambdaRekognitionRole"
  description = "Name of IAM role for Lambda"
}