"""Notlinear regression analyse page."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.dependencies import Input, Output

from plot_page.control.visualisation.gui_control import notlinear_regression_evaluation
from plot_page.view.components.app import app


#####################################################################################################################################################
def layout() -> html.Div:
    """Notlinear regression layout.

    Returns:
        html.Div: Notlinear regression content.
    """
    return dbc.Card(
        [
            html.H1("NOTLINEAR REGRESSION", style={"textAlign": "center"}),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            options=[],
                            value=None,
                            id="data_notlinear_regression_attribute1",
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            options=[],
                            id="data_notlinear_regression_attribute2",
                            value=None,
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            options=[
                                "linear",
                                "quadratic",
                                "exponential",
                                "power",
                                "sinus",
                                "gaussian",
                                "polynomial3",
                                "polynomial4",
                                "polynomial5",
                            ],
                            id="data_notlinear_regression_model",
                            value=None,
                        ),
                        width=2,
                    ),
                    dbc.Col(dbc.Button("Analyse", id="data_notlinear_regression_evaluation"), width=2),
                ],
                style={"padding": "1em"},
            ),
        ]
    )


#####################################################################################################################################################
@app.callback(
    Output("data_notlinear_regression_attribute1", "options"),
    Output("data_notlinear_regression_attribute2", "options"),
    Input("data_attribute_options", "data"),
)
def data_notlinear_attributes(attributes: list[str]) -> tuple[list[str]]:
    """Update the attribute options.

    Args:
        attributes (list[str]): Attribute list of the selected table.

    Returns:
        tuple[list[str]]: Returns the attributes to multiple components.
    """
    return (attributes, attributes) if attributes else ([], [])


#####################################################################################################################################################
@app.callback(
    Output("data_analyse_notlinear", "children", allow_duplicate=True),
    Input("data_notlinear_regression_evaluation", "n_clicks"),
    State("data_select_table", "value"),
    State("data_notlinear_regression_attribute1", "value"),
    State("data_notlinear_regression_attribute2", "value"),
    State("data_notlinear_regression_model", "value"),
    prevent_initial_call=True,
)
def notlinear_regression_output(
    n_clicks: int | None, selected_table: str | None, main_attribute: str | None, second_attributes: str | None, selected_model: str | None
) -> list[html.Div]:
    """Plot the notlinear regression result for the selected attributes when requested.

    Args:
        n_clicks (int | None): React on click event.
        selected_table (str | None): The current selected table.
        main_attribute (str | None): The selected primary attribute.
        second_attributes (str | None): The selected secondary attribute.
        selected_model (str | None): The selected notlinear model that should be trained.

    Returns:
        list[html.Div]: The resulting plot that shows the notlinear regression result.
    """
    return notlinear_regression_evaluation(selected_table, main_attribute, second_attributes, selected_model) if n_clicks else dash.no_update
