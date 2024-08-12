"""Functions to visualise the home page."""

import os
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html
import pandas as pd

from plot_page.app import app
from plot_page.control.data_operations import add_dataset
from plot_page.data.global_variables import DATAFRAME_STORE
from plot_page.view.components import get_upload_component


#####################################################################################################################################################
def explanation_card() -> html.Div:
    """Create a card that explains the webpage.

    Returns:
        html.Div: The explanation of the webpage as html. Div
    """
    return dbc.Card(
        [
            html.H4("Data Manager", style={"text-align": "center"}),
            html.P("This page is used to upload data for analysis purposes. The uploaded data can be viewed in more detail in the table below."),
            html.P("Currently only json-files are allowed with the structure {'table_names': list[dict[str, val]]}"),
            html.H5("Upload Files", style={"text-align": "center"}),
            html.Div(get_upload_component(), style={"text-align": "center"}),
        ]
    )


#####################################################################################################################################################
def create_table_card() -> dbc.Card:
    """Create a card that allows to visualise the uploaded data.

    Returns:
        dbc.Card: The table dbc.Card that allows to modify and show data in a table.
    """
    return dbc.Card(
        [
            html.H2("Table", style={"text-align": "center"}),
            html.Div(
                dcc.Dropdown(options=["None"], id="table_select"),
                style={"padding": "20px"},
            ),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(options=["None"], id="attribute_select"), width=3),
                        dbc.Col(dcc.Dropdown([">=", ">", "<", "<=", "=", "!="], id="filter_drop"), width=3),
                        dbc.Col(dbc.Input(placeholder="Value...", type="text", id="value_input"), width=3),
                        dbc.Col(dbc.Button("use filter", id="add_filter"), width=1),
                    ]
                ),
                style={"padding": "20px"},
            ),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Input(placeholder="Save filtered dataset as", type="text", id="save_name"), width=3),
                        dbc.Col(dbc.Button("Save dataset", id="save_dataset"), width=2),
                    ]
                ),
                style={"padding": "20px"},
            ),
            dash_table.DataTable(data=[], id="plot_table", page_size=20, export_format="csv"),
        ]
    )


#####################################################################################################################################################
def layout() -> html.Div:
    """The data home layout.

    Returns:
        html.Div: Home layout that is used for the page-content.
    """
    return html.Div(
        [
            dcc.Store(id="current_filter"),
            html.H1("Analyse Page", style={"text-align": "center"}),
            html.Div(explanation_card(), style={"padding": "20px"}),
            html.Div(create_table_card(), style={"padding": "20px"}),
        ]
    )


#####################################################################################################################################################
@app.callback(
    Output("table_data", "data", allow_duplicate=True),
    Input("use_dataset", "n_clicks"),
    State("table_data", "data"),
    State("current_filter", "data"),
    State("input_name", "value"),
    prevent_initial_call=True,
)
def add_filtered_data(n_clicks: int, table_data: dict, add_data: list[dict], name_dataset: str) -> dict:
    """Add a new dataset.

    Args:
        n_clicks (int): Check if it is a click event.
        table_data (dict): Dictionary of key and dataset.
        add_data (list[dict]): The value that should be added.
        name_dataset (str): Name of the dataset.

    Returns:
        dict: Updated dictionary.
    """
    if n_clicks is None:
        return dash.no_update
    return add_dataset(table_data, add_data, name_dataset)


####################################################################################################################################################
@app.callback(Output("table_select", "options"), Input("table_data", "data"))
def table_options(table_data: dict[str, list[dict]]) -> list[str]:
    """Update available data options.

    Args:
        table_data (dict[str, list[dict]]): The current uploaded data options.

    Returns:
        list[str]: List of all keys in table_data.
    """
    if table_data is None:
        return dash.no_update
    return list(table_data)


#####################################################################################################################################################
@app.callback(
    Output("plot_table", "data", allow_duplicate=True),
    Output("attribute_select", "options"),
    Input("table_select", "value"),
    prevent_initial_call="initial_duplicate",
)
def table_select(selected_table: str) -> tuple[list[dict], list[str]]:
    """Updated selected table.

    Args:
        selected_table (str): The current key of the selcted table.

    Returns:
        tuple[list[dict], list[str]]: Value of the selected table and possible attributes to filter.
    """
    if selected_table is None:
        return dash.no_update, []
    current_dataframe = pd.read_pickle(os.path.join(DATAFRAME_STORE, f"{selected_table}.pkl"))
    records = current_dataframe.to_dict("records")
    return records, list(records[0])


# #####################################################################################################################################################
# @app.callback(
#     Output("current_filter", "data", allow_duplicate=True),
#     Input("add_filter", "n_clicks"),
#     State("attribute_select", "value"),
#     State("filter_drop", "value"),
#     State("value_input", "value"),
#     State("current_filter", "data"),
#     prevent_initial_call="initial_duplicate",
# )
# def filter_table(n_clicks: int, selected_attribute: str, filter_operation: str, filter_value: str, table_data: dict) -> dict:
#     """Use filter for this table.

#     Args:
#         n_clicks (int): Click event.
#         selected_attribute (str): Selected attribute to filter data.
#         filter_operation (str): Selected operation to filter data.
#         filter_value (str): Use this value as reference.
#         table_data (dict): The current table data.

#     Returns:
#         dict: The updated table data.
#     """
#     if any(input_data is None for input_data in [n_clicks, filter_operation, selected_attribute, filter_value, table_data]):
#         return dash.no_update

#     try:
#         if filter_operation == "<=":
#             return [val for val in table_data if val.get(selected_attribute, None) <= float(filter_value)]
#         if filter_operation == "<":
#             return [val for val in table_data if val.get(selected_attribute, None) < float(filter_value)]
#         if filter_operation == ">":
#             return [val for val in table_data if val.get(selected_attribute, None) > float(filter_value)]
#         if filter_operation == ">=":
#             return [val for val in table_data if val.get(selected_attribute, None) >= float(filter_value)]
#         if filter_operation == "=":
#             return [val for val in table_data if str(val.get(selected_attribute, None)) == filter_value]
#         if filter_operation == "!=":
#             return [val for val in table_data if str(val.get(selected_attribute, None)) != filter_value]
#     except Exception:
#         pass
#     return table_data


# #####################################################################################################################################################
# @app.callback(
#     Output("table_data", "data"),
#     Input("save_dataset", "n_clicks"),
#     State("save_name", "value"),
#     State("table_data", "data"),
#     State("current_filter", "data"),
# )
# def save_filtered_data(click_event: int, save_name: str, table_data: dict[str, list[dict]], current_data: list[dict]) -> dict[str, list[dict]]:
#     """Store current displayed data in the dictionary.

#     Args:
#         click_event (int): Click event.
#         save_name (str): Name of the current visualised dataset in table_data.
#         table_data (dict[str, list[dict]]): The current table_data that holds all tables.
#         current_data (list[dict]): The current visualised dataset.

#     Returns:
#         dict[str, list[dict]]: The updated table_data.
#     """
#     if any(input_data is None for input_data in [click_event, save_name, current_data, table_data]):
#         return dash.no_update
#     table_data[save_name] = current_data
#     return table_data
