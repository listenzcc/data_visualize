# File: web_app.py
# Aim: Provide web-based Dash App

import random
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
app = dash.Dash(__name__)
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
data = pd.read_csv('iris.data', names=names)

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

app.layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
                id='ddl_x',
                options=[{'label': i, 'value': i} for i in names],
                value=names[0],
                # style={'width': '50 %'}
            ),
            dcc.Dropdown(
                id='ddl_y',
                options=[{'label': i, 'value': i} for i in names],
                value=names[1],
                # style={'width': '50 %'}
            ),
        ], style={'width': '100 % ', 'display': 'block'}),
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
    for prov in data.Province.unique():
        df = data.loc[data.Province == prov]
        trace_lst.append(go.Scatter(x=df[ddl_x_value],
                                    y=df[ddl_y_value],
                                    text=df.Province + ', ' + df.City,
                                    mode='markers',
                                    name=prov))

    for prov in data.Province.unique():
        df = data.loc[data.Province == prov]
        trace_lst.append(go.Scattermapbox(lon=df[ddl_x_value],
                                          lat=df[ddl_y_value],
                                          text=df.Province + ', ' + df.City,
                                          mode='markers',
                                          name=prov))

    # trace_lst = [go.Scatter(x=[ddl_x_value],
    #                         y=data.loc[data.Province == prov][ddl_y_value],
    #                         text=[prov for _ in range(
    #                             len(data.loc[data.Province == prov]))],
    #                         mode='markers',
    #                         name=prov)
    #              for prov in data.Province.unique()]

    # trace_lst = [go.Scatter(x=data[data['class'] == cls][ddl_x_value],
    #                         y=data[data['class'] == cls][ddl_y_value],
    #                         mode='markers',
    #                         marker={'size': 15},
    #                         name=cls)
    #              for cls in data['class'].unique()]

    layout = go.Layout(width=styles['width'],
                       height=styles['height'],
                       hovermode='closest',
                       title=go.layout.Title(
                           text='Dash Interactive Data Visualization', xref='paper', x=0))

    return go.Figure(data=trace_lst, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
