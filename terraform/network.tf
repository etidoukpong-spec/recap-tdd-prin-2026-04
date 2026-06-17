resource "aws_default_vpc" "default" {}

resource "aws_default_subnet" "default_az1" {
  availability_zone = "eu-west-2a"
}

resource "aws_default_subnet" "default_az2" {
  availability_zone = "eu-west-2b"
}