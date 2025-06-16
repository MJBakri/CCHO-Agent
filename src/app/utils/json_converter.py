import json
from bson import json_util


def dict_bson_to_json(data: dict):
    """
    Converts a dictionary with BSON types to a JSON string.
    Args:
        data (dict): The dictionary to convert.
    Returns:
        str: The JSON string representation of the dictionary.
    """
    return json.loads(json_util.dumps(data),)