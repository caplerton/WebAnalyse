"""Functions for operations on data."""

from typing import Any


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


def flatten_dictionary(current_dictionary: dict[str, Any], parent_key: str | None = None) -> dict[str, Any]:
    res = {}
    for key, val in current_dictionary.items():
        new_key = f"{parent_key}_key" if parent_key is not None else key
        if isinstance(val, dict):
            res = res | flatten_dictionary(val, new_key)
        else:
            res[new_key] = val
    return res


#####################################################################################################################################################
def split_data(data: dict, grouping: list[str] | None) -> dict:
    """Split dictionary of data in groups.

    Args:
        data (dict): The dictionary that contaisn the data.
        grouping (list[str] | None): List of attributes the data should be grouped.

    Returns:
        dict: The resulting splitted dataset.
    """
    res = data
    if grouping is None:
        return res

    for group in grouping:
        try:
            group_values = list(set(res[list(res.keys())[0]][group].tolist()))
            res = {f"{key}_{attribute}": val[getattr(val, group_values) == attribute] for key, val in res.items() for attribute in group_values}
        except Exception:
            pass

    return res


#####################################################################################################################################################
def dictionary_values_to_string(input_dict: dict[str, Any]) -> list[dict[str, str]]:
    """Convert the values of dictionary to string.

    Args:
        input_dict (dict[str, Any]): The dictionary that should be transformed.

    Returns:
        list[dict[str, str]]: The resulting List of dictionary values.
    """
    return [{key: str(val) for key, val in dataset.items()} for dataset in input_dict]
