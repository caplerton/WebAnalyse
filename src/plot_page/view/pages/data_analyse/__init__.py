"""DataAnalyse Page."""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html


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


#####################################################################################################################################################
def data_analyse_layout() -> html.Div:
    """Data analyse components.

    Returns:
        html.Div: html.Div that contains the base layout for data analyse.
    """
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


#####################################################################################################################################################
@app.callback(Output("data_analyse_setting", "children"), Input("data_analyse_tool", "value"))
def data_update_settings_page(selected_data_analyse_tool: str) -> html.Div:
    """Change the shown settings content.

    Args:
        selected_data_analyse_tool (str): The current selected analyse tool.

    Returns:
        html.Div: Html components that lets user do the configue for the analyse tool.
    """
    if selected_data_analyse_tool == "Correlation coefficients":
        return data_correlation.layout()
    if selected_data_analyse_tool == "Notlinear Regression":
        return data_notlinear_regression.layout()
    return html.Div()


#####################################################################################################################################################
@app.callback(Output("data_select_table", "options"), Input("url", "pathname"), Input("table_data", "data"))
def data_update_selectable_tables(pathname: str, table_data: dict[str, list] | None) -> list[str]:
    """Update the selected table.

    Args:
        pathname (str): Event when page was loaded.
        table_data (dict[str, list] | None): The current table data.

    Returns:
        list[str]: List of selectable tables as option.
    """
    return list(table_data) if table_data else []


#####################################################################################################################################################
@app.callback(Output("data_analyse_tool", "disabled"), Input("data_select_table", "value"))
def data_update_disabled_tool(selected_table: str) -> bool:
    """Dash update the disabled status of a component.

    Args:
        selected_table (str): The current selected table.

    Returns:
        bool: True if no table is selected.
    """
    return selected_table is None or len(selected_table) < 1


#####################################################################################################################################################
@app.callback(Output("data_attribute_options", "data"), Input("data_select_table", "value"), State("table_data", "data"))
def data_update_attribut_options(selected_table: str, table_data: dict[str, list[str]]) -> list[str]:
    """Update the selectable attribute options.

    Args:
        selected_table (str): The new selected table.
        table_data (dict[str, list[str]]): Data of all dataframes.

    Returns:
        list[str]: The attributes that can be selected for configuration purpose.
    """
    return table_data[selected_table] if selected_table else []
