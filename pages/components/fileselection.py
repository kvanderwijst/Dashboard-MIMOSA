from common.dash import *
from common import data

import numpy as np

from app import app

def all_experiments_options():
    options = []
    for path in data.get_all_experiments():
        filename = path.split(data.DATA_DIRECTORY)[1]
        options.append({'label': filename, 'value': filename})
    return options

layout = html.Div([
    dbc.Row([
        dbc.Col([html.P('Experiment:')], md=3),
        dbc.Col([
            dcc.Dropdown(
                id="plot-fileselection-filename",
                options=all_experiments_options()
            )
        ]),
        dbc.Col([dbc.Button('Refresh', color='primary', id='plot-fileselection-refresh')], md=2),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([html.P('Time range:')], md=3),
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
    ]),
    dcc.Store(id='plot-selected-store')
])



@app.callback(
    Output('plot-selected-store', 'data'),
    [Input('plot-fileselection-filename', 'value')])
def update_store(name):
    # Put database in cache
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate
    return name

@app.callback(
    Output('plot-timerange', 'max'),
    [Input('plot-fileselection-filename', 'value')])
def update_range(name):
    df = data.dataStore.get(name)
    if df is None:
        raise PreventUpdate
    return max(df.drop(columns=['Variable', 'Region']).columns.to_numpy(dtype='float'))
