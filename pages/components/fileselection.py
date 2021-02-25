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
        html.Div(id="legend-plot-row"),
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


@app.callback(
    Output("legend-plot-row", "children"),
    [Input("plot-fileselection-filename", "value")],
)
def update_legend(names):
    databases = data.dataStore.get(names)
    if (
        databases is None or len(databases) <= 1
    ):  # Only update when multiple files are selected
        return []

    fig = {
        "data": [
            {
                "type": "scatter",
                "x": [None],
                "y": [None],
                "mode": "lines",
                "name": name,
                "line": {
                    "color": "black",
                    "dash": single_df["meta"]["line_dash"],
                },
            }
            for name, single_df in databases.items()
        ],
        "layout": {
            "height": 30 * np.ceil(len(names) / 2),
            "margin": {"t": 0, "l": 0, "r": 0, "b": 0},
            "legend": {
                "orientation": "h",
                "y": 0.5,
                "yanchor": "middle",
            },
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "xaxis": {
                "showgrid": False,
                "zeroline": False,
                "visible": False,
            },
            "yaxis": {
                "showgrid": False,
                "zeroline": False,
                "visible": False,
            },
        },
    }

    return [
        dbc.Row(
            [
                dbc.Col([html.P("Legend:")], md=1),
                dbc.Col([dcc.Graph(figure=fig)]),
            ]
        )
    ]
