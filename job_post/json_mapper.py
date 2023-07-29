import argparse
import json


class JSONMapper:
    """
        A class to handle loading and filtering data from a JSON file.

        Attributes:
            json_file (str): The path to the input JSON file.
            data (dict): The loaded JSON data.

        Methods:
            load_json_data(): Load JSON data from the input file and store it in the 'data' attribute.
            filter_json_data(): Filter the loaded JSON data and return a dictionary with selected fields.

        Example:
            # Create a JSONMapper instance and process the JSON data
            mapper = JSONMapper("input.json")
            mapper.load_json_data()
            result = mapper.filter_json_data()
    """

    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None

    def load_json_data(self):
        with open(self.json_file) as f:
            self.data = json.load(f)

    def filter_json_data(self):
        """
            Filter the loaded JSON data and return a dictionary with selected fields.

            Returns:
                dict: A dictionary containing selected fields from the JSON data.

            Raises:
                ValueError: If the JSON data is not loaded.
        """

        if not self.data:
            raise ValueError("JSON data not loaded")

        result = {}
        for field in self.data["fields"]:
            if field["type"] == "DROPDOWN":
                field_label = field["label"]
                value_id = field["value"][0]
                options = field["options"]
                option_text = next((option["text"] for option in options if option["id"] == value_id), None)
                if option_text is not None:
                    result.setdefault(field_label, []).append(option_text)
            else:
                label = field["label"]
                value = field["value"]
                result[label] = value
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSON Mapper")
    parser.add_argument("json_file", help="Path to the input JSON file")

    args = parser.parse_args()

    mapper = JSONMapper(args.json_file)
    mapper.load_json_data()
    merged_result = mapper.filter_json_data()
    print(json.dumps(merged_result, indent=2))
