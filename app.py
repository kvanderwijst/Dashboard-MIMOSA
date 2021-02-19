from common.dash import *
from pages import plot

external_stylesheets = [dbc.themes.BOOTSTRAP]
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.FLATLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='common-lastmodified-store')
], className="p-5", fluid=True)  


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