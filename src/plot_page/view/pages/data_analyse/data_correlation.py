"""Correlation page."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from plot_page.control.visualisation.gui_control import correlation_evaluation
from plot_page.view.components.app import app


#####################################################################################################################################################
def layout() -> dbc.Card:
    """Correlation page.

    Returns:
        dbc.Card: The layout of the correlation page.
    """
    return dbc.Card(
        [
            html.H1("CORRELATION COEFFICIENT", style={"textAlign": "center"}),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(options=[], value=None, id="data_correlation_main_attribute", multi=False), width=2),
                    dbc.Col(dcc.Dropdown(options=[], id="data_correlation_second_attributes", value=None, multi=True), width=2),
                    dbc.Col(dbc.Button("Analyse", id="data_correlation_evaluation"), width=2),
                ],
                style={"padding": "1em"},
            ),
        ]
    )


#####################################################################################################################################################
@app.callback(
    Output("data_correlation_main_attribute", "options"),
    Output("data_correlation_second_attributes", "options"),
    Input("data_attribute_options", "data"),
)
def data_correlation_attributes(attributes: list[str]) -> tuple[list[str]]:
    """Update the attribute options.

    Args:
        attributes (list[str]): Attribute list of the selected table.

    Returns:
        tuple[list[str]]: Returns the attributes to multiple components.
    """
    return (attributes, attributes) if attributes else ([], [])


#####################################################################################################################################################
@app.callback(
    Output("data_analyse_content", "children", allow_duplicate=True),
    Input("data_correlation_evaluation", "n_clicks"),
    State("data_select_table", "value"),
    State("data_correlation_main_attribute", "value"),
    State("data_correlation_second_attributes", "value"),
    prevent_initial_call=True,
)
def data_correlation_update_output(
    n_clicks: int | None, selected_table: str | None, main_attribute: str | None, second_attributes: list[str] | None
) -> list[html.Div]:
    """Show the correlation result.

    Args:
        n_clicks (int | None): Click event.
        selected_table (str | None): The current selected table.
        main_attribute (str | None): The primary attribute.
        second_attributes (list[str] | None): The secondary attribute.

    Returns:
        list[html.Div]: List of html components that are used to visualise the result.
    """
    return correlation_evaluation(selected_table, main_attribute, second_attributes) if n_clicks else dash.no_update
