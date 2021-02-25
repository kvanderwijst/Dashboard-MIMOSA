"""
Tab for the Damages plots:
 - Residual vs gross damages + adapt costs
 - Adaptation level
 - Stock vs flow adaptation
 - Sea level rise
"""

from common.dash import dcc, html, Input, Output, PreventUpdate
from common import data

from pages.components.tabs_components import plotutils

from app import app

layout = html.Div(
    [
        html.Br(),
        html.H4("Residual vs gross damage costs, with adaptation costs"),
        html.Div(id="tabs-damages-main-plots"),
        html.H4("Adaptation level (top) and stock vs flow (bottom):"),
        dcc.Graph(id="tabs-damages-adaptlevel-plot"),
        dcc.Graph(id="tabs-damages-adaptcosts-plot"),
        html.H4("Sea level rise:"),
        html.Div(id="tabs-damages-SLR-plots"),
    ],
    className="tabs-plot-container",
)


## Residual vs gross damage costs
@app.callback(
    Output("tabs-damages-main-plots", "children"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_damages_plot(names, timerange):
    databases = data.dataStore.get(names)
    if databases is None or len(databases) == 0:
        raise PreventUpdate

    figs = [
        dcc.Graph(
            figure=plotutils.create_plot(
                {filename: single_df},
                ["adapt_costs", "resid_damages", "gross_damages", "SLR_damages"],
                timerange,
                stackgroup={"adapt_costs": "costs", "resid_damages": "costs"},
                yaxis_title="Costs (% GDP)",
                tickformat="p",
                height=max(150, plotutils.DEFAULT_HEIGHT / len(databases)),
            )
        )
        for filename, single_df in databases.items()
    ]
    return figs


## Adaptation level
@app.callback(
    Output("tabs-damages-adaptlevel-plot", "figure"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_adaptlevel_plot(names, timerange):
    databases = data.dataStore.get(names)
    if databases is None or len(databases) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        databases, ["adapt_level"], timerange, colors=[4], height=250
    )
    return fig


## Adaptation costs disaggregation
@app.callback(
    Output("tabs-damages-adaptcosts-plot", "figure"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_adaptcosts_plot(names, timerange):
    databases = data.dataStore.get(names)
    if databases is None or len(databases) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        databases,
        ["adapt_FAD", "adapt_IAD", "adapt_SAD"],
        timerange,
        hidden_variables=["adapt_SAD"],
        height=250,
        yaxis_title="Costs (% GDP)",
        tickformat="p",
        colors=[5, 6, 7],
    )
    return fig


## Sea level rise
@app.callback(
    Output("tabs-damages-SLR-plots", "children"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_slr_plot(names, timerange):
    databases = data.dataStore.get(names)
    if databases is None or len(databases) == 0:
        raise PreventUpdate

    figs = [
        dcc.Graph(
            figure=plotutils.create_plot(
                {filename: single_df},
                ["SLR", "CUMGSIC", "CUMGIS", "total_SLR"],
                timerange,
                stackgroup={"SLR": "SLR", "CUMGSIC": "SLR", "CUMGIS": "SLR"},
                yaxis_title="SLR (in meter)",
                hidden_variables=["total_SLR"],
                colors=[8, 9, 10, 11],
                height=max(150, plotutils.DEFAULT_HEIGHT / len(databases)),
            )
        )
        for filename, single_df in databases.items()
    ]
    return figs
