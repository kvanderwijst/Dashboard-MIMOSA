from common.dash import *
from common import data

import numpy as np

from app import app

def all_experiments_options():
    options = []
    for filename in data.get_all_experiments():
        options.append({'label': filename, 'value': filename})
    return options

layout = html.Div([
    dbc.Row([
        dbc.Col([html.P('Experiment:')], md=1),
        dbc.Col([
            dcc.Dropdown(
                id="plot-fileselection-filename",
                options=all_experiments_options(),
                multi=True
            )
        ]),
        dbc.Col([dbc.Button('Refresh', color='primary', id='plot-fileselection-refresh')], md=2),
    ]),
    html.Div(id='legend-plot-row'),
    dbc.Row([
        dbc.Col([html.P('Time range:')], md=1),
        dbc.Col([
            dcc.RangeSlider(
                id="plot-timerange",
                min=2020,
                max=2100,
                step=10,
                value=[2020, 2100],
                marks={int(x): str(int(x)) for x in np.arange(2020, 2200, 10)}
            )
        ]),
        dbc.Col([], md=2),
    ], style={'padding-top': '10px'}),
    dcc.Store(id='plot-selected-store')
])



@app.callback(
    Output('plot-selected-store', 'data'),
    [Input('plot-fileselection-filename', 'value')])
def update_store(names):
    # Put database in cache
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate
    return names

@app.callback(
    Output('plot-timerange', 'max'),
    [Input('plot-fileselection-filename', 'value')])
def update_range(names):
    df = data.dataStore.get(names)
    if df is None or len(df) == 0:
        raise PreventUpdate
    return min([
        max(single_df['data'].drop(columns=['Variable', 'Region']).columns.to_numpy(dtype='float')) 
        for single_df in df.values()
    ])


@app.callback(
    Output('legend-plot-row', 'children'),
    [Input('plot-fileselection-filename', 'value')])
def update_legend(names):
    df = data.dataStore.get(names)
    if df is None or len(df) <= 1: # Only update when multiple files are selected
        return []

    return [
        dbc.Row([
            dbc.Col([html.P('Legend:')], md=1),
            dbc.Col([dcc.Graph(figure={
                'data': [
                    {
                        'type': 'scatter',
                        'x': [None], 'y': [None],
                        'mode': 'lines',
                        'name': name,
                        'line': {'color': 'black', 'dash': single_df['meta']['line_dash']}
                    }
                    for name, single_df in df.items()
                ],
                'layout': {
                    'height': 30*np.ceil(len(names)/2),
                    'margin': {'t': 0, 'l': 0, 'r': 0, 'b': 0},
                    'legend': {
                        'orientation': 'h',
                        'y': 0.5,
                        'yanchor': 'middle'
                    },
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'xaxis': {'showgrid': False, 'zeroline': False, 'visible': False},
                    'yaxis': {'showgrid': False, 'zeroline': False, 'visible': False},
                }
            })])
        ])
    ]
