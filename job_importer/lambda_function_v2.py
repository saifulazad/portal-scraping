import os
import typesense
import boto3
import json
import pytz
import unicodedata
from datetime import timedelta , datetime
from dateutil import parser


# Initialize Typesense client
client = typesense.Client(
    {
        "api_key": os.environ["TYPESENSE_API_KEY"],
        "nodes": [
            {"host": "typesense.fractalslab.com", "port": "443", "protocol": "https"}
        ],
        "connection_timeout_seconds": 2,
    }
)

# Initialize AWS resources
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('extractor-service-dev')

# Define your local timezone
local = pytz.timezone("Asia/Dhaka")

def filter_json_data(data):
    """
    Filter the loaded JSON data and return a dictionary with selected fields.

    Parameters:
        data (dict): The loaded JSON data.

    Returns:
        dict: A dictionary containing selected fields from the JSON data.

    Raises:
        ValueError: If the JSON data is not loaded or is missing required fields.
    """
    if not data:
        raise ValueError("JSON data not loaded")

    # Directly map fields from the provided structure
    values = {
        "id": data.get("id", ""),
        "company_name": unicodedata.normalize("NFKD", data.get("company_name", "")),
        "job_title": unicodedata.normalize("NFKD", data.get("job_title", "")),
        "working_model": unicodedata.normalize("NFKD", data.get("working_model", "")),
        "job_type": unicodedata.normalize("NFKD", data.get("job_type", "")),
        "required_experience": unicodedata.normalize("NFKD", data.get("required_experience", "")),
        "location": unicodedata.normalize("NFKD", data.get("location", "")),
        "salary": unicodedata.normalize("NFKD", data.get("salary", "")),
        "apply_procedure": unicodedata.normalize("NFKD", data.get("how_to_apply", "")),
        "job_requirement": unicodedata.normalize("NFKD", data.get("job_requirement", "")),
        "job_responsibilities": unicodedata.normalize("NFKD", data.get("job_responsibilities", "")),
        "benefits": unicodedata.normalize("NFKD", data.get("benefits", "")),
        "about_company": unicodedata.normalize("NFKD", data.get("about_company", "")),
        "post_link": unicodedata.normalize("NFKD", data.get("post_link", "")),
    }

    # Parse the post_date using the datetime module
    post_date = data.get("post_date", "")
    if post_date:
        try:
            # Since post_date is in "%Y-%m-%dT%H:%M:%S.%fZ" format, use strptime
            datetime_object = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            
            # Convert to local timezone and then to UTC
            local_dt = local.localize(datetime_object, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            values["post_created_at"] = int(utc_dt.timestamp())
        except ValueError:
            values["post_created_at"] = None
    else:
        # Handle case where post_date is missing
        values["post_created_at"] = None

    # Meta data
    values["meta"] = {
        "document_id": data.get("id", ""),
        "document_created_at": post_date if post_date else "N/A"
    }

    return values

def transform_jobs(prefix):
    """
    Transform and filter all JSON files in the specified S3 folder.

    Parameters:
        prefix (str): The S3 folder path prefix.

    Returns:
        list: A list of transformed job data dictionaries.
    """
    new_jobs = []
    objs = my_bucket.objects.filter(Prefix=prefix)
    files = [obj.key for obj in sorted(objs, key=lambda x: x.last_modified, reverse=True)]

    for file_key in files[:-1]:
        obj = s3.Object(bucket_name='extractor-service-dev', key=file_key)
        body = obj.get()['Body'].read()
        # Use utf-8-sig to handle BOM
        pythonObject = json.loads(body.decode('utf-8-sig'))
        job_data = filter_json_data(pythonObject)
        new_jobs.append(job_data)

    return new_jobs

def jobs_import(prefix):
    """
    Import jobs from the specified S3 folder into Typesense.

    Parameters:
        prefix (str): The S3 folder path prefix.

    Returns:
        dict: The result of the Typesense import operation.
    """
    new_jobs = transform_jobs(prefix)
    import_results = []
    if len(new_jobs):
        import_results = client.collections["jobs"].documents.import_(
            new_jobs, {"action": "upsert", "return_id": True}
        )
    return import_results

def lambda_handler(event, context):
    current_date = datetime.now()
    # Specify the folder path prefix
    prefix = (current_date - timedelta(minutes=5)).strftime("jobs/%y/%m/%d")
    print(prefix)
    # Import jobs from S3 and insert into Typesense
    data = jobs_import(prefix)

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
if __name__ == "__main__":
    lambda_handler({}, {})
