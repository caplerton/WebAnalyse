from typing import Any

from plot_page.control.data_operations import check_line_config
from plot_page.control.plot_functions import plot_data


def get_default_selected_values() -> dict[str, Any]:
    return {"plot_data": [], "x_axis": None, "y_axis": None, "multi": False}


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

    line_config = check_line_config(plot_type, val_type, group_attributes)
    if line_config is not None:
        return {"plot_data": selected_values.get("plot_data", []) + [line_config]}

    return None


def create_plot(plot_data_2d: list[dict], x_axis: str, y_axis: str, selected_tables: dict, use_multi_plot: list[bool]) -> list:
    """Create Plot of the selected table and configuration.

    Args:
        plot_data_2d (list[dict]): The current cofig table.
        x_axis (str): The selected attribute for the x_axis.
        y_axis (str): The selected attribute for the y_axis.
        selected_tables (dict): All selected table data.
        use_multi_plot (list[bool]): True if multiple plots should be created.

    Returns:
        list: List of dcc.Graphs that should be plotted.
    """
    if plot_data_2d is None or plot_data_2d == []:
        return None
    if selected_tables is None:
        return None
    if x_axis is None or y_axis is None:
        return None

    data_to_plot = [{key: val} for key, val in selected_tables.items()] if use_multi_plot == [] else [selected_tables]
    return [plot_data(data, plot_data_2d, x_axis, y_axis) for data in data_to_plot]


def grouping_options(value_type: str, attributes: list[str]) -> list[str]:
    """Update grouping option.

    Args:
        value_type (str): The current selected value type.
        attributes (list[str]): Possible attributes that can be selected for grouping.

    Returns:
        list[str]: List of selectable grouping attributes.
    """
    return attributes if value_type in ["History", "Min", "Max", "Median", "Mean"] else []
