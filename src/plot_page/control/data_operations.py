"""Functions for operations on data."""

import base64
import json

import pandas as pd


#####################################################################################################################################################
def filter_columns(selected_data: dict[str, list[dict]]) -> list[str]:
    """Filter common keys of all selected tables.

    Args:
        selected_data (dict[str, list[dict]]): The selected data that should be used.

    Returns:
        list[str]: List of common keys between all tables.
    """
    if selected_data is None or len(selected_data) < 1:
        return []
    if any(len(val) < 1 for val in selected_data.values()):
        return []
    possible_keys = [list(val[0]) for val in selected_data.values()]
    if len(possible_keys) == 1:
        return possible_keys[0]
    return list(set(possible_keys[0]).intersection(*possible_keys[1:]))


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
    table_data[name_dataset] = add_data
    return table_data


#####################################################################################################################################################
def convert_uploaded_data(file_name: str, file_structure: str, store_data: dict, table_data: list) -> dict:
    """Convert uploaded data to format that can be used.

    Args:
        file_name (str): Name of the uploaded file.
        file_structure (str): The structure of the uploaded data.
        store_data (dict): Dictionary of the stored data.
        table_data (list): U

    Returns:
        dict: _description_
    """
    if not table_data:
        table_data = {}

    if file_name is None or file_structure is None:
        return None

    try:
        if "{'id': dict}" == file_structure:
            table_data[file_name] = [{"id": key} | val for key, val in store_data[file_name].items()]

        if "{'table1': [dict]}" == file_structure:
            for key, val in store_data[file_name].items():
                table_data[key] = val
    except Exception:
        return None

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
def prepare_upload_data(uploaded_data: tuple[str, str], store_data: None | dict[str, dict]) -> dict[str, dict]:
    """Prepare uploaded data and return it as dict.

    Args:
        contents (str): The uploaded file content.
        filenames (str): Name of the uploaded file.
        store_data (None | dict[str, dict]): The current stored data.

    Returns:
        dict[str, dict]: The new data to store.
    """
    if store_data is None:
        store_data = {}

    if uploaded_data[0].endswith(".json"):
        store_data.update(prepare_json(uploaded_data[1]))

    return store_data


#####################################################################################################################################################
def grouping_pd(group: str, data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Group the dataframe by the attribute values.

    Args:
        group (str): Attribute name the data should be grouped with.
        data (dict[str, pd.DataFrame]): The already grouped dataframes.

    Returns:
        dict[str, pd.DataFrame]: The new grouped dataframe.
    """
    groups = list(set(data[list(data.keys())[0]][group].tolist()))
    return {f"{key}_{attribute}": val[getattr(val, group) == attribute] for key, val in data.items() for attribute in groups}


#####################################################################################################################################################
def split_data(data: dict, grouping: list[str]) -> dict:
    """Split dictionary of data in groups.

    Args:
        data (dict): The dictionary that contaisn the data.
        grouping (list[str]): List of attributes the data should be grouped.

    Returns:
        dict: The resulting splitted dataset.
    """
    res = {key: pd.DataFrame.from_dict(val) for key, val in data.items()}

    if grouping is None:
        return res

    for g in grouping:
        res = grouping_pd(g, res)

    return res


#####################################################################################################################################################
def check_line_config(plot_type: str, value_to_plot: str, group_by: list[str]) -> dict:
    """Check if the line configuration is ok.

    Args:
        plot_type (str): The type that should be plotted.
        value_to_plot (str): Extended information about what should be plotted.
        group_by (list[str]): List of attributes the data should be grouped by.

    Returns:
        dict: Dictionary that contains all informations
    """
    if plot_type is None:
        return None
    if value_to_plot is None:
        return None

    return {"type": plot_type, "plot_kind": value_to_plot, "group_attributes": group_by}
