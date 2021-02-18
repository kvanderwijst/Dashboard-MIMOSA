from common.dash import *
from common import data

from pages.components.tabs_components import plotutils

from app import app

layout = html.Div([
    html.Br(),
    html.H4('Residual vs gross damage costs, with adaptation costs'),
    dcc.Graph(
        id='tabs-damages-main-plot'
    ),
    html.H4('Adaptation level (top) and stock vs flow (bottom):'),
    dcc.Graph(
        id='tabs-damages-adaptlevel-plot'
    ),
    dcc.Graph(
        id='tabs-damages-adaptcosts-plot'
    ),
    html.H4('Sea level rise:'),
    dcc.Graph(
        id='tabs-damages-SLR-plot'
    ),
], className='tabs-plot-container')


## Residual vs gross damage costs
@app.callback(
    Output('tabs-damages-main-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_damages_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['adapt_costs', 'resid_damages', 'gross_damages', 'SLR_damages'], 
        timerange, 
        stackgroup={'adapt_costs': 'costs', 'resid_damages': 'costs'},
        yaxis_title='Costs (% GDP)', 
        tickformat='%'
    )
    return fig


## Adaptation level
@app.callback(
    Output('tabs-damages-adaptlevel-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_adaptlevel_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['adapt_level'], 
        timerange, 
        colors=[4],
        height=250
    )
    return fig


## Adaptation costs disaggregation
@app.callback(
    Output('tabs-damages-adaptcosts-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_adaptlevel_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['adapt_FAD', 'adapt_IAD', 'adapt_SAD'], 
        timerange,
        hidden_variables=['adapt_SAD'],
        height=250,
        yaxis_title='Costs (% GDP)', 
        tickformat='%',
        colors=[5,6,7]
    )
    return fig


## Sea level rise
@app.callback(
    Output('tabs-damages-SLR-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_SLR_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['SLR', 'CUMGSIC', 'CUMGIS', 'total_SLR'], 
        timerange, 
        stackgroup={'SLR': 'SLR', 'CUMGSIC': 'SLR', 'CUMGIS': 'SLR'},
        yaxis_title='SLR (in meter)',
        hidden_variables=['total_SLR'],
        colors=[8,9,10,11]
    )
    return fig
