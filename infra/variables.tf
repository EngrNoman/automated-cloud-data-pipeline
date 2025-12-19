variable "aws_region" {
  description = "AWS Region Jahan resources banagi"
  default = "us-east-1"  
}

variable "project_name" {
  description = "Project k Unique name "
  default = "automated-aws-datapipeline"
}

variable "environment"{
  description = "Environment (dev , prod, staging)"
  default = "dev"
}