from plotly.subplots import make_subplots
from common.dash import *
from common import data

import plotly.express as px

from app import app

layout = html.Div([
    dcc.Graph(
        id='tabs-emissions-plot'
    )
])


@app.callback(
    Output('tabs-emissions-plot', 'figure'),
    [Input('plot-selected-store', 'data')])
def update_plot(name):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate

    selection = df[df['Variable'].isin(['baseline', 'regional_emissions'])].set_index(['Variable', 'Region'])
    regions = list(selection.loc['regional_emissions'].index)

    fig = make_subplots(1, len(regions))#, subplot_titles=regions)

    for variable, color in zip(['baseline', 'regional_emissions'], ['cadetblue', 'mediumvioletred']):
        for i, (region, values) in enumerate(selection.loc[variable].iterrows()):
            fig.add_trace({
                'x': list(values.index),
                'y': list(values),
                'xaxis': f'x{i+1}',
                'yaxis': 'y1',
                'type': 'scattergl',
                'legendgroup': variable,
                'line': {'color': color},
                'name': variable,
                'showlegend': i==0
            })

    fig.update_xaxes(range=[2020,2100]).update_layout(
        margin={'l': 20, 'r': 20, 't': 50, 'b': 50},
        legend={'orientation': 'h', 'x': 0.5, 'xanchor': 'center'}
    )
    return fig
    