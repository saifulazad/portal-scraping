import boto3
import datetime
from s3.utils import upload_jobs_details
from bulk_job_processor import get_all_job_details


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    file_obj = event["Records"][0]

    filename = str(file_obj['s3']['object']['key'])
    data = s3.get_object(Bucket='jobstext-v2', Key=filename)
    contents = data['Body'].iter_lines()
    jobs_details = get_all_job_details(contents)
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
