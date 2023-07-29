import datetime
import json
import boto3
def upload_jobs_details(key, content, bucket_name):
    """

    :param bucket_name:
    :param key:
    :param content:
    :return:
    """
    s3 = boto3.resource("s3")
    key = "jobs-post/" + key

    try:
        data = json.dumps(content).encode("utf-8")
        s3_response = s3.Object(bucket_name, key).put(Body=data)
        print(s3_response)
    except Exception as e:
        raise IOError(e)


def lambda_handler(event, context):
    
    key = datetime.datetime.now().strftime("%d-%m-%y")
    payload = (json.loads(event['body'])['data'])
    key = payload['submissionId']
    file_name = f"{key}.json"
    
    upload_jobs_details(key= file_name, content=payload, bucket_name='extractor-service-dev')


if __name__ == "__main__":
    data = {"Records": [{"s3": {"object": {"key": "joblinksfile/2023-02-23"}}}]}
    lambda_handler(data, {})
