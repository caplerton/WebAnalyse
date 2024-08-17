"""Functions for operations on data."""

import base64
import json

import pandas as pd

from plot_page.control.data_analyse.notlinear_function import (
    linear_model,
    quadratic_model,
    exponential_model,
    logarithmic_model,
    power_model,
    sinus_model,
    gaussian_model,
    polynomial3_model,
    polynomial4_model,
    polynomial5_model,
)
from scipy.optimize import curve_fit


from plot_page.data.panda_data import load_dataframe


#####################################################################################################################################################
def query_table(selected_table: str, queries: list[str]) -> pd.DataFrame:
    """Aplly query on the current data.

    Args:
        selected_table (str): The name of the selected dataframe.
        queries (list[str]): The query that should be applied on the dataframe.

    Returns:
        pd.DataFrame: The resulting dataframe
    """
    data_table = load_dataframe(selected_table)
    for query in queries:
        try:
            tmp_result = data_table.query(query)
            data_table = tmp_result
        except Exception:
            pass
    return data_table


#####################################################################################################################################################
def get_intersections_dict(selected_tables: list[str], table_data: dict) -> list[str]:
    """Get list of str that are common in all selected tables.

    Args:
        selected_tables (list[str]): A list of selected table.
        table_data (dict): The current stored information to all dataframes.

    Returns:
        list[str]: List of attributes that are common in all dataframes.
    """
    if selected_tables is None or selected_tables == []:
        return []
    if not all(filename in table_data for filename in selected_tables):
        return []

    possible_keys = [table_data[filename] for filename in selected_tables]
    if len(possible_keys) == 1:
        return possible_keys[0]
    return list(set(possible_keys[0]).intersection(*possible_keys[1:]))


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
def calculate_correlation(selected_data: pd.DataFrame, main_attribute: str, second_attributes: list[str]) -> dict[str, float]:
    """Calculate the correlation factor.

    Args:
        selected_data (pd.DataFrame): The selected data.
        main_attribute (str): The primary attribute.
        second_attributes (list[str]): List of second attribute.

    Returns:
        dict[str, float]: The resulting correlation coefficients between primary and secondary attributes.
    """
    res = {}
    for second_attribute in second_attributes:
        try:
            res[second_attribute] = selected_data[main_attribute].corr(selected_data[second_attribute])
        except Exception:
            continue
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


#####################################################################################################################################################
def calculate_notlinear_regression(
    selected_data: pd.DataFrame, main_attr: str, second_attr: str, selected_func: str
) -> tuple[tuple[float], float, callable]:
    """Calculate the nonlinear regression between two attributes.

    Args:
        selected_data (pd.DataFrame): The selected dataframe.
        main_attr (str): The primary attribute.
        second_attr (str): The secondary attibute.
        selected_func (str): The selected function that should be looked at for the data.

    Returns:
        tuple[tuple[float], float, callable]: The resulting factor, the coverage and the callable for the selected function.
    """
    select_data = {
        "linear": (linear_model, (1, 1), "{} * x + {}"),
        "quadratic": (quadratic_model, (1, 1, 1), "{} * x**2 + {} * x + {}"),
        "exponential": (exponential_model, (1, 1, 1), "{} * e ** ({} * x) + {}"),
        "logarithmic": (logarithmic_model, (1, 1, 1), "{} * log({} * x) + {}"),
        "power": (power_model, (1, 1, 1), "{} * x**{} + {}"),
        "sinus": (sinus_model, (1, 1, 1), "{} * sin({} * x + {})"),
        "gaussian": (gaussian_model, (1, 1, 1, 1), " {} * e ** (-((x - {}) ** 2) / (2 * (**2)) + {} "),
        "polynomial3": (polynomial3_model, (1, 1, 1, 1), "{} * x**3 + {} * x**2 + {} * x + {}"),
        "polynomial4": (polynomial4_model, (1, 1, 1, 1, 1), "{} * x**4 + {} * x**3 + {} * x**2 + {} * x + {}"),
        "polynomial5": (polynomial5_model, (1, 1, 1, 1, 1, 1), "{} * x**5 + {} * x**4 + {} * x**3 + {} * x**2 + {} * x + {}"),
    }
    model_func, optimization_tuple, res_string = select_data[selected_func]

    popt, pcov = curve_fit(model_func, selected_data[second_attr], selected_data[main_attr], p0=optimization_tuple)
    return popt, pcov, res_string, model_func
