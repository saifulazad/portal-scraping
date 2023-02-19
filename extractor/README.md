### Extractor

[//]: # (![Diagram]&#40;https://github.com/saifulazad/portal-scraping/blob/mamun_wip/extractor/map.jpeg?raw=true "Title"&#41;)

#### Lambda Functions

``lambda_function.py`` is triggered when an object is created in an S3 bucket. 
It reads the content of the uploaded file and extracts job links from it. 
Then it creates absolute job URLs using a function named ``create_absolute_url`` and fetches 
job details for each URL using ``get_all_job_details`` function from ``bulk_job_processor`` 
module. 

Finally, it creates job details as a JSON file.
The file is uploaded to the same S3 bucket using the ``upload_jobs_details`` function from the
``s3.utils`` module.
