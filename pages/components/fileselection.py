"""
Provides the file selection dropdown and time range slider.

When multiple files are selected, this also shows a legend with
the line dash style for each file.
"""

import numpy as np

from app import app
from common import data
from common.dash import dbc, dcc, Input, Output, html, PreventUpdate


def all_experiments_options():
    options = []
    for filename in data.get_all_experiments():
        options.append({"label": filename, "value": filename})
    return options


layout_dropdown = dcc.Dropdown(
    id="plot-fileselection-filename",
    options=all_experiments_options(),
    multi=True,
)
layout_refreshbutton = dbc.Button(
    "Refresh", color="primary", id="plot-fileselection-refresh"
)
layout_rangeslider = dcc.RangeSlider(
    id="plot-timerange",
    min=2020,
    max=2100,
    step=10,
    value=[2020, 2100],
    marks={int(x): str(int(x)) for x in np.arange(2020, 2200, 10)},
)
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([html.P("Experiment:")], md=1),
                dbc.Col([layout_dropdown]),
                dbc.Col(
                    [layout_refreshbutton],
                    md=2,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([html.P("Time range:")], md=1),
                dbc.Col([layout_rangeslider]),
                dbc.Col([], md=2),
            ],
            style={"padding-top": "10px"},
        ),
        dcc.Store(id="plot-selected-store"),
    ]
)


@app.callback(
    Output("plot-selected-store", "data"),
    [Input("plot-fileselection-filename", "value")],
)
def update_store(names):
    # Put database in cache
    databases = data.dataStore.get(names)
    if databases is None or len(databases) == 0:
        raise PreventUpdate
    return names


@app.callback(
    Output("plot-fileselection-filename", "options"),
    [Input("plot-fileselection-refresh", "n_clicks")],
)
def update_options(n):
    if n is None or n == 0:
        raise PreventUpdate
    data.dataStore.reset()
    return all_experiments_options()


@app.callback(
    Output("plot-fileselection-filename", "value"),
    [Input("plot-fileselection-refresh", "n_clicks")],
)
def clear_filename(n):
    if n is None or n == 0:
        raise PreventUpdate
    return []


@app.callback(
    Output("plot-timerange", "max"), [Input("plot-fileselection-filename", "value")]
)
def update_range(names):
    databases = data.dataStore.get(names)
    if databases is None or len(databases) == 0:
        raise PreventUpdate
    return min(
        [
            max(
                single_df["data"]
                .drop(columns=["Variable", "Region"])
                .columns.to_numpy(dtype="float")
            )
            for single_df in databases.values()
        ]
    )
