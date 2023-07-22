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
    allvariables,
)

tab_selected_style = {"borderTop": "2px solid #89a041"}

layout = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label="Emissions",
                            children=emissions.layout,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Costs",
                            children=costs.layout,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="GDP",
                            children=gdp.layout,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Damages",
                            children=damages.layout,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="All variables",
                            children=allvariables.layout,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Input parameters",
                            children=inputparams.layout,
                            selected_style=tab_selected_style,
                        ),
                        # dcc.Tab(label="IPOPT output", children="tab-content-6"),
                    ]
                )
            ]
        )
    ]
)
