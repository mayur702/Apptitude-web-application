terraform {
  backend "s3" {
    bucket = "mayur413310"
    key    = "ecs/terraform.tfstate"
    region = "us-east-2"
  }
}
