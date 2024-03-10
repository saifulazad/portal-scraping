from settings import BUCKET_NAME
import typesense
import os
import unicodedata
import pytz
import json
import boto3
from datetime import datetime
import datetime

current_date = datetime.datetime.now()
s3 = boto3.resource('s3')

client = typesense.Client({
    'api_key': os.environ['TYPESENSE_API_KEY'],
    'nodes': [{
        'host': 'typesense.fractalslab.com',
        'port': '443',
        'protocol': 'https'
    }],
    'connection_timeout_seconds': 2
})

local = pytz.timezone("Asia/Dhaka")


# Load JSON data from file
def load_json_data(json_file):
    with open(json_file) as f:
        return json.load(f)


# Filter JSON data and extract relevant fields
def filter_json_data(data):
    if not data:
        raise ValueError("JSON data not loaded")

    mapping = {
        "Company name": "company_name",
        "Job title": "job_title",
        "Working model": "working_model",
        "Job Type": "job_type",
        "Required Experience": "required_experience",
        "Location": "location",
        "Salary": "salary",
        "How to apply?": "apply_procedure",
        "Job Requirement": "job_requirement",
        "Job Responsibilities": "job_responsibilities",
        "Benefits": "benefits",
        "About Company": "about_company",
        "Post link": "post_link",
    }

    result = {}
    for field in data["fields"]:
        field_label = field["label"].strip()
        if field["type"] == "DROPDOWN":
            value_id = field["value"][0]
            options = field["options"]
            option_text = next(
                (option["text"] for option in options if option["id"] == value_id), None
            )
            if option_text is not None:
                result[field_label] = option_text
        else:
            value = field["value"]
            result[field_label] = value

    values = {}
    for key, value in mapping.items():
        res = result.get(key)
        values[value] = unicodedata.normalize("NFKD", res) if res else ''

    datetime_str = "{} {}".format(result["Post Date"], result["Time"])
    datetime_object = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    local_dt = local.localize(datetime_object, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    values["id"] = data["responseId"]
    values["post_created_at"] = int(utc_dt.timestamp())
    meta = {"document_id": data["responseId"], "document_created_at": data["createdAt"]}
    values["meta"] = meta

    # Ensure certain fields are not None
    for key in ("job_requirement", "job_responsibilities", "location", "benefits", "about_company"):
        if values[key] is None:
            values[key] = ""

    return values


def transform_job(prefix):
    new_jobs = []
    bucket = s3.Bucket(BUCKET_NAME)
    objs = bucket.objects.filter(Prefix=prefix)
    files = [obj.key for obj in sorted(objs, key=lambda x: x.last_modified, reverse=True)]

    for file in files:
        obj = s3.Object(bucket_name=BUCKET_NAME, key=file)
        body = obj.get()['Body'].read()
        python_object = json.loads(body.decode('utf-8'))
        job_data = filter_json_data(python_object)
        new_jobs.append(job_data)

    return new_jobs


def save_job_ids(ids):
    prefix = current_date.strftime("jobs-id/%y/%m/%d")
    job_id = []
    for id in ids:
        job_id.append(id["id"])
    s3.Object(BUCKET_NAME, prefix).put(Body=','.join(job_id))


def lambda_handler(event, context):
    prefix = current_date.strftime("jobs-post/%y/%m/%d")
    new_jobs = transform_job(prefix)
    import_results = []

    if new_jobs:
        import_results = client.collections["jobs"].documents.import_(
            new_jobs, {"action": "upsert", "return_id": True}
        )
    save_job_ids(import_results)
    return import_results


if __name__ == "__main__":
    lambda_handler({}, {})
