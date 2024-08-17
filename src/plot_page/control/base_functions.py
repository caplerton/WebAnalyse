"""Functions for basic python actions."""

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
