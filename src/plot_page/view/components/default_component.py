
from dash import dcc, html



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
