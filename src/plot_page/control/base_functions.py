"""Functions for basic python actions."""

import base64
import json
import os


#####################################################################################################################################################
def read_json(json_path: str) -> dict:
    """Read json file.

    Args:
        json_path (str): Path to the json-File.

    Returns:
        dict: Json-File content as dictionary.
    """
    if not os.path.exists(json_path):
        return {}
    with open(json_path, mode="r", encoding="utf-8") as json_file:
        return json.load(json_file)


#####################################################################################################################################################
def write_json(json_path: str, data: dict) -> None:
    """Write dict as json-File.

    Args:
        json_path (str): JSON-File path to store json-File.
        data (dict): The data that should be stored.
    """
    with open(json_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file)


#####################################################################################################################################################
def parse_contents(contents: str, filename: str) -> dict[str, dict]:
    """Convert the uploaded file to a json Object.

    Args:
        contents (str): The content of the file.
        filename (str): The name of the file.

    Returns:
        dict[str, dict]: Dictionary with filename as key and content as dictionary.
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    if filename.__contains__(".json"):
        return {filename: json.loads(decoded)}
    return {}
