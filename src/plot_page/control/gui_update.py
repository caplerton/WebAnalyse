import os
from typing import Any

from plot_page.control.data_operations import check_line_config
from plot_page.control.plot_functions import plot_data
import pandas as pd

from plot_page.data.global_variables import DATAFRAME_STORE


def add_plot_data(click_event: int, plot_type: str, val_type: str, group_attributes: list[str], selected_values: dict[str, Any]) -> dict[str, Any]:
    """Add plot data.

    Args:
        click_event (int): Check for a click event.
        plot_type (str): Visualization type of the data.
        val_type (str): Value type of the data.
        group_attributes (list[str]): Attributes that should be used to group the data.
        selected_values (dict[str, Any]): The current config.

    Returns:
        dict[str, Any]: The resulting
    """
    if click_event is None:
        return None
    if plot_type is None:
        return None
    if selected_values is None:
        selected_values = {}

    line_config = check_line_config(plot_type, val_type, group_attributes)
    if line_config is not None:
        return {"plot_data": selected_values.get("plot_data", []) + [line_config]}

    return None


def create_plot(
    plot_settings: list[dict],
    title: str | None,
    selected_tables: list[str],
    x_axis: str | None,
    y_axis: str | None,
    graph_type: str | None,
) -> list:
    if graph_type is None:
        return []
    if len(plot_settings) < 1:
        return []
    if title is None or x_axis is None or y_axis is None:
        return []

    data_to_plot = (
        [{key: pd.read_pickle(os.path.join(DATAFRAME_STORE, f"{key}.pkl")) for key in selected_tables}]
        if graph_type == "Combined Graphs"
        else [{key: pd.read_pickle(os.path.join(DATAFRAME_STORE, f"{key}.pkl"))} for key in selected_tables]
    )
    return [plot_data(data, plot_settings, title, x_axis, y_axis) for data in data_to_plot]


def grouping_options(value_type: str, attributes: list[str]) -> list[str]:
    """Update grouping option.

    Args:
        value_type (str): The current selected value type.
        attributes (list[str]): Possible attributes that can be selected for grouping.

    Returns:
        list[str]: List of selectable grouping attributes.
    """
    return attributes if value_type in ["History", "Min", "Max", "Median", "Mean"] else []
