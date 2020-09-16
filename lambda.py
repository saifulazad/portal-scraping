import boto3
import requests
import time
import datetime
from s3.utils import upload_jobs_details
from mapper.maper import Mapper


def fetch_page(url):
    r = requests.get(url)
    return r.text


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    file_obj = event["Records"][0]

    filename = str(file_obj['s3']['object']['key'])
    data = s3.get_object(Bucket='jobstext-v2', Key=filename)
    contents = data['Body'].iter_lines()

    url_list = []
    jobs_details = []
    for x in contents:
        url = f'https://jobs.bdjobs.com/{x.decode("utf-8")}'
        url_list.append(url)
    for url in url_list:

        try:
            body = {}
            page = fetch_page(url)
            # print(url)
            ob = Mapper(page=page)
            body = ob._read_from_HTML()
            print(body)

        except Exception as ex:

            body = {'error': str(ex)}

        finally:
            keys = {
                'url': url,
                'created_at': int(time.time())
            }
            data = {**body, **keys}
            jobs_details.append(data)
    key = datetime.datetime.now().strftime('%d-%m-%y')
    file_name = f'{key}.json'
    upload_jobs_details(key=file_name, content=jobs_details)


if __name__ == '__main__':
    data = {
        'Records': [
            {
                's3': {
                    'object': {'key': 'joblinksfile/2020-09-15'}
                }
            }
        ]
    }
    lambda_handler(data, {})
