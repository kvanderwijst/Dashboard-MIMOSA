"""
Creates the main Dash application and provides the external stylesheets
"""
from common.dash import dbc, dash

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, title="MIMOSA Dashboard"
)
app.config.suppress_callback_exceptions = True
app._favicon = "circle_logo.svg"
