from common.dash import *

from app import app
from pages import plot


app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='common-lastmodified-store')
], className="p-5")  


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return plot.layout
    # if pathname == '/settings':
    #     return settings.layout
    # else:
    #     return main.layout

if __name__ == '__main__':
    app.run_server(debug=True)