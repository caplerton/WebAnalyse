"""Page to update and modify data.."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html

from plot_page.control.data_operation.extract_information import query_table
from plot_page.control.visualisation.gui_control import upload_create_filtered_dataset
from plot_page.data.panda_data import remove_dataframe
from plot_page.view.components.app import app

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
def create_query_components() -> html.Div:
    """Card to add queries that should be applied on the selected table.

    Returns:
        html.Div: A html.Div that can be used to apply queries on the dataframe.
    """
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


####################################################################################################################################################
@app.callback(
    Output("table_data", "data", allow_duplicate=True),
    Input("upload_remove_table", "n_clicks"),
    State("upload_selected_table", "value"),
    State("table_data", "data"),
    prevent_initial_call=True,
)
def upload_remove_selected_table(n_clicks: int, selected_table: str | None, table_data: dict[str, list]) -> dict[str, list]:
    """Remove a stored dataframe.

    Args:
        n_clicks (int): Remove clicke event.
        selected_table (str | None): Delete the dataset with this name.
        table_data (dict[str, list]): The current Information about the datasets.

    Returns:
        dict[str, list]: The updated information about the dataset.
    """
    if n_clicks is None or selected_table is None:
        return dash.no_update
    remove_dataframe(selected_table)
    if selected_table in table_data:
        table_data.pop(selected_table)
    return table_data


####################################################################################################################################################
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
    res, res_string = upload_create_filtered_dataset(n_clicks, selected_table, table_name, query_list, table_data)
    return res if res else dash.no_update


####################################################################################################################################################
@app.callback(Output("plot_table", "data"), Input("upload_selected_table", "value"), Input("upload_query_list", "data"))
def upload_update_plot(selected_table: str | None, query_list: list[str]) -> list[dict]:
    """Update data that should be shown.

    Args:
        selected_table (str | None): The current selected table.
        query_list (list[str]): List of all queries that should be applied on the selected table.

    Returns:
        list[dict]: List of data records that should be shown.
    """
    return query_table(selected_table, query_list).to_dict("records") if selected_table else dash.no_update


####################################################################################################################################################
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
    """Add/remove query from the list.

    Args:
        remove_click (int | None): Remove button click event.
        add_click (int | None): Add button click event.
        new_query (str | None): The query that should be added to the list.
        current_queries (list[str]): List of current queries.

    Returns:
        tuple[list[str], str]: New query list and updated value for query_input.
    """
    if remove_click is not None:
        return [], ""

    if add_click is None or new_query is None or len(new_query) < 3:
        return dash.no_update, dash.no_update
    return [new_query] + current_queries, ""


####################################################################################################################################################
@app.callback(Output("upload_query_output", "children"), Input("upload_query_list", "data"))
def upload_update_query_output(query_list: list[str] | None) -> html.P:
    """Shows all query statements.

    Args:
        query_list (list[str] | None): List of current queries.

    Returns:
        html.P: An paragraph that shows all queries separated by ",".
    """
    return [html.P(", ".join(query_list))] if query_list else dash.no_update


####################################################################################################################################################
@app.callback(Output("upload_selected_table", "options"), Input("table_data", "data"))
def upload_table_selction_options(table_data: dict[str, list[dict]] | None) -> list[str]:
    """Update available data options.

    Args:
        table_data (dict[str, list[dict]] | None): The current uploaded data options.

    Returns:
        list[str]: List of all keys in table_data.
    """
    return list(table_data) if table_data else dash.no_update
