"""DataAnalyse Page."""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.dependencies import Input, Output

from plot_page.view.components.app import app

from plot_page.view.components import get_upload_component
from plot_page.view.pages.data_analyse import data_correlation, data_notlinear_regression


#####################################################################################################################################################
def graph_setting() -> dbc.Card:
    """Create graph setting card.

    Returns:
        dbc.Card: dbc.Card that lets the user configure settings for the plot.
    """
    return dbc.Card(
        [
            html.H1("DATA UPLOAD", style={"textAlign": "center"}),
            get_upload_component(),
            html.Div(dcc.Dropdown([], value=None, id="data_select_table", clearable=True), style={"padding": "1em"}),
            html.Div(
                dcc.Dropdown(["Correlation coefficients", "Notlinear Regression"], value="None", id="data_analyse_tool", disabled=True),
                style={"padding": "1em"},
            ),
        ]
    )


def data_analyse_layout() -> html.Div:
    return html.Div(
        [
            dcc.Store(id="data_attribute_options", data=[]),
            graph_setting(),
            html.Div(id="data_analyse_setting", style={"padding": "2em"}),
            html.Div(id="data_analyse_content", style={"padding": "2em"}),
            html.Div(id="data_analyse_notlinear", style={"padding": "2em"}),
        ],
        style={"padding": "1em"},
    )


@app.callback(Output("data_analyse_setting", "children"), Input("data_analyse_tool", "value"))
def data_update_settings_page(selected_data_analyse_tool: str) -> html.Div:
    if selected_data_analyse_tool == "Correlation coefficients":
        return data_correlation.layout()
    if selected_data_analyse_tool == "Notlinear Regression":
        return data_notlinear_regression.layout()
    return html.Div()


@app.callback(Output("data_select_table", "options"), Input("url", "pathname"), Input("table_data", "data"))
def data_update_selectable_tables(pathname: str, table_data: dict[str, list] | None) -> list[str]:
    if table_data is None:
        return []
    return list(table_data)


@app.callback(Output("data_analyse_tool", "disabled"), Input("data_select_table", "value"))
def data_update_disabled_tool(selected_table: str) -> bool:
    return selected_table is None or len(selected_table) < 1


@app.callback(Output("data_attribute_options", "data"), Input("data_select_table", "value"), State("table_data", "data"))
def data_update_attribut_options(selected_table: str, table_data: dict[str, list[str]]) -> list[str]:
    return [] if selected_table is None else table_data[selected_table]
