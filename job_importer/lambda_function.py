import datetime
import json
import boto3
import os
import googlemaps


# address


def find_location(address):
    # API key is passed as an environment variable in the Lambda function
    api_key = os.environ["GOOGLE_MAP_API_KEY"]
    gmaps = googlemaps.Client(key=api_key)

    # Geocoding an address
    geocode_result = gmaps.geocode(address)

    # Return the result as JSON
    return geocode_result


def get_address(fields):
    for field in fields:
        if field["label"] == "Location":
            return field["value"] or ""
    return ""


def upload_jobs_details(key, content, bucket_name):
    """

    :param bucket_name:
    :param key:
    :param content:
    :return:
    """
    s3 = boto3.resource("s3")
    key = "jobs-post/" + key
    address_as_text = get_address(content["fields"])
    if address_as_text:
        content["address"] = find_location(address_as_text)
    else:
        content["address"] = []

    data = json.dumps(content).encode("utf-8")

    s3_response = s3.Object(bucket_name, key).put(Body=data)
    print(s3_response)


def lambda_handler(event, context):
    prefix = datetime.datetime.now().strftime("%y/%m/%d")
    payload = json.loads(event["body"])["data"]
    key = payload["submissionId"]
    file_name = f"{prefix}/{key}.json"
    upload_jobs_details(
        key=file_name, content=payload, bucket_name="extractor-service-dev"
    )


if __name__ == "__main__":
    data = {"Records": [{"s3": {"object": {"key": "joblinksfile/2023-02-23"}}}]}
    lambda_handler(data, {})
