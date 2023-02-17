provider "aws" {
  region = "us-east-1"
  shared_config_files = ["/home/azad/.aws/config"]
  shared_credentials_files = ["/home/azad/.aws/credentials"]
  profile = "default"

}
