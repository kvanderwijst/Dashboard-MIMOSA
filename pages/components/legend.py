"""
Provides a table with the differences between the selected scenarios.
"""

import pandas as pd
from app import app
from common import data
from common.dash import dbc, dcc, Input, Output, html


layout = dbc.Row(
    [
        dbc.Col(html.P("Legend:"), md=1),
        dbc.Col(html.Div(id="legend-table")),
        dbc.Col([], md=2),
    ]
)


@app.callback(
    Output("legend-table", "children"),
    [Input("plot-fileselection-filename", "value")],
)
def update_legend(names):
    all_params = data.dataStore.get(names, params=True)
    if (
        all_params is None or len(all_params) <= 1
    ):  # Only update when multiple files are selected
        return []

    differences = param_differences(all_params)

    headers = [
        html.Th(create_empty_legend(name, all_params[name]["meta"]["line_dash"]))
        for name in differences.columns
    ]
    table_header = [html.Thead(html.Tr([html.Td("Differences:")] + headers))]

    rows = [
        html.Tr([html.Th(param)] + [html.Td(str(value)) for value in row])
        for param, row in differences.iterrows()
    ]

    table_body = [html.Tbody(rows)]

    return dbc.Table(table_header + table_body, size="sm", hover=True)


def create_empty_legend(name, dash):
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
                    "dash": dash,
                },
                "showlegend": True,
            }
        ],
        "layout": {
            "height": 30,
            "width": 200,
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

    return dcc.Graph(figure=fig)


def param_differences(all_params) -> pd.DataFrame:
    # First, flatten the nested parameter dictionaries
    flattened = {
        name: flatten(single_params["data"])
        for name, single_params in all_params.items()
    }

    differences = {}

    # Loop through each flattened dict to find differences
    all_keys = [set(x.keys()) for x in flattened.values()]
    keys_union = set.union(*all_keys)
    keys_intersect = set.intersection(*all_keys)
    keys_difference = keys_union - keys_intersect

    for key in keys_intersect:
        # Check if all values are equal
        unique_values = set(params[key] for params in flattened.values())
        if len(unique_values) > 1:
            keys_difference.add(key)

    # Loop through each key_difference to get the respective values
    differences = {
        key: {name: params.get(key, "") for name, params in flattened.items()}
        for key in keys_difference
    }

    return pd.DataFrame(differences).T


def recursive_traverse(name, subset, flattened):
    for key, value in subset.items():
        if key not in ["regions", "regionstype"]:  # Regions are checked separately
            newname = f"{name} - {key}" if name != "" else key
            if type(value) == dict:
                recursive_traverse(newname, value, flattened)
            else:
                flattened[newname] = value


def flatten(dictionary):
    flattened = {}
    recursive_traverse("", dictionary, flattened)
    return flattened