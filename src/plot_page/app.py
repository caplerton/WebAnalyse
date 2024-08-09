import dash_bootstrap_components as dbc
from dash import Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Analyse Dash App"
app.config.suppress_callback_exceptions = True
server = app.server
