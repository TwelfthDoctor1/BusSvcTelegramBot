import json


def json_dump(json_dict: dict):
    """
    Function to convert Python Dictionary into JSON.
    :param json_dict: Dictionary to be converted into JSON format.
    :return:
    """
    return json.dumps(json_dict, sort_keys=True, indent=4)


def json_load(json_data: [str, bytes]):
    """
    Function to convert JSON into Python Dictionary.
    :param json_data: JSON data to be converted into Dictionary format.
    :return:
    """
    return json.loads(json_data)
