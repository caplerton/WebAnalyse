"""Functions to visualise the plot_2d page."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html
from dash.dependencies import Input, Output

from plot_page.view.components.app import app
from plot_page.control.base_functions import dictionary_values_to_string
from plot_page.control.data_operations import check_line_config, filter_columns, get_intersections_dict
from plot_page.control.gui_update import add_plot_data, create_plot, grouping_options
from plot_page.control.plot_functions import plot_data
from plot_page.view.components import get_upload_component


#####################################################################################################################################################
def graph_setting() -> dbc.Card:
    """Create graph setting card.

    Returns:
        dbc.Card: dbc.Card that lets the user configure settings for the plot.
    """
    return dbc.Card(
        [
            html.H1("DATA SELECTION", style={"textAlign": "center"}),
            get_upload_component(),
            html.Div(dcc.Dropdown([], value=[], id="plot2_select_table", multi=True, clearable=True), style={"padding": "10px"}),
        ]
    )


@app.callback(
    Output("plot2_graph_xaxis", "options"),
    Output("plot2_graph_yaxis", "options"),
    Output("plot2_group_by", "options", allow_duplicate=True),
    Input("plot2_select_table", "value"),
    State("table_data", "data"),
    prevent_initial_call=True,
)
def plot2_update_attributes(selected_tables: list[str], table_data: dict[str, list]) -> list[str]:
    attributes = get_intersections_dict(selected_tables, table_data)
    return (
        attributes,
        attributes,
        attributes,
    )


@app.callback(
    Output("plot2_graph_xaxis", "value"),
    Output("plot2_graph_yaxis", "value"),
    Output("plot2_group_by", "value"),
    Output("plot_settings_data", "data", allow_duplicate=True),
    Input("plot2_select_table", "value"),
    prevent_initial_call=True,
)
def reset_table_settings(selected_tables: list[str]) -> tuple[str | None]:
    return "", None, None, []


def plot2_upload_card() -> dbc.Card:
    return dbc.Card(
        [
            html.Div(
                [
                    html.H1("Table setting", style={"textAlign": "center"}),
                    dbc.Row(
                        [
                            dbc.Col(dbc.Input(placeholder="Enter the name:", id="plot2_graph_headline"), width=2),
                            dbc.Col(dcc.Dropdown([], placeholder="x-Axis", id="plot2_graph_xaxis"), width=2),
                            dbc.Col(dcc.Dropdown([], placeholder="y-Axis", id="plot2_graph_yaxis"), width=2),
                            dbc.Col(dcc.Dropdown(["Single Graphs", "Combined Graphs"], value="Combined Graphs", id="plot2_graph_type"), width=2),
                        ]
                    ),
                    html.Div(dash_table.DataTable(data=[], id="plot2_plot_graphs", page_size=20), style={"padding": "10px"}),
                ],
                style={"padding": "10px"},
            ),
        ]
    )


@app.callback(
    Output("2d_plot_chart", "children"),
    Input("plot_settings_data", "data"),
    State("plot2_select_table", "value"),
    State("plot2_graph_headline", "value"),
    State("plot2_graph_xaxis", "value"),
    State("plot2_graph_yaxis", "value"),
    State("plot2_graph_type", "value"),
    prevent_initial_call=True,
)
def plot_update_graphs(
    plot_settings: list[dict],
    title: str | None,
    selected_tables: list[str],
    x_axis: str | None,
    y_axis: str | None,
    graph_type: str | None,
) -> list[dcc.Graph]:
    res = create_plot(plot_settings, selected_tables, title, x_axis, y_axis, graph_type)
    return dash.no_update if res is None else res


#####################################################################################################################################################
def plot_config() -> dbc.Card:
    """Create a card to config the plot.

    Returns:
        dbc.Card: The create card that lets the user decide what to plot.
    """
    return dbc.Card(
        [
            html.H1("Add Plot", style={"textAlign": "center"}),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Dropdown(["Line", "Bar"], value="Line", placeholder="Plot Type", id="plot2_select_type"), width=2),
                            dbc.Col(
                                dcc.Dropdown(
                                    ["History", "Min", "Max", "Median", "Mean"], value="History", placeholder="Value to plot", id="plot2_value_type"
                                ),
                                width=2,
                            ),
                            dbc.Col(dcc.Dropdown(placeholder="Group By", options=[], id="plot2_group_by", multi=True), width=2),
                            dbc.Col(dcc.Dropdown(options=["lines", "lines+markers", "markers"], value="lines", id="plot2_mode_selector"), width=2),
                            dbc.Col(dbc.Button("Add Plot Config", id="plot_add_plot_config", style={"width": "100%"}), width=2),
                            dbc.Col(dbc.Button("REFRESH PLOT", id="plot_refresh_plot", style={"width": "100%"}), width=2),
                        ]
                    ),
                    dash_table.DataTable(
                        data=[],
                        id="plot_settings_table",
                        page_size=20,
                        row_deletable=True,
                    ),
                ],
                style={"padding": "10px"},
            ),
        ]
    )


@app.callback(
    Output("plot_settings_data", "data", allow_duplicate=True),
    Input("plot_settings_table", "data"),
    State("plot_settings_data", "data"),
    prevent_initial_call=True,
)
def plot_remove_table_data(shown_table: list[dict], stored_table: list[dict]) -> list[dict]:
    return [val for val in stored_table if any(str(val["id"]) == val2["id"] for val2 in shown_table)]


@app.callback(
    Output("plot_settings_table", "data"),
    Output("plot2_select_type", "value"),
    Output("plot2_value_type", "value"),
    Output("plot2_group_by", "value", allow_duplicate=True),
    Output("plot2_mode_selector", "value"),
    Input("plot_settings_data", "data"),
    prevent_initial_call=True,
)
def plot_reset_plot_type(plot_settings_data: list[str]) -> tuple[str]:
    return dictionary_values_to_string(plot_settings_data), "Line", "History", None, "lines"


@app.callback(
    Output("plot_settings_data", "data"),
    Input("plot_add_plot_config", "n_clicks"),
    State("plot2_select_type", "value"),
    State("plot2_value_type", "value"),
    State("plot2_group_by", "value"),
    State("plot2_mode_selector", "value"),
    State("plot_settings_data", "data"),
)
def plot_add_additional_plot(
    n_clicks: int | None,
    plot_type: str | None,
    value_type: str | None,
    group_by: list[str],
    mode_selector: str | None,
    current_plot_settings: list[dict],
) -> list[dict]:
    if n_clicks is None:
        return dash.no_update
    if plot_type not in ["Line", "Bar"]:
        return dash.no_update
    if not (
        plot_type == "Line"
        and value_type in ["History", "Min", "Max", "Median", "Mean"]
        or plot_type == "Bar"
        and value_type in ["Min", "Max", "Median", "Mean"]
    ):
        return dash.no_update
    plot_id = 0 if len(current_plot_settings) == 0 else max(v["id"] for v in current_plot_settings) + 1
    current_plot_settings.append({"id": plot_id, "type": plot_type, "value": value_type, "group_attributes": group_by, "mode": mode_selector})
    return current_plot_settings


#####################################################################################################################################################
def layout() -> html.Div:
    """The 2D-Plot layout.

    Returns:
        html.Div: The created layout.
    """
    return html.Div(
        [
            dcc.Store(id="plot_settings_data", data=[], storage_type="memory"),
            dcc.Store(id="plot2_possible_attributes", data=[], storage_type="session"),
            dcc.Store(id="settings", storage_type="session"),
            dcc.Store(id="selected_table_data", storage_type="session"),
            dcc.Store(id="plot_data_2d", storage_type="memory"),
            graph_setting(),
            plot2_upload_card(),
            plot_config(),
            html.Div(children=[], id="2d_plot_chart", style={"padding": "20px"}),
        ],
        style={"padding": "20px"},
    )


@app.callback(Output("plot2_select_table", "options"), Input("table_data", "data"))
def update_selectable_tables(data_tables: dict[str, list]) -> list[str]:
    if not data_tables:
        return []
    return list(data_tables)
