"""Functions for visualisation of basic components."""

import dash_bootstrap_components as dbc
from dash import dcc, html


from plot_page.data.panda_data import list_dataframes, load_dataframe


#####################################################################################################################################################
def get_topbar() -> dbc.NavbarSimple:
    """Return the topbar.

    Returns:
        dbc.NavbarSimple: Topbar with navigation to the subpages.
    """
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Data", href="/")),
            dbc.NavItem(dbc.NavLink("2D-Plot", href="/plot_2d")),
            dbc.NavItem(dbc.NavLink("Data-Analyse", href="/data_analyse")),
        ],
        brand="Analyse Dash App",
        brand_href="/",
        color="black",
        dark=True,
    )


#####################################################################################################################################################
def page_layout() -> html.Div:
    """Return the webpage layout.

    Returns:
        html.Div: Div that contains the base layout.
    """
    load_dataframe
    existing_data = {key[:-4]: list(load_dataframe(key).columns) for key in list_dataframes() if key.endswith(".pkl")}
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="table_data", data=existing_data, storage_type="session"),
            dcc.Store(id="new_table_data", storage_type="session"),
            get_topbar(),
            html.Div(id="page-content"),
        ]
    )


#####################################################################################################################################################
def get_upload_component() -> dcc.Upload:
    """Create a dcc component that allows to upload a file.

    Returns:
        dcc.Upload: The created upload component.
    """
    return dcc.Upload(
        id="upload-plot",
        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
        style={
            "width": "95%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
            "display": "inline-block",
            "align": "center",
        },
        multiple=True,
    )
