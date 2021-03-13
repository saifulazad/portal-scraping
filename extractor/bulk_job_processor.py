import time

import requests
from mapper.maper import Mapper


def fetch_page(url):
    r = requests.get(url)
    return r.text


def get_all_job_details(contents):
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
    return jobs_details
