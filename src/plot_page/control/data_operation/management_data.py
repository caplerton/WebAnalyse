"""Functions for operations on data."""

import base64
import json

import pandas as pd


from plot_page.control.data_operation.modify_data import flatten_dictionary
from plot_page.data.panda_data import store_dataframe


#####################################################################################################################################################
def add_dataset(table_data: dict, add_data: list[dict], name_dataset: str) -> dict:
    """Add a new dataset.

    Args:
        table_data (dict): Dictionary of key and dataset.
        add_data (list[dict]): The value that should be added.
        name_dataset (str): Name of the dataset.

    Returns:
        dict: Updated dictionary.
    """
    if add_data is None or name_dataset is None:
        return None
    if table_data is None:
        table_data = {}
    current_dataframe = pd.DataFrame.from_dict(add_data)
    store_dataframe(current_dataframe, name_dataset)
    table_data[name_dataset] = list(current_dataframe.columns)
    return table_data


#####################################################################################################################################################
def prepare_json(contents: str) -> dict[str, list[dict]]:
    """Prepare uploaded json-file.

    Args:
        contents (str): The file content as str.

    Returns:
        dict[str, list[dict]]: File content that has been converted to the table structure.
    """
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return {key: val for key, val in json.loads(decoded).items() if val and isinstance(val, list) and isinstance(val[0], dict)}


#####################################################################################################################################################
def prepare_upload_data(contents: list[str] | None, filenames: list[str], store_data: None | dict[str, dict]) -> dict[str, dict]:
    """Prepare uploaded data and return it as dict.

    Args:
        contents (str): The uploaded file content.
        filenames (str): Name of the uploaded file.
        store_data (None | dict[str, dict]): The current stored data.

    Returns:
        dict[str, dict]: The new data to store.
    """

    if contents is None or filenames is None:
        return store_data

    new_data: dict[str, pd.DataFrame] = {}
    for uploaded_data in zip(filenames, contents):
        if uploaded_data[0].endswith(".json"):
            json_data = prepare_json(uploaded_data[1])
            if all(isinstance(values, list) for values in json_data.values()):
                for key, val in json_data.items():
                    new_data[key] = pd.DataFrame.from_dict([flatten_dictionary(v) for v in val])

    for key, val in new_data.items():
        store_dataframe(val, key)
        store_data[key] = list(val.columns)

    return store_data
