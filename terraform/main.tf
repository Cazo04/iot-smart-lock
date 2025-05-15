module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = var.bucket_name
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }
}

module "dynamodb_table" {
  source   = "terraform-aws-modules/dynamodb-table/aws"

  name     = var.dynamodb_table_name
  hash_key = var.hash_key

  billing_mode = "PROVISIONED"

  read_capacity = var.read_capacity
  write_capacity = var.write_capacity

  attributes = [
    {
      name = var.attribute_name
      type = var.attribute_type
    }
  ]

  tags = {
    Terraform   = "true"
    Environment = "staging"
  }
}

resource "awscc_rekognition_collection" "rekognition_collection" {
  collection_id = var.rekognition_collection_id
}

resource "aws_iam_role" "lambda_iam_role" {
  name = var.iam_role_name
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]}
  )
}

resource "aws_iam_policy" "lambda_access_policy" {
  name        = var.access_policy_name
  policy = jsonencode(
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::nt532-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:ap-southeast-1:381492301125:table/nt532_collection"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:IndexFaces"
            ],
            "Resource": "*"
        }
    ]}
  )
}

resource "aws_iam_role_policy_attachment" "lambda_iam_role_policy" {
  policy_arn = aws_iam_policy.lambda_access_policy.arn
  role       = aws_iam_role.lambda_iam_role.name
}