from common.dash import *
from common import data

from pages.components.tabs_components import plotutils

from app import app

layout = html.Div([
    html.Br(),
    html.H4('Regional relative adaptation costs, abatement costs and residual damages'),
    html.Div(id='tabs-costs-plots'),
    
    html.H4('Regional carbon prices'),
    dcc.Graph(
        id='tabs-costs-carbonprices-plot'
    ),
    html.H4('Learning factors'),
    dcc.Graph(
        id='tabs-costs-learning-plot'
    ),
], className='tabs-plot-container')


## Regional costs (adaptation+abatement+resid damages)
@app.callback(
    Output('tabs-costs-plots', 'children'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_costs_plot(names, timerange):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate

    figs = [
        dcc.Graph(
            figure=plotutils.create_plot(
                {filename: single_df}, 
                ['rel_abatement_costs', 'resid_damages', 'adapt_costs'], 
                timerange, 
                stackgroup={'rel_abatement_costs': 'costs', 'resid_damages': 'costs', 'adapt_costs': 'costs'}, 
                yaxis_title='Costs (% GDP)', 
                tickformat='p',
                height=max(150, plotutils.DEFAULT_HEIGHT/len(df))
            )
        )
        for filename, single_df in df.items()
    ]
    return figs


## Carbon prices
@app.callback(
    Output('tabs-costs-carbonprices-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_carbonprices_plot(names, timerange):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['carbonprice'], 
        timerange, 
        yaxis_title='TODO',
        colors=[3],
        height=250
    )
    return fig

## Learning factors
@app.callback(
    Output('tabs-costs-learning-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_learning_plot(names, timerange):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate

    fig = plotutils.create_plot(
        df, 
        ['learning_factor', 'LBD_factor', 'LOT_factor'], 
        timerange, 
        colors=[4, 5, 6],
        height=250
    )
    return fig
