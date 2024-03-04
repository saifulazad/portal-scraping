import datetime
from s3.utils import upload_jobs_details
from bulk_job_processor import get_all_job_details, create_absolute_url
import boto3
from settings import BUCKET_NAME


def lambda_handler(event, context):
    file_obj = event["Records"][0]
    filename = str(file_obj["s3"]["object"]["key"])
    s3 = boto3.client("s3")
    data = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
    contents = data["Body"].read()
    job_links = contents.decode("utf-8").splitlines()
    absolute_job_urls = [create_absolute_url(line) for line in job_links]
    # print(absolute_job_urls)
    jobs_details = get_all_job_details(absolute_job_urls)
    key = datetime.datetime.now().strftime("%d-%m-%y")
    file_name = f"{key}.json"
    print(file_name)
    upload_jobs_details(key=file_name, content=jobs_details, bucket_name=BUCKET_NAME)


if __name__ == "__main__":
    data = {"Records": [{"s3": {"object": {"key": "joblinksfile/2024-02-17"}}}]}
    lambda_handler(data, {})
