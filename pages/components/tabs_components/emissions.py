from common.dash import dash, dcc, dbc, html, Input, Output, PreventUpdate
from common import data

from pages.components.tabs_components import plotutils

import plotly.express as px

from app import app

layout = html.Div(
    [
        html.Br(),
        html.H4("Regional emissions, with baseline:"),
        dcc.Graph(id="tabs-regional-emissions-plot"),
        html.H4("Global emissions and temperature path:"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="tabs-global-emissions-plot"),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="tabs-global-temperature-plot"),
                    ]
                ),
            ]
        ),
    ],
    className="tabs-plot-container",
)


## Regional emissions
@app.callback(
    Output("tabs-regional-emissions-plot", "figure"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_plot_regional_emissions(names, timerange):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df,
        ["baseline", "regional_emissions"],
        timerange,
        yaxis_title="Emissions (GtCO<sub>2</sub>/yr)",
    )

    return fig


## Global emissions and cumulative emissions
@app.callback(
    Output("tabs-global-emissions-plot", "figure"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_plot_global_emissions(names, timerange):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df,
        ["global_emissions", "cumulative_emissions"],
        timerange,
        yaxis_title="Emissions (GtCO<sub>2</sub>/yr)",
        hidden_variables=["cumulative_emissions"],
        colors=[2, 3],
        height=350,
    )

    return fig


## Temperature
@app.callback(
    Output("tabs-global-temperature-plot", "figure"),
    [Input("plot-selected-store", "data"), Input("plot-timerange", "value")],
)
def update_plot_temperature(names, timerange):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df,
        ["temperature"],
        timerange,
        yaxis_title="GMST (above pre-industrial)",
        colors=[4],
        height=350,
    )

    return fig
