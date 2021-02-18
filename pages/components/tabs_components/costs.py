from plotly.subplots import make_subplots
from common.dash import *
from common import data

import plotly.express as px

from app import app

layout = html.Div([
    dcc.Graph(
        id='tabs-costs-plot'
    )
])


@app.callback(
    Output('tabs-costs-plot', 'figure'),
    [Input('plot-selected-store', 'data')])
def update_plot(name):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    variables = ['rel_abatement_costs', 'resid_damages', 'adapt_costs']

    selection = df[df['Variable'].isin(variables)]

    regions = list(selection['Region'].unique())
    fig = make_subplots(1, len(regions), subplot_titles=regions)

    for (variable, subselection), color in zip(selection.groupby('Variable'), px.colors.qualitative.Plotly):
        for i, (region, values) in enumerate(subselection.set_index('Region').iterrows()):
            fig.add_trace({
                'x': list(values.index),
                'y': list(values),
                'xaxis': f'x{i+1}',
                'yaxis': 'y1',
                'type': 'scatter',
                'line': {'color': color},
                'stackgroup': 'costs',
                'legendgroup': variable,
                'name': variable,
                'showlegend': i==0
            })

    fig.update_xaxes(range=[2020,2100]).update_layout(
        margin={'l': 20, 'r': 20, 't': 50, 'b': 50},
        legend={'orientation': 'h', 'x': 0.5, 'xanchor': 'center'}
    )
    return fig
    