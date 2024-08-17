"""Page to visualise the data as 2d plot."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html


from plot_page.control.data_operation.extract_information import get_intersections_dict
from plot_page.control.data_operation.modify_data import dictionary_values_to_string
from plot_page.control.visualisation.gui_control import create_2dplot, plot2d_generate_additional_plot_setting
from plot_page.view.components.app import app

from plot_page.view.components import get_upload_component


#####################################################################################################################################################
def plot2d_graph_setting() -> dbc.Card:
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


#####################################################################################################################################################
def plot2d_data_selection() -> dbc.Card:
    """Add components to the layout for data settings.

    Returns:
        dbc.Card: Card that contains component for data configuration.
    """
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


#####################################################################################################################################################
def plot2d_plot_configuration() -> dbc.Card:
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


#####################################################################################################################################################
def plot2d_layout() -> html.Div:
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
            plot2d_graph_setting(),
            plot2d_data_selection(),
            plot2d_plot_configuration(),
            html.Div(children=[], id="2d_plot_chart", style={"padding": "20px"}),
        ],
        style={"padding": "20px"},
    )


#####################################################################################################################################################
@app.callback(
    Output("plot2_graph_xaxis", "options"),
    Output("plot2_graph_yaxis", "options"),
    Output("plot2_group_by", "options", allow_duplicate=True),
    Input("plot2_select_table", "value"),
    State("table_data", "data"),
    prevent_initial_call=True,
)
def plot2_update_attributes(selected_tables: list[str], table_data: dict[str, list]) -> tuple[list[str]]:
    """Update Dropdown options to the possible selectable attributes.

    Args:
        selected_tables (list[str]): The current selected table.
        table_data (dict[str, list]): Name of datasets and attribute names inside.

    Returns:
        tuple[list[str]]: Tuple of attribute list.
    """
    attributes = get_intersections_dict(selected_tables, table_data)
    return (
        attributes,
        attributes,
        attributes,
    )


#####################################################################################################################################################
@app.callback(
    Output("plot2_graph_xaxis", "value"),
    Output("plot2_graph_yaxis", "value"),
    Output("plot2_group_by", "value"),
    Output("plot_settings_data", "data", allow_duplicate=True),
    Input("plot2_select_table", "value"),
    prevent_initial_call=True,
)
def reset_table_settings(selected_tables: list[str]) -> tuple[str | None]:
    """Reset the table setting.

    Args:
        selected_tables (list[str]): The new selected table.

    Returns:
        tuple[str | None]: Tuple of default values for the components.
    """
    return "", None, None, []


#####################################################################################################################################################
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
def plot2d_update_graphs(
    plot_settings: list[dict],
    title: str | None,
    selected_tables: list[str],
    x_axis: str | None,
    y_axis: str | None,
    graph_type: str | None,
) -> list[dcc.Graph]:
    """Use the current configuration to create a plot of the selected tables.

    Args:
        plot_settings (list[dict]): Information about what to plot.
        title (str | None): The table title.
        selected_tables (list[str]): A list of selected tables.
        x_axis (str | None): The selected attribute for the x-axis.
        y_axis (str | None): The selected attribute for the y-axis.
        graph_type (str | None): The graph type that should be plotted.

    Returns:
        list[dcc.Graph]: List of resulting dcc.Graphs.
    """
    res = create_2dplot(plot_settings, selected_tables, title, x_axis, y_axis, graph_type)
    return dash.no_update if res is None else res


#####################################################################################################################################################
@app.callback(
    Output("plot_settings_data", "data", allow_duplicate=True),
    Input("plot_settings_table", "data"),
    State("plot_settings_data", "data"),
    prevent_initial_call=True,
)
def plot2d_remove_plot_configuration(shown_plot_settings: list[dict], plot_settings_data: list[dict]) -> list[dict]:
    """Remove an already added plot configuration.

    Args:
        shown_plot_settings (list[dict]): Event when the shown table has changed.
        stored_table (list[dict]): The stored plot settings.

    Returns:
        list[dict]: The new plot settings.
    """
    return [val for val in plot_settings_data if any(str(val["id"]) == val2["id"] for val2 in shown_plot_settings)]


#####################################################################################################################################################
@app.callback(
    Output("plot_settings_table", "data"),
    Output("plot2_select_type", "value"),
    Output("plot2_value_type", "value"),
    Output("plot2_group_by", "value", allow_duplicate=True),
    Output("plot2_mode_selector", "value"),
    Input("plot_settings_data", "data"),
    prevent_initial_call=True,
)
def plot2d_reset_plot_type(plot_settings_data: list[str]) -> tuple[str]:
    """Reset plot type.

    Args:
        plot_settings_data (list[str]): The current plot settings.

    Returns:
        tuple[str]: Tuple with default values for the html components.
    """
    return dictionary_values_to_string(plot_settings_data), "Line", "History", None, "lines"


#####################################################################################################################################################
@app.callback(
    Output("plot_settings_data", "data"),
    Input("plot_add_plot_config", "n_clicks"),
    State("plot2_select_type", "value"),
    State("plot2_value_type", "value"),
    State("plot2_group_by", "value"),
    State("plot2_mode_selector", "value"),
    State("plot_settings_data", "data"),
)
def plot2d_add_additional_plot(
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
    res = plot2d_generate_additional_plot_setting(n_clicks, plot_type, value_type, group_by, mode_selector, current_plot_settings)
    return res if res else dash.no_update


#####################################################################################################################################################
@app.callback(Output("plot2_select_table", "options"), Input("table_data", "data"))
def plot2d_update_selectable_tables(data_tables: dict[str, list]) -> list[str]:
    """Update list of selectable tables.

    Args:
        data_tables (dict[str, list]): List of stored tables.

    Returns:
        list[str]: List that contains names of the stored tables.
    """
    return list(data_tables) if data_tables else []
