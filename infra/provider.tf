terraform {
  required_providers {
    # 1. AWS Provider
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    # 2. Archive Provider (Yeh missing tha, isliye error aya)
    # Iski zaroorat humein Python code ko Zip karne k liye hai
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4.2"
    }
  }
}

# AWS se connection
provider "aws" {
  region = var.aws_region
}
