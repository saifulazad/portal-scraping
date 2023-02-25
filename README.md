
# Portal Scraping 


[![Watch the video](https://github.com/saifulazad/portal-scraping/blob/mamun_wip/infrastructure/app.jpeg)](https://youtu.be/jtVVs7RWkkM)


### Let's create the infrastructure 🚀
This Terraform code creates a serverless architecture on AWS, which includes an S3 bucket, an 
AWS Lambda function, an IAM role for the Lambda function, and an S3 trigger to invoke the Lambda 
function. This documentation will provide an overview of the code, explain each resource, and show 
how to deploy the infrastructure on AWS.

#### Step: 1
Frock and Clone the GitHub repository for the project [here.](https://github.com/saifulazad/portal-scraping)

#### Step: 2
Create a lambda function layer and replace `aws_lambda_function` layer 
with your AWS Function layer arn. [arn:aws:lambda******] [Doc for Lambda layers.](https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d) 

#### Step: 3
Create a `terraform.tfvars` in infrastructure directory and add your `aws_access_key`, `aws_secret_key`.

``terraform.tfvars``  file will look like this:
```
    aws_access_key = "*******5NU"         
    aws_secret_key = "*******9Rwz32c"
```

#### Step: 4

After filling in the custom values, 
run `terraform apply -var-file=terraform.tfvars` , it will display all the 
resources discussed above that need to be created, select `yes` to create the 
resources.


#### Step: 5
If everything is OK, Then deploy your project by following the command below

```
  $ terraform init                   # Initialize project
  $ terraform plan                   # setup internal state
  $ terraform apply -auto-approve    # Deploy the infrastructure
  $ terraform destroy                # Only if you want to destroy the infra and cleanup
```



#### Step: 6
After all the resource has been fully created, upload a file to the S3 bucket 
created, you'll see the lambda function has been triggered.


## Introduction 
Scraping is a hot topic nowadays. This is a demo about my scraping skill. [bdjobs](http://jobs.bdjobs.com/jobsearch.asp?fcatId=8) is the largest job posting site in Bangladesh. We are only concern on IT-related jobs.
Please note that this is only for training and educational purpose. Do not use this to hamper our bdjobs portal.  

## How does it work:
Basically, there are two folders. one is `scraper` and another is `extractor`.

To understand and install `scraper` please follow this video [link.](https://www.youtube.com/watch?v=1j2Fl63QBFI)

To understand and install `extractor` please follow this video [link.](https://www.youtube.com/watch?v=Z7eDjhczcgw)
  
Please note that `scraper` folder will collect links by puppeteer and then those links will feed to `extractor` to collect
details information from each link.

### Contact
> Facebook https://www.facebook.com/mr.saiful.azad

> Gmail mr.saiful.azad@gmail.com


[![Visits Badge](https://badges.pufler.dev/visits/braydoncoyer/braydoncoyer)](https:braydoncoyer.dev)
[![Twitter Badge](https://img.shields.io/badge/Twitter-Profile-informational?style=flat&logo=twitter&logoColor=white&color=1CA2F1)](https://twitter.com/BraydonCoyer)
[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-Profile-informational?style=flat&logo=linkedin&logoColor=white&color=0D76A8)](https://www.linkedin.com/in/braydon-coyer/)
[![CodePen Badge](https://img.shields.io/badge/CodePen-Profile-informational?style=flat&logo=codepen&logoColor=white&color=black)](https://codepen.io/braydoncoyer)