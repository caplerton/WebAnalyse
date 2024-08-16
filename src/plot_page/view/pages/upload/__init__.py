"""Functions to visualise the home page."""

import os
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html
import pandas as pd

from plot_page.view.components.app import app
from plot_page.control.data_operations import add_dataset
from plot_page.control.table_operations import query_table
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


def create_query_components() -> html.Div:
    return html.Div(
        dbc.Row(
            [
                dbc.Col(dbc.Input(placeholder="Add Query (e.g. age < 20 )", type="text", id="upload_query_input"), width=4),
                dbc.Col(dbc.Button("add query", id="upload_query_add_button", style={"width": "100%"}), width=2),
                dbc.Col(dbc.Button("reset queries", id="upload_query_remove_button", style={"width": "100%"}), width=2),
                dbc.Col(html.Div(children=[], id="upload_query_output"), width=4),
            ]
        ),
        style={"padding": "20px"},
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
                children=dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(options=["None"], id="upload_selected_table"), width=9),
                        dbc.Col(dbc.Button("Remove Table", id="upload_remove_table", style={"width": "100%"}), width=3),
                    ]
                ),
                style={"padding": "20px"},
            ),
            create_query_components(),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Input(placeholder="Save filtered dataset as", type="text", id="upload_save_name"), width=3),
                        dbc.Col(dbc.Button("Save dataset", id="upload_save_dataset"), width=2),
                    ]
                ),
                style={"padding": "20px"},
            ),
            dash_table.DataTable(data=[], id="plot_table", page_size=20, export_format="csv"),
        ]
    )


@app.callback(
    Output("table_data", "data", allow_duplicate=True),
    Input("upload_remove_table", "n_clicks"),
    State("upload_selected_table", "value"),
    State("table_data", "data"),
    prevent_initial_call=True,
)
def upload_remove_selected_table(n_clicks: int, selected_table: str | None, table_data: dict[str, list]) -> dict[str, list]:
    if n_clicks is None or selected_table is None:
        return dash.no_update
    file_path = os.path.join(DATAFRAME_STORE, f"{selected_table}.pkl")
    if os.path.exists(file_path):
        os.remove(file_path)
    if selected_table in table_data:
        table_data.pop(selected_table)
    return table_data


#####################################################################################################################################################
def upload_layout() -> html.Div:
    """The data home layout.

    Returns:
        html.Div: Home layout that is used for the page-content.
    """
    return html.Div(
        [
            dcc.Store(id="upload_query_list", data=[]),
            dcc.Store(id="current_filter"),
            html.H1("Analyse Page", style={"text-align": "center"}),
            html.Div(explanation_card(), style={"padding": "20px"}),
            html.Div(create_table_card(), style={"padding": "20px"}),
        ]
    )


@app.callback(
    Output("table_data", "data"),
    Output("upload_save_name", "value"),
    Input("upload_save_dataset", "n_clicks"),
    State("upload_selected_table", "value"),
    State("upload_save_name", "value"),
    State("upload_query_list", "data"),
    State("table_data", "data"),
)
def upload_save_filtered_dataset(
    n_clicks: int | None, selected_table: str | None, table_name: str | None, query_list: list[str], table_data: dict[str, list]
) -> dict[str, list]:
    if n_clicks is None:
        return dash.no_update, dash.no_update
    if selected_table is None:
        return dash.no_update, dash.no_update
    if table_name is None or len(table_name) < 1:
        return dash.no_update, dash.no_update

    res_dataframe = query_table(selected_table, query_list)
    pd.to_pickle(res_dataframe, os.path.join(DATAFRAME_STORE, f"{table_name}.pkl"))
    table_data[table_name] = list(res_dataframe.columns)
    return table_data, ""


@app.callback(Output("plot_table", "data"), Input("upload_selected_table", "value"), Input("upload_query_list", "data"))
def upload_update_plot(selected_table: str | None, query_list: list[str]) -> list[dict]:
    if selected_table is None:
        return dash.no_update
    res_dataframe = query_table(selected_table, query_list)
    return res_dataframe.to_dict("records")


@app.callback(
    Output("upload_query_list", "data"),
    Output("upload_query_input", "value"),
    Input("upload_query_remove_button", "n_clicks"),
    Input("upload_query_add_button", "n_clicks"),
    State("upload_query_input", "value"),
    State("upload_query_list", "data"),
)
def upload_update_query_list(
    remove_click: int | None, add_click: int | None, new_query: str | None, current_queries: list[str]
) -> tuple[list[str], str]:
    if remove_click is not None:
        return [], ""

    if add_click is None or new_query is None or len(new_query) < 3:
        return dash.no_update, dash.no_update
    return [new_query] + current_queries, ""


@app.callback(Output("upload_query_output", "children"), Input("upload_query_list", "data"))
def upload_update_query_output(query_list: list[str] | None) -> html.P:
    if query_list is None:
        return dash.no_update
    return [html.P(", ".join(query_list))]


####################################################################################################################################################
@app.callback(Output("upload_selected_table", "options"), Input("table_data", "data"))
def upload_table_selction_options(table_data: dict[str, list[dict]] | None) -> list[str]:
    """Update available data options.

    Args:
        table_data (dict[str, list[dict]]): The current uploaded data options.

    Returns:
        list[str]: List of all keys in table_data.
    """
    if table_data is None:
        return dash.no_update
    return list(table_data)
