# File: web_app.py
# Aim: Provide web-based Dash App

import plotly.figure_factory as ff
import random
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
app = dash.Dash(__name__)


data = pd.read_json('./geographic_frame.json')
data['Lat'] = data.Position.map(lambda x: x[0])
data['Lon'] = data.Position.map(lambda x: x[1])
data = data[['Lat', 'Lon', 'Province', 'City']]
names = data.columns
describe = data.describe()
print(describe)
styles = dict(
    width=(describe.Lat['max'] - describe.Lat['min']) * 20,
    height=(describe.Lon['max'] - describe.Lon['min']) * 20
)

control_x = html.Div([html.H2('X:',
                              style={'text-align': 'center', 'width': '50px', 'margin': '5px'}),
                      dcc.Dropdown(id='ddl_x',
                                   options=[{'label': i, 'value': i}
                                            for i in names],
                                   value=names[0],
                                   style={'width': '100px'})],
                     className='controller')

control_y = html.Div([html.H2('Y:',
                              style={'text-align': 'center', 'width': '50px', 'margin': '5px'}),
                      dcc.Dropdown(id='ddl_y',
                                   options=[{'label': i, 'value': i}
                                            for i in names],
                                   value=names[1],
                                   style={'width': '100px'})],
                     className='controller')

app.layout = html.Div(
    [
        html.Div([
            control_x,
            control_y,
        ], id='control-area'),
        html.Div([
            dcc.Graph(id='graph1')
        ], style={'width': '800px', 'display': 'block'})
    ]
)


@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [
        Input(component_id='ddl_x', component_property='value'),
        Input(component_id='ddl_y', component_property='value')
    ]
)
def update_output(ddl_x_value, ddl_y_value):
    print(data)
    trace_lst = []
    # for prov in data.Province.unique():
    #     df = data.loc[data.Province == prov]
    #     trace_lst.append(go.Scatter(x=df[ddl_x_value],
    #                                 y=df[ddl_y_value],
    #                                 text=df.Province + ', ' + df.City,
    #                                 mode='markers',
    #                                 name=prov))

    for prov in data.Province.unique():
        df = data.loc[data.Province == prov]
        trace_lst.append(go.Scattergeo(lon=df[ddl_x_value],
                                       lat=df[ddl_y_value],
                                       text=df.Province + ', ' + df.City,
                                       name=prov,
                                       mode='markers',
                                       marker=dict(opacity=0.5),
                                       ))

    # trace_lst.append(go.Scattergeo(
    #     lon=[0, 10],
    #     lat=[0, 20],
    #     mode='lines',
    #     line=dict(width=1, color='red'),
    # ))

    layout = go.Layout(width=styles['width'],
                       height=styles['height'],
                       hovermode='closest',
                       title=go.layout.Title(
        text='Dash Interactive Data Visualization', xref='paper', x=0))

    fig = go.Figure(data=trace_lst, layout=layout)

    projection_type = 'natural earth'
    # projection_type = 'orthographic'

    fig.update_geos(fitbounds='locations',
                    # resolution=50,
                    projection_type=projection_type,
                    lataxis_showgrid=True, lonaxis_showgrid=True,
                    showcountries=True, countrycolor='Black',
                    showsubunits=True, subunitcolor='Blue',
                    showland=True, landcolor='rgb(130, 75, 26)',
                    showocean=True, oceancolor='DarkBlue',
                    showlakes=True, lakecolor='rgb(100, 200, 200)',
                    showrivers=True, rivercolor='Blue',
                    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
