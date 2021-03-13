import time
import requests
from mapper.maper import Mapper
import logging

logger = logging.getLogger(__name__)

BASE_URL = 'https://jobs.bdjobs.com/'


def fetch_page(url):
    r = requests.get(url)
    return r.text


def get_all_job_details(job_links):
    jobs_details = []
    for url in job_links:
        try:
            body = {}
            page = fetch_page(url)
            ob = Mapper(page=page)
            body = ob._read_from_HTML()

        except Exception as ex:

            body = {'error': str(ex)}

        finally:
            keys = {
                'url': url,
                'created_at': int(time.time())
            }
            data = {**body, **keys}
            logger.info(body)
            jobs_details.append(data)
    return jobs_details


def create_absolute_url(partial_url):
    return "{}{}".format(BASE_URL, partial_url)


def read_jobs_links(filename):
    """

    :param filename:
    :return:
    """
    file = open(filename, 'r')

    raw_list = [str(line.strip()) for line in file.readlines()]
    return [create_absolute_url(line) for line in raw_list]
