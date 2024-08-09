
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from dash.dependencies import Input, Output  # noqa: F811


def get_topbar() -> dbc.NavbarSimple:
    """Return the topbar.

    Returns:
        dbc.NavbarSimple: Topbar with navigation to the subpages.
    """
    return dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Data", href="/")),
        dbc.NavItem(dbc.NavLink("2D-Plot", href="/plot_2d")),
    ],
    brand="Analyse Dash App",
    brand_href="/",
    color="black",
    dark=True,
)


def page_layout() -> html.Div:
    """Return the webpage layout.

    Returns:
        html.Div: Div that contains the base layout.
    """
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="table_data", storage_type="session"),
            get_topbar(),
            html.Div(id="page-content"),
        ]
    )
