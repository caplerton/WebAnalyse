import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html
from dash.dependencies import Input, Output

from plot_page.view.components.app import app
from plot_page.control.gui_update import correlation_evaluation
from plot_page.control.plot_functions import plot_correlation_coefficient


def layout() -> dbc.Card:
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


@app.callback(
    Output("data_correlation_main_attribute", "options"),
    Output("data_correlation_second_attributes", "options"),
    Input("data_attribute_options", "data"),
)
def data_correlation_attributes(attributes: list[str]) -> tuple[list[str]]:
    ret_val = [] if attributes is None else attributes
    return ret_val, ret_val


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
    if n_clicks is None:
        return dash.no_update
    return correlation_evaluation(selected_table, main_attribute, second_attributes)
