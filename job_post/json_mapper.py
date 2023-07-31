import argparse
import json

def load_json_data(json_file):
    """
    Load JSON data from the input file.

    Parameters:
        json_file (str): The path to the input JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(json_file) as f:
        return json.load(f)

def filter_json_data(data):
    """
    Filter the loaded JSON data and return a dictionary with selected fields.

    Parameters:
        data (dict): The loaded JSON data.

    Returns:
        dict: A dictionary containing selected fields from the JSON data.

    Raises:
        ValueError: If the JSON data is not loaded.
    """
    if not data:
        raise ValueError("JSON data not loaded")

    result = {}
    for field in data["fields"]:
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
    parser.add_argument("json_file", help="Path to the input JSON file", type=argparse.FileType('r'))

    args = parser.parse_args()

    data = load_json_data(args.json_file.name)
    json_data = filter_json_data(data)

    # Get the output file path by adding "_output" before the file extension
    output_file_path = args.json_file.name.replace(".json", "_output.json")

    with open(output_file_path, 'w') as output_file:
        json.dump(json_data, output_file, indent=2)