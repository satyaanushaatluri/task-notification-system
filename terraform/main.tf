# STARTER ONLY - committing this file creates NO AWS resources.
# To create resources you must run `terraform init` and `terraform apply`
# with valid AWS credentials. This starter provisions only an ECR repository
# to hold the app container image. It does NOT create a production EKS
# cluster, ECS service, database, or public deployment.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "region" {
  description = "AWS region for the ECR repository."
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name, used for the ECR repository name."
  type        = string
  default     = "task-notification-system"
}

provider "aws" {
  region = var.region
}

resource "aws_ecr_repository" "app" {
  name                 = var.app_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    app       = var.app_name
    managedby = "terraform-starter"
  }
}

output "ecr_repository_url" {
  description = "Push the container image to this URL, then use it in k8s/deployment.yaml."
  value       = aws_ecr_repository.app.repository_url
}
