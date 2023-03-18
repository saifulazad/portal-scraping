from bs4 import BeautifulSoup
import copy


class Mapper(object):
    def __init__(self, page):
        self.class_value_has_list = {
            "job_des": {"name": "Job Description / Responsibility", "descriptions": []},
            "job_req": {"name": "Job Requirements", "descriptions": []},
            "oth_ben": {"name": "Other Benefits", "descriptions": []},
            "adi_info": {"name": "Additional Information", "information": []},
        }
        self.class_value_no_list = {
            "job-title": {"name": "Job Title", "tag": "h2"},
            "company-name": {"name": "Company Name", "tag": "h3"},
            "company-info": {"name": "Company Information", "tag": "div"},
        }

        self.soup = BeautifulSoup(
            page, "html.parser"
        )  # Consume HTML page from requests library

    def _read_additional_info(self):
        panel_body = self.soup.find("div", {"class": "panel-body"})
        h4_tags = panel_body.find_all("strong")
        data = []

        for h4 in h4_tags:
            tag = panel_body.find("strong", text=h4.text.strip())
            text = tag.next_sibling.strip()
            keys = h4.text.strip()
            data.append({keys[: len(keys) - 1]: text})

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

    def _read_job_des_and_req(self):

        class_value_has_list_cloned = copy.deepcopy(self.class_value_has_list)
        class_value_has_list_cloned["adi_info"]["information"].append(
            self._read_additional_info()
        )
        for key in class_value_has_list_cloned.keys():
            try:
                informations = self.soup.findAll("div", attrs={"class": key})
                for information in informations:
                    list_items = information.find("ul")

                    for list_item in list_items.findAll("li"):
                        class_value_has_list_cloned[key]["descriptions"].append(
                            list_item.text.strip()
                        )
            except:
                pass
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
        return {**all_list_info, **basic_info_list}
