terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.50.0"
    }
  }

  required_version = ">= 1.2"

  backend "s3" {
    bucket = "etido-tdd-tf-state"
    key    = "ecs-express/terraform.tfstate"
    region = "eu-west-2"
  }
}