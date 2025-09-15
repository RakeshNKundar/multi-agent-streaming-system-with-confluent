terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "2.39.0"
    }
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "1.16.0"
    }
  }
}


resource "random_string" "random" {
  length  = 4
  upper   = false
  special = false
}

provider "confluent" {
  cloud_api_key    = var.cc_cloud_api_key
  cloud_api_secret = var.cc_cloud_api_secret
}

provider "mongodbatlas" {
  public_key  = var.mongodbatlas_public_key
  private_key = var.mongodbatlas_private_key
}

variable "cc_cloud_api_key" {}
variable "cc_cloud_api_secret" {}
variable "mongodbatlas_public_key" {}
variable "mongodbatlas_private_key" {}

data "http" "myip" {
  url = "https://ipv4.icanhazip.com"
}

data "confluent_ip_addresses" "default" {
  filter {
    clouds        = ["AWS"]
    regions       = [data.aws_region.current.name]
    services      = ["CONNECT"]
    address_types = ["EGRESS"]
  }
}

data "confluent_organization" "default" {}

data "aws_caller_identity" "current" {}
