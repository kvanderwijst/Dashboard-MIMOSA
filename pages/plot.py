from common.dash import *

from app import app
from pages.components import fileselection, tabs

back_button = dbc.Button('< Back to content', href='/', color='primary', outline=True)

layout = html.Div([
    html.H1('Project MIMOSA'),
    html.H3('Plot results'),
    html.Hr(),
    
    fileselection.layout,
    
    html.Br(),

    tabs.layout,


    html.Br(),
    html.Div(id='empty', style={'display': 'none'}),
    html.Hr(),
    back_button
])
