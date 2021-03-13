import time
import requests
from mapper.maper import Mapper
import logging

logger = logging.getLogger(__name__)

def fetch_page(url):
    r = requests.get(url)
    return r.text


def get_all_job_details(job_links):
    url_list = []
    jobs_details = []
    for job_link in job_links:
        url = 'https://jobs.bdjobs.com/{}'.format(job_link)
        url_list.append(url)
    for url in url_list:
        try:
            body = {}
            page = fetch_page(url)
            logger.error(url)
            ob = Mapper(page=page)
            body = ob._read_from_HTML()
            # print(body)

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


def read_jobs_links(filename):
    """

    :param filename:
    :return:
    """
    file = open(filename, 'r')
    return [line.strip() for line in file.readlines()]
