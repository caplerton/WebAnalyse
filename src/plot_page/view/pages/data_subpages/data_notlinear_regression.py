import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html
from dash.dependencies import Input, Output

from plot_page.app import app
from plot_page.control.gui_update import notlinear_regression_evaluation


def layout() -> html.Div:
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


@app.callback(
    Output("data_notlinear_regression_attribute1", "options"),
    Output("data_notlinear_regression_attribute2", "options"),
    Input("data_attribute_options", "data"),
)
def data_correlation_attributes(attributes: list[str]) -> tuple[list[str]]:
    ret_val = [] if attributes is None else attributes
    return ret_val, ret_val


@app.callback(
    Output("data_analyse_notlinear", "children", allow_duplicate=True),
    Input("data_notlinear_regression_evaluation", "n_clicks"),
    State("data_select_table", "value"),
    State("data_notlinear_regression_attribute1", "value"),
    State("data_notlinear_regression_attribute2", "value"),
    State("data_notlinear_regression_model", "value"),
    prevent_initial_call=True,
)
def data_correlation_update_output(
    n_clicks: int | None, selected_table: str | None, main_attribute: str | None, second_attributes: str | None, selected_model: str | None
) -> list[html.Div]:
    if n_clicks is None:
        return dash.no_update
    return notlinear_regression_evaluation(selected_table, main_attribute, second_attributes, selected_model)
