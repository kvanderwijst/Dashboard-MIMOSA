from common.dash import *
from common import data

from pages.components.tabs_components import plotutils

import plotly.express as px

from app import app

layout = html.Div([
    html.Br(),
    html.H4('Regional emissions, with baseline:'),
    dcc.Graph(
        id='tabs-regional-emissions-plot'
    ),
    html.H4('Global emissions and temperature path:'),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='tabs-global-emissions-plot'
            ),
        ]),
        dbc.Col([
            dcc.Graph(
                id='tabs-global-temperature-plot'
            ),
        ])
    ])
    
], className='tabs-plot-container')


@app.callback(
    Output('tabs-regional-emissions-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate
    
    fig = plotutils.create_plot(
        df, 
        ['baseline', 'regional_emissions'], 
        timerange, 
        yaxis_title='Emissions (GtCO<sub>2</sub>/yr)'
    )
    
    return fig


@app.callback(
    Output('tabs-global-emissions-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate
    
    fig = plotutils.create_plot(
        df, 
        ['global_emissions'], 
        timerange, 
        yaxis_title='Emissions (GtCO<sub>2</sub>/yr)'
    )

    return fig
    