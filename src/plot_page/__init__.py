import dash
from dash import Input, Output, State

from plot_page.app import app
from plot_page.control.data_operations import prepare_upload_data
from plot_page.view.components import page_layout  # noqa: F811
from plot_page.view.pages import home, plot_2d

if __name__ == "__main__":
    app.layout = page_layout()
    app.run_server(debug=True)


#####################################################################################################################################################
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def display_page(pathname: str) -> list:
    """Change the webpage.

    Args:
        pathname (str): Name of the current path.

    Returns:
        tuple[html.Div, dict]: List with html components for page-content and data.
    """
    if pathname == "/plot_2d":
        return plot_2d.layout()
    else:
        return home.layout()


#####################################################################################################################################################
@app.callback(
    Output("table_data", "data", allow_duplicate=True),
    Input("upload-plot", "contents"),
    State("upload-plot", "filename"),
    State("table_data", "data"),
    prevent_initial_call=True,
)
def upload_data(contents: str, filenames: str, table_data: None | dict[str, dict]):
    """Upload files to webpage.

    Args:
        contents (str): The uploaded file content.
        filenames (str): Name of the uploaded file.
        table_data (None | dict[str, dict]): The current stored data.
    """
    if contents is None or filenames is None:
        return dash.no_update
    for uploaded_data in zip(filenames, contents):
        table_data = prepare_upload_data(uploaded_data, table_data)
    return table_data
