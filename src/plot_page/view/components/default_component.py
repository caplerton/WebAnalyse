import base64
import datetime
import io
import json
import operator
import os

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc, html

from plot_page.app import app
from plot_page.control.data_operations import add_dataset, prepare_upload_data


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
