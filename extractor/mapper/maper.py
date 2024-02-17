from bs4 import BeautifulSoup
import copy


class Mapper(object):
    def __init__(self, page):
        self.class_value_has_list = {
            "job_des": {"name": "Job Description / Responsibility", "descriptions": []},
            "job_req": {"name": "Job Requirements", "descriptions": []},
            "oth_ben": {"name": "Other Benefits", "descriptions": []},
            "addi_info": {"name": "Additional Information", "information": {}},
        }
        self.class_value_no_list = {
            "jtitle": {"name": "Job Title", "tag": "h2"},
            "cname": {"name": "Company Name", "tag": "h2"},
            "compinfo": {"name": "Company Information", "tag": "div"},
        }

        self.soup = BeautifulSoup(
            page, "html.parser"
        )  # Consume HTML page from requests library

    def _read_additional_info(self):
        panel_body = self.soup.find("div", {"class": "jobcontent"})
        data = {}
        divs = panel_body.find_all('div', class_='col-sm-12')
        for div in divs:
            heading = div.find('h5', class_='subheading')
            if heading:
                keys = heading.text.strip()
                items = div.find_all('li')
                data[keys] = items
        return data

    def _read_basic_info(self):
        class_value_no_list_cloned = copy.deepcopy(self.class_value_no_list)
        for key in class_value_no_list_cloned:
            information = self.soup.find(
                self.class_value_no_list[key]["tag"], attrs={"class": key}
            )
            class_value_no_list_cloned[key][
                "info"
            ] = information.text.strip()  # Store those as 'info' key
            del class_value_no_list_cloned[key]["tag"]
            del class_value_no_list_cloned[key]["name"]
        return class_value_no_list_cloned

    def _extract_key_value_pairs(self, ul_element):
        li_elements = ul_element.find_all('li')
        data = {}
        for li in li_elements:
            key = li.contents[0].strip(':').strip()
            value = li.find('span').text.strip()
            data[key[:len(key) - 1]] = value  # Remove the trailing colon
        return data

    def _extract_job_resp_benefits(self, information, class_value_has_list_cloned):
        keys = ["job_resp", "benefits"]
        for key in keys:
            try:
                job_info = information.select(f'div.col-sm-12 > h4#{key}')[0].parent
                h4_tag = job_info.find('h4', class_='sectxt')
                if 'job_resp' in h4_tag['id']:
                    self._extract_job_response(job_info, class_value_has_list_cloned)
                elif 'benefits' in h4_tag['id']:
                    self._extract_benefits(job_info, class_value_has_list_cloned)
            except:
                pass

    def _extract_job_response(self, job_info, class_value_has_list_cloned):
        if job_info.find('li'):
            for item in job_info.find_all(['li']):
                class_value_has_list_cloned['job_des']["descriptions"].append(
                    item.text.strip()
                )
        else:
            for item in job_info.find_all(['p']):
                class_value_has_list_cloned['job_des']["descriptions"].append(
                    item.text.strip()
                )

    def _extract_benefits(self, job_info, class_value_has_list_cloned):
        if job_info.find('li'):
            for item in job_info.find_all('li'):
                class_value_has_list_cloned['oth_ben']["descriptions"].append(
                    item.text.strip()
                )
        else:
            for item in job_info.find_all('p'):
                class_value_has_list_cloned['oth_ben']["descriptions"].append(
                    item.text.strip()
                )

    def _read_job_des_and_req(self):
        class_value_has_list_cloned = copy.deepcopy(self.class_value_has_list)

        additional_info = self._read_additional_info()
        items = additional_info['Additional Requirements']

        for item in items:
            class_value_has_list_cloned['job_req']["descriptions"].append(
                item.text.strip()
            )

        summery_items = self.soup.find(class_='summery__items')
        data = self._extract_key_value_pairs(summery_items)
        class_value_has_list_cloned["addi_info"]["information"].update(data)

        information = self.soup.find('div', class_='jobcontent')
        self._extract_job_resp_benefits(information, class_value_has_list_cloned)

        return class_value_has_list_cloned

    def _read_from_HTML(self, path=None):
        """
        This method to process whole job page. We are processing only 2 main parts of a page
        One is basic info and another is description and responsibilities
        Just call above 2 methods
        :param path:
        :return:
        """

        all_list_info = self._read_job_des_and_req()

        basic_info_list = self._read_basic_info()
        print(all_list_info)
        return {**all_list_info, **basic_info_list}
