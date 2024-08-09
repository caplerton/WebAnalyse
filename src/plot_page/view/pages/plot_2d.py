
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html
from dash.dependencies import Input, Output

from plot_page.app import app
from plot_page.control.data_operations import check_line_config, filter_columns
from plot_page.control.plot_functions import plot_data
from plot_page.view.components.default_component import get_upload_component


#####################################################################################################################################################
def graph_setting() -> dbc.Card:
    """Create graph setting card.

    Returns:
        dbc.Card: dbc.Card that lets the user configure settings for the plot.
    """
    return dbc.Card(
        [
            html.H1("Graph setting", style={"textAlign": "center"}),
            get_upload_component(),
            html.Div(dcc.Dropdown([], value=[], id="select_2d_table", multi=True, clearable=True), style={"padding": "10px"}),
            html.Div(
                [
                    html.H4("Table setting"),
                    dbc.Row(
                        [
                            dbc.Col(dbc.Label("x-Axis"), width=1),
                            dbc.Col(dcc.Dropdown([], id="x_axis"), width=2),
                            dbc.Col(dbc.Label("y-Axis"), width=1),
                            dbc.Col(dcc.Dropdown([], id="y_axis"), width=2),
                            dbc.Col(dcc.Checklist(id="multi_plots", options={"disabled": "Plot Per File"}, value=["disabled"]), width=2),
                        ]
                    ),
                    html.Div(id="2d-setting"),
                ],
                style={"padding": "10px"},
            ),
        ]
    )


#####################################################################################################################################################
@app.callback(
    Output("2d_plot_chart", "children"),
    Input("plot_config_table", "data"),
    State("x_axis", "value"),
    State("y_axis", "value"),
    State("selected_table_data", "data"),
    State("multi_plots", "value"),
)
def create_plot(plot_config_table: list[dict], x_axis: str, y_axis: str, data_table: dict, use_multi_plot: list[bool]) -> list:
    """Create Plot of the selected table and configuration.

    Args:
        plot_config_table (list[dict]): The current cofig table.
        x_axis (str): The selected attribute for the x_axis.
        y_axis (str): The selected attribute for the y_axis.
        data_table (dict): All selected table data.
        use_multi_plot (list[bool]): True if multiple plots should be created.

    Returns:
        list: List of dcc.Graphs that should be plotted.
    """
    if plot_config_table is None or x_axis is None or y_axis is None or data_table is None:
        return dash.no_update

    data_to_plot = [{key: val} for key, val in data_table.items()] if use_multi_plot == [] else [data_table]
    res = [plot_data(data, plot_config_table["settings"], x_axis, y_axis) for data in data_to_plot]
    return res


#####################################################################################################################################################
def plot_config() -> dbc.Card:
    """Create a card to config the plot.

    Returns:
        dbc.Card: The create card that lets the user decide what to plot.
    """
    return dbc.Card(
        [
            html.H1("Add Plot", style={"textAlign": "center"}),
            html.Div(dcc.Dropdown(["Line", "Bar"], placeholder="Set Plot Type", id="plot_type"), style={"padding": "10px"}),
            dbc.Row(
                [
                    dbc.Col(html.Div(dcc.Dropdown([], id="value_to_plot", style={"padding": "10px"})), width=3),
                    dbc.Col(
                        html.Div(dcc.Dropdown(placeholder="Group By", options=[], id="group_by", multi=True), style={"padding": "10px"}), width=3
                    ),
                ]
            ),
            html.Div(dbc.Button("Add Plot Config", id="add_plot_config"), style={"padding": "10px"}),
            html.Div(dash_table.DataTable(data=[], id="plot_settings", page_size=20), style={"padding": "10px"}),
        ]
    )


#####################################################################################################################################################
@app.callback(
    Output("plot_config_table", "data", allow_duplicate=True),
    Output("plot_type", "value"),
    Output("value_to_plot", "value"),
    Output("group_by", "value"),
    Input("add_plot_config", "n_clicks"),
    State("plot_type", "value"),
    State("value_to_plot", "value"),
    State("group_by", "value"),
    Input("plot_config_table", "data"),
    prevent_initial_call=True,
)
def update_plot_config(n_clicks: int, plot_type: str, value_to_plot: str, group_by: list[str], current_config: dict) -> dict:
    """Update the plot config.

    Args:
        n_clicks (int): Click event.
        plot_type (str): The type that should be plotted.
        value_to_plot (str): Value that should be plotted.
        group_by (list[str]): Group plot data by this attribute.
        current_config (dict): The current config.

    Returns:
        dict: The updated config.
    """
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    if current_config is None:
        current_config = {"settings": []}

    reset = False
    line_config = check_line_config(plot_type, value_to_plot, group_by)
    if line_config is not None:
        current_config["settings"].append(line_config)
        reset = True

    input_val = None if reset else dash.no_update
    return current_config, input_val, input_val, input_val


