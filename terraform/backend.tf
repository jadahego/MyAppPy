terraform {
  backend "s3" {
    bucket = "bbog-ca-tf-states"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
