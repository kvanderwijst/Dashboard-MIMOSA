from common.dash import *
from common import data

from app import app
from pages.components.tabs_components import GDP, costs, emissions

layout = dbc.Row([
    dbc.Col([
        dcc.Tabs([
            dcc.Tab(label='Emissions', children=emissions.layout),
            dcc.Tab(label='Costs', children=costs.layout),
            dcc.Tab(label='GDP', children=GDP.layout),
            dcc.Tab(label='Damages', children='tab-content-4'),
            dcc.Tab(label='Input parameters', children='tab-content-5'),
            dcc.Tab(label='IPOPT output', children='tab-content-6'),
        ])
    ])
])
