import os
import boto3
import json
from settings import BUCKET_NAME


def upload_jobs_details(key, content):
    """

    :param key:
    :param content:
    :return:
    """
    s3 = boto3.resource('s3')
    key = os.path.join('jobs-details', key)

    try:
        data = json.dumps(content).encode('utf-8')
        s3_response = s3.Object(BUCKET_NAME, key).put(Body=data)
    except Exception as e:
        raise IOError(e)


if __name__ == '__main__':
    upload_jobs_details('aaa.json', {'data': [312, 13, 212]})
