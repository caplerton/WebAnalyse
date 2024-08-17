"""Functions the evaluates GUI inputs and return the results."""

from typing import Any


from plot_page.control.data_operation.extract_information import calculate_correlation, calculate_notlinear_regression, check_line_config, query_table
from plot_page.control.visualisation.plot_function import plot_2d_data, plot_correlation_coefficient, plot_notlinear_regression
from plot_page.data.panda_data import load_dataframe, store_dataframe


#####################################################################################################################################################
def add_plot_data(
    click_event: int | None, plot_type: str | None, val_type: str, group_attributes: list[str], selected_values: dict[str, Any] | None
) -> dict[str, Any]:
    """Add plot data.

    Args:
        click_event (int | None): Check for a click event.
        plot_type (str | None): Visualization type of the data.
        val_type (str): Value type of the data.
        group_attributes (list[str]): Attributes that should be used to group the data.
        selected_values (dict[str, Any] | None): The current config.

    Returns:
        dict[str, Any]: The created plot settings config.
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


#####################################################################################################################################################
def create_2dplot(
    plot_settings: list[dict],
    title: str | None,
    selected_tables: list[str],
    x_axis: str | None,
    y_axis: str | None,
    graph_type: str | None,
) -> list:
    """Create a 2d plot with the current settings.

    Args:
        plot_settings (list[dict]): The current plot settings.
        title (str | None): Title of the plot.
        selected_tables (list[str]): List of selected dataframes that should be plotted.
        x_axis (str | None): Selected attribute for the x_axis.
        y_axis (str | None): Selected attribute for the y_axis.
        graph_type (str | None): The graph type.

    Returns:
        list: List of html componets that contains all plots.
    """
    if graph_type is None:
        return []
    if len(plot_settings) < 1:
        return []
    if title is None or x_axis is None or y_axis is None:
        return []

    data_to_plot = (
        [{key: load_dataframe(key) for key in selected_tables}]
        if graph_type == "Combined Graphs"
        else [{key: load_dataframe(key)} for key in selected_tables]
    )

    return [plot_2d_data(data, plot_settings, title, x_axis, y_axis) for data in data_to_plot]


#####################################################################################################################################################
def correlation_evaluation(selected_table: str | None, main_attribute: str | None, second_attributes: list[str] | None) -> list:
    """Evaluate the correlation coefficient.

    Args:
        selected_table (str | None): Name of the selected table.
        main_attribute (str | None): The primary attribute.
        second_attributes (list[str] | None): A list of secondary attributes.

    Returns:
        list: HTML components that show result of the corellation evaluation.
    """
    if selected_table is None:
        return []
    if main_attribute is None:
        return []
    if second_attributes is None or len(second_attributes) < 1:
        return []

    loaded_selected_table = load_dataframe(selected_table)
    correlation_coefficient = calculate_correlation(loaded_selected_table, main_attribute, second_attributes)
    return [plot_correlation_coefficient(loaded_selected_table, main_attribute, key, factor) for key, factor in correlation_coefficient.items()]


#####################################################################################################################################################
def notlinear_regression_evaluation(
    selected_table: str | None, main_attribute: str | None, second_attribute: str | None, selected_function: str | None
) -> list:
    """Evaluate the notlinear regression for the current dataframe.

    Args:
        selected_table (str | None): The name of selected table that should be be evaluated.
        main_attribute (str | None): The primary attribute.
        second_attribute (str | None): The secondary attribute.
        selected_function (str | None): Identifier for the function that should be used to fit the data.

    Returns:
        list: List of the result as html compnents.
    """
    if selected_table is None:
        return []
    if main_attribute is None:
        return []
    if second_attribute is None:
        return []
    if selected_function is None:
        return []

    loaded_selected_table = load_dataframe(selected_table)
    popt, pcov, res_string, model_func = calculate_notlinear_regression(loaded_selected_table, main_attribute, second_attribute, selected_function)
    return plot_notlinear_regression(loaded_selected_table, main_attribute, second_attribute, popt, pcov, res_string, model_func)


#####################################################################################################################################################
def plot2d_generate_additional_plot_setting(
    n_clicks: int | None,
    plot_type: str | None,
    value_type: str | None,
    group_by: list[str],
    mode_selector: str | None,
    current_plot_settings: list[dict],
) -> list[dict]:
    """Add additrional plot setting.

    Args:
        n_clicks (int | None): Click event value.
        plot_type (str | None): Type of the plot.
        value_type (str | None): Plot the selected value.
        group_by (list[str]): Group dataset by the selected attributes.
        mode_selector (str | None): The selected plot mode.
        current_plot_settings (list[dict]): The already existing plot setting.

    Returns:
        list[dict]: The updated plot_setting.
    """
    if not n_clicks:
        return None
    if plot_type not in ["Line", "Bar"]:
        return None
    if not (
        plot_type == "Line"
        and value_type in ["History", "Min", "Max", "Median", "Mean"]
        or plot_type == "Bar"
        and value_type in ["Min", "Max", "Median", "Mean"]
    ):
        return None
    plot_id = 0 if len(current_plot_settings) == 0 else max(v["id"] for v in current_plot_settings) + 1
    current_plot_settings.append({"id": plot_id, "type": plot_type, "value": value_type, "group_attributes": group_by, "mode": mode_selector})
    return current_plot_settings


####################################################################################################################################################
def upload_create_filtered_dataset(
    n_clicks: int | None, selected_table: str | None, table_name: str | None, query_list: list[str], table_data: dict[str, list]
) -> tuple[dict[str, list], str]:
    """Save the modified dataset.

    Args:
        n_clicks (int | None): Execute this function when click event happens.
        selected_table (str | None): The current selected data.
        table_name (str | None): The name for the new dataset.
        query_list (list[str]): List of queries that where executed on the dataset.
        table_data (dict[str, list]): The existing dict of dataset.

    Returns:
        tuple[dict[str, list], str]: The updated dictionary of dataset and default value for input component.
    """
    if n_clicks is None:
        return None, None
    if selected_table is None:
        return None, None
    if table_name is None or len(table_name) < 1:
        return None, None

    res_dataframe = query_table(selected_table, query_list)
    store_dataframe(res_dataframe, table_name)
    table_data[table_name] = list(res_dataframe.columns)
    return table_data, ""
