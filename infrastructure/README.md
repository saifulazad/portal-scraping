### Let's create the infrastructure 🚀
This Terraform code creates a serverless architecture on AWS, which includes an S3 bucket, an 
AWS Lambda function, an IAM role for the Lambda function, and an S3 trigger to invoke the Lambda 
function. This documentation will provide an overview of the code, explain each resource, and show 
how to deploy the infrastructure on AWS.

#### Step 1
Frock and Clone the GitHub repository for the project [here.](https://github.com/saifulazad/portal-scraping)

#### Step 2
Create a lambda function layer and replace `aws_lambda_function` layer 
with your AWS Function layer arn. [arn:aws:lambda******] [Doc for Lambda layers.](https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d) 

#### Step 3
Navigate to `terraform.tfvars` and fill in the custom values on how you want your 
infrastructure to be deployed.

#### Step 4

After filling in the custom values, 
run `terraform apply -var-file=terraform.tfvars` , it will display all the 
resources discussed above that need to be created, select `yes` to create the 
resources.


#### Step 5
After all the resource has been fully created, upload a file to the S3 bucket 
created, you'll see the lambda function has been triggered.

#### Step 6
If you're done, and you choose to destroy the necessary resources, run `terraform destroy` 
This will destroy all the necessary resources created.


### AWS Infrastructure Deployment Using Terraform

##### Terraform Backend
The backend configuration specifies where Terraform should 
store the state of the infrastructure. In this case, the backend is configured to use an S3 
bucket named ``fractalslab-terraform-state`` in the ``ap-southeast-1`` region with the 
key ``states/portal-scraping``. By using a backend, the infrastructure state is kept 
outside the local workspace, making it easier to collaborate and manage the infrastructure.

#### AWS Provider
The AWS provider configuration specifies the region where the infrastructure should be deployed and the 
access and secret keys for the AWS account. The region is set to ``ap-southeast-1`` and the access and 
secret keys are set using variables ``aws_access_key`` and ``aws_secret_key``. 
Read more about [Provider Configuration](https://developer.hashicorp.com/terraform/language/providers/configuration).



#### AWS IAM Role
The ``aws_iam_role`` resource creates an IAM role that the Lambda function will assume. 
The name attribute is set to a variable ``lambda_role_name`` that specifies the name of the role. 
The ``assume_role_policy`` attribute specifies the permissions that the role has to assume the Lambda 
function. In this case, the role has permission to assume the Lambda function by setting the ``Service``
to ``lambda.amazonaws.com``.

#### AWS IAM Role Policy
The ``aws_iam_role_policy`` resource creates a policy that is attached to the IAM role. 
The policy is used to grant permission to the role to access S3 and CloudWatch Logs. 
The ``name`` attribute is set to a variable ``lambda_iam_policy_name`` that specifies the name 
of the policy. The ``role`` attribute specifies the IAM role's ID. The policy attribute 
is set to a JSON object that specifies the actions that are allowed on S3 and CloudWatch Logs.

#### AWS Lambda Function
The ``aws_lambda_function`` resource creates an AWS Lambda function. 
The ``function_name`` attribute is set to a variable ``function_name``
that specifies the name of the Lambda function. 
The 
``role`` attribute is set to the ARN of the IAM role created earlier. 
The``handler`` attribute specifies the entry point to the Lambda function. 

The``runtime`` attribute specifies the language runtime for the Lambda function. The 
``timeout`` attribute specifies the maximum time that the Lambda function can run before timing out. The 
``layers`` attribute specifies a list of ARNs for [Lambda layers.](https://medium.com/the-cloud-architect/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d) 

The``filename`` attribute specifies the path to the Lambda deployment package. The 
``source_code_hash`` attribute is set to the SHA256 hash of the deployment package.
[Read more about aws_lambda_function.](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function)

#### AWS S3 Bucket
The ``aws_s3_bucket`` resource creates an S3 bucket. The bucket attribute is set to a variable 
``bucket_name`` that specifies the name of the S3 bucket. Read more about [AWS S3 Bucket.](https://aws.amazon.com/s3/)

#### AWS S3 Bucket Notification
The ``aws_s3_bucket_notification`` resource configures an S3 trigger to invoke the Lambda function 
when an object is created in the S3 bucket. 
The bucket attribute is set to the ID of the S3 bucket created earlier. The ``lambda_function`` 
attribute specifies the ARN of the Lambda function, 
the events that trigger the Lambda function, and a filter prefix that specifies the S3 object prefix for 
triggering the Lambda function. The ``depends_on`` attribute specifies that the 
Lambda function must be created before the S3 trigger can be created.

#### AWS Lambda Permission
The ``aws_lambda_permission`` resource adds a permission to the Lambda function.
[Lambda execution role to access Amazon S3 bucket.](https://repost.aws/knowledge-center/lambda-execution-role-s3-bucket)

