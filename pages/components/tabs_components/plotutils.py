from common.dash import *
from common import data

import plotly.express as px

def create_plot(df_dict, variables, timerange, stackgroup={}, yaxis_title='', tickformat=None, height=450, hidden_variables=[], colors=None, percapita=False):

    filenames = list(df_dict.keys())
    databases = list(df_dict.values())

    possible_line_styles = ['solid', 'dot', 'dash', 'dashdot', 'longdash', 'longdashdot']

    traces = []

    for df_i, (df, line_dash) in enumerate(zip(databases, possible_line_styles)):

        selection = df[df['Variable'].isin(variables)]
        regions = list(selection['Region'].unique())

        regions_to_axis = {region: f'x{i+1}' for i, region in enumerate(regions)}

        if percapita:
            population_factor = df[df['Variable'] == 'population'].drop(columns='Variable').set_index('Region')
        else:
            population_factor = 1

        for var_i, (variable, subselection) in enumerate(selection.groupby('Variable')):
            
            # Color list * 3 to get the same colours repeated three times, such that it never runs out of range
            color = (px.colors.qualitative.Plotly*3)[var_i if colors is None else colors[var_i]]

            subselection = subselection.drop(columns='Variable').set_index('Region') / population_factor

            for region_i, (region, values) in enumerate(subselection.loc[:,str(timerange[0]):str(timerange[1])].iterrows()):
                traces.append({
                    'type': 'scatter',
                    'x': [float(x) for x in values.index],
                    'y': list(values),
                    'xaxis': regions_to_axis[region], 'yaxis': 'y1',
                    'line': {'color': color, 'dash': line_dash},
                    'mode': 'lines',
                    'name': variable, 'legendgroup': variable,
                    'showlegend': region_i==0 and df_i==0,
                    'visible': 'legendonly' if variable in hidden_variables else None,
                    'stackgroup': stackgroup.get(variable),
                })
        
        minyear = float(values.index[0])

    fig = {
        'data': traces,
        'layout': {
            'grid': {
                'columns': len(regions),
                'rows': 1
            },
            'yaxis1': {'title': yaxis_title + (' (per capita) [UNIT?]' if percapita else '')},
            'margin': {'l': 50, 'r': 20, 't': 50, 'b': 30},
            'legend': {'orientation': 'h', 'x': 0.5, 'xanchor': 'center', 'y': -0.15},
            'height': height,
            'annotations': [
                {
                    'text': region,
                    'showarrow': False,
                    'xref': 'paper', 'yref': 'paper',
                    'xanchor': 'center', 'yanchor': 'middle',
                    'x': (i+0.5) / len(regions), 'y': 1+0.05*450/height,
                    'font': {'size': 16}
                } for i, region in enumerate(regions)
            ],
            'shapes': [
                {
                    'type': 'line',
                    'yref': 'paper', 'xref': f'x{i+1}',
                    'x0': minyear, 'x1': minyear,
                    'y0': 0, 'y1': 1,
                    'line': {'width': 1, 'color': '#666'}
                }
                for i in range(len(regions))
            ]
        }
    }

    if tickformat is not None:
        for region_i in range(len(regions)):
            yaxis = f'yaxis{region_i+1}'
            if yaxis not in fig['layout']:
                fig['layout'][yaxis] = {}
            fig['layout'][yaxis]['tickformat'] = tickformat

    return fig

