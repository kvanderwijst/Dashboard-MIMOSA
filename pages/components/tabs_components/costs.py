from common.dash import *
from common import data

from pages.components.tabs_components import plotutils

from app import app

layout = html.Div([
    dcc.Graph(
        id='tabs-costs-plot'
    )
], className='tabs-plot-container')


@app.callback(
    Output('tabs-costs-plot', 'figure'),
    [Input('plot-selected-store', 'data'), Input('plot-timerange', 'value')])
def update_plot(name, timerange):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    return plotutils.create_plot(df, ['rel_abatement_costs', 'resid_damages', 'adapt_costs'], timerange, stackgroup='costs', yaxis_title='Costs (% GDP)', tickformat='%')