#####################################################################################################################################################
@app.callback(Output("plot_config_table", "data", allow_duplicate=True), Input("select_2d_table", "value"), prevent_initial_call=True)
def reset_table(current_table: dict) -> dict:
    """Reset the table.

    Args:
        current_table (dict): Data of the current table.

    Returns:
        dict: The initial config_table data.
    """
    if current_table is not None:
        return dash.no_update
    return {"settings": []}


#####################################################################################################################################################
@app.callback(Output("plot_settings", "data"), Input("plot_config_table", "data"))
def update_plot_settings(plot_config_table: dict) -> list:
    """Update the plot settings table.

    Args:
        plot_config_table (dict): The current added config.

    Returns:
        list: List of dictionary that contains the configuration.
    """
    if plot_config_table is None or len(plot_config_table.get("settings", [])) < 1:
        return []
    return [{key: str(val) for key, val in dataset.items()} for dataset in plot_config_table["settings"]]


#####################################################################################################################################################
def layout() -> html.Div:
    """The 2D-Plot layout.

    Returns:
        html.Div: The created layout.
    """
    return html.Div(
        [
            dcc.Store(id="selected_table_data", storage_type="session"),
            dcc.Store(id="plot_config_table", storage_type="memory"),
            graph_setting(),
            plot_config(),
            html.Div(children=[], id="2d_plot_chart", style={"padding": "20px"}),
        ],
        style={"padding": "20px"},
    )


#####################################################################################################################################################
@app.callback(Output("x_axis", "options"), Output("y_axis", "options"), Input("selected_table_data", "data"))
def update_attributes(selected_data: dict[str, list[dict]]) -> list[str]:
    """Update List of selectable attributes.

    Args:
        selected_data (dict[str, list[dict]]): All selected data tables.

    Returns:
        list[str]: List of common attributes between those tables.
    """
    columns = filter_columns(selected_data)
    return columns, columns


#####################################################################################################################################################
@app.callback(
    Output("2d_table_select", "options", allow_duplicate=True), Input("url", "pathname"), State("table-data", "data"), prevent_initial_call=True
)
def display_page(pathname: str, table_data: dict) -> list[str]:
    """Change the webpage.

    Args:
        pathname (str): Name of the current path.

    Returns:
        tuple[html.Div, dict]: List with html components for page-content and data.
    """
    if table_data is None:
        return []
    return list(table_data)


#####################################################################################################################################################
@app.callback(Output("value_to_plot", "options"), Input("plot_type", "value"))
def update_possible_types(plot_type: str) -> list[str]:
    """Update possible config to create plots.

    Args:
        plot_type (str): The selected plot type.

    Returns:
        list[str]: List of selectable attributes.
    """
    if plot_type is None:
        return []
    if plot_type in ["Line", "Bar"]:
        return ["History", "Min", "Max", "Median", "Mean"]
    return []


#####################################################################################################################################################
@app.callback(Output("group_by", "options"), Input("value_to_plot", "value"), Input("x_axis", "options"))
def update_group_options(value_to_plot: str, attributes: list[str]) -> list[str]:
    """Update the possible group options.

    Args:
        value_to_plot (str): Selected value to plot.
        attributes (list[str]): The selectable attributes to select the grouping category.

    Returns:
        list[str]: List of attributes the dataset can be grouped by.
    """
    if value_to_plot is None:
        return []
    if value_to_plot in ["History", "Min", "Max", "Median", "Mean"]:
        return attributes
    return []


#####################################################################################################################################################
@app.callback(Output("select_2d_table", "options"), Input("table_data", "data"))
def update_selectable_data(table_data: dict[str, list[dict]]) -> list[str]:
    """Update selectable data.

    Args:
        table_data (dict[str, list[dict]]): All uploaded datasets.

    Returns:
        list[str]: List of dataset keys.
    """
    if table_data is None:
        return []
    return list(table_data)


#####################################################################################################################################################
@app.callback(Output("plot_config_table", "data"), Input("select_2d_table", "value"))
def reset_config_table(data: dict) -> dict:
    """Reset the plot_config_table.

    Args:
        data (dict): The updated select_2d_table.

    Returns:
        dict: The new plot_config table.
    """
    return {"settings": []}


#####################################################################################################################################################
@app.callback(Output("selected_table_data", "data"), Input("select_2d_table", "value"), State("table_data", "data"))
def selected_table(selected_tables: list[str], table_data: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Update the selected table value.

    Args:
        selected_tables (list[str]): List of tables that have been selected.
        table_data (dict[str, list[dict]]): The current stored data.

    Returns:
        dict[str, list[dict]]: A dictionary of the selected tables.
    """
    if selected_tables is None:
        return dash.no_update
    if table_data is None:
        return dash.no_update
    return {key: table_data[key] for key in selected_tables}
