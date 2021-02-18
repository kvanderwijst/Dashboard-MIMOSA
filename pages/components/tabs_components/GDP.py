from common.dash import *
from common import data

from pages.components.tabs_components import plotutils

from app import app

layout = html.Div([
    html.Br(),
    html.H4('GDP, capital stock and consumption:'),
    dbc.RadioItems(
        options=[{'label': 'Absolute', 'value': False}, {'label': 'Per capita', 'value': True}],
        value=False,
        inline=True,
        id='tabs-GDP-percapita'
    ),
    dcc.Graph(
        id='tabs-GDP-plot'
    ),
    html.H4('Utility:'),
    dcc.Graph(
        id='tabs-GDP-utility-plot'
    ),
], className='tabs-plot-container')


## GDP, capital stock and consumption
@app.callback(
    Output('tabs-GDP-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value'), Input('tabs-GDP-percapita', 'value')])
def update_GDP_plot(name, timerange, percapita):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['GDP_gross', 'GDP_net', 'capital_stock', 'consumption'], 
        timerange, 
        yaxis_title='trillion US$2005/yr',
        percapita=percapita
    )
    return fig


## Carbon prices
@app.callback(
    Output('tabs-GDP-utility-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_utility_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['utility'], 
        timerange, 
        colors=[4]
    )
    return fig
