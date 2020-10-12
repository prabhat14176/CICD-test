provider "aws" {
  version = "~> 2.0"
  region  = "eu-west-2"
}

resource "aws_s3_bucket" "urllisterservice" {
  bucket = "urllisterservice"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"

  }

  tags   = {
    Name        = "Contains the urllisterservice values"
    Environment = "Prod"
  }

}

resource "aws_s3_bucket_policy" "urllisterservice" {
  bucket = aws_s3_bucket.urllisterservice.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "allowReadAccessToResponderBucket",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
          "s3:GetObject"
      ],
      "Resource": [
          "arn:aws:s3:::urllisterservice/*"
      ]
    }
  ]
}
POLICY
}
