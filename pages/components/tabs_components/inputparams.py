from common.dash import *
from common import data

import pprint

from app import app

layout = html.Div([
    html.Br(),
    html.H4('Input parameters:'),
    html.Pre(id='tabs-inputparams-pre')
], className='tabs-plot-container')


@app.callback(
    Output('tabs-inputparams-pre', 'children'),
    [Input('plot-selected-store', 'data')])
def update_params(names):
    all_params = data.dataStore.get(names, params=True)
    if all_params is None:
        raise PreventUpdate
    html_elements = []
    for filename, params in all_params.items():
        html_elements.extend([
            html.H5(filename),
            html.Pre(pprint.pformat(params))
        ])
    return html_elements
