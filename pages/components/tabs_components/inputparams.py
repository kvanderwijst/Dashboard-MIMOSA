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
def update_params(name):
    params = data.dataStore.getparams(name)
    if params is None:
        raise PreventUpdate
    return pprint.pformat(params)
