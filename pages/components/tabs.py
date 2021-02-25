"""
Simple dash Tabs for each part of the visualisation
"""
from common.dash import dcc, dbc

from pages.components.tabs_components import (
    gdp,
    costs,
    damages,
    emissions,
    inputparams,
)

layout = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(label="Emissions", children=emissions.layout),
                        dcc.Tab(label="Costs", children=costs.layout),
                        dcc.Tab(label="GDP", children=gdp.layout),
                        dcc.Tab(label="Damages", children=damages.layout),
                        dcc.Tab(label="Input parameters", children=inputparams.layout),
                        dcc.Tab(label="IPOPT output", children="tab-content-6"),
                    ]
                )
            ]
        )
    ]
)
