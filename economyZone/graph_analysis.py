# File: graph_analysis.py
# Aim: Analysis graph

import json
import pandas as pd
import pdb
import plotly.graph_objs as go

from tqdm.auto import tqdm

from . import beside
from . import config

# --------------------------------------------------------------------------------
# Load graph

# Load vertex
vertex_frame = pd.read_json(beside(config.get('Geography', 'filename')))
num = len(vertex_frame)

# Load edge
edge = json.load(open(beside('edge.json'), 'r'))
edge_frame = pd.DataFrame(edge, index=['Src']).transpose()
edge_frame['Dst'] = edge_frame.index.map(int)
edge_frame.index = range(len(edge_frame))
start_vertex = [e for e in range(num) if e not in edge_frame.Dst.values]
assert(len(start_vertex) == 1)
start_vertex = start_vertex[0]

print(f'Graph has {num} vertexes\n', vertex_frame)
print(f'Edge start vertex is {start_vertex}\n', edge_frame)

# --------------------------------------------------------------------------------
# Counting cities in province
print('Counting cities in province')
province_frame = pd.DataFrame(columns=['Count', 'Cities'])
for prov in tqdm(vertex_frame.Province.unique()):
    cities = vertex_frame.loc[vertex_frame.Province == prov].City.to_list()
    province_frame = province_frame.append(dict(
        Province=prov,
        Count=len(cities),
        Cities=cities),
        ignore_index=True)
province_frame.set_index('Province', drop=False, inplace=True)
province_frame.index.name = ''
print(province_frame)

# --------------------------------------------------------------------------------
# Counting the links of vertex
print('Counting links of vertex')
vertex_frame['Links'] = [[] for _ in range(num)]
for j in tqdm(edge_frame.index):
    src, dst = edge_frame.Src[j], edge_frame.Dst[j]
    vertex_frame.Links[src].append(dst)
    vertex_frame.Links[dst].append(src)

vertex_frame['LinksCount'] = vertex_frame.Links.map(len)
print('\n', vertex_frame)

# --------------------------------------------------------------------------------
# Display provinces
trace0 = go.Bar(dict(
    x=province_frame.Province,
    y=province_frame.Count,
    name='City Counting Bar',
    text=province_frame.Count,
    marker=dict(
        opacity=0.5,
        color='black',
    ),
))

trace1 = go.Scatter(dict(
    x=province_frame.Province,
    y=province_frame.Count,
    name='City Counting Line',
    mode='lines+markers',
    line=dict(
        shape='spline',
        color='gray',
    ),
    marker=dict(
        color=province_frame.Count,
        colorscale=[[0, 'green'], [0.5, 'orange'], [1.0, 'red']],
    ),
))


layout = go.Layout(
    xaxis=dict(title='xaxis', zeroline=False, rangeslider=dict(visible=True)),
    yaxis=dict(title='yaxis', zeroline=False),
    title='Title',
    showlegend=True,
)

fig = go.Figure(data=[trace0, trace1], layout=layout)
fig.show()
