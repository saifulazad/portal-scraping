import boto3
import datetime
from s3.utils import upload_jobs_details
from bulk_job_processor import get_all_job_details, create_absolute_url
import smart_open

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    file_obj = event["Records"][0]

    filename = str(file_obj['s3']['object']['key'])
    job_links = [line.strip().decode("utf-8") for line in smart_open.smart_open(f's3://jobstext-v2/{filename}')]

    absolute_job_urls = [create_absolute_url(line) for line in job_links]

    jobs_details = get_all_job_details(absolute_job_urls)
    key = datetime.datetime.now().strftime('%d-%m-%y')
    file_name = f'{key}.json'
    upload_jobs_details(key=file_name, content=jobs_details)


if __name__ == '__main__':
    data = {
        'Records': [
            {
                's3': {
                    'object': {'key': 'joblinksfile/2021-03-13'}
                }
            }
        ]
    }
    lambda_handler(data, {})
