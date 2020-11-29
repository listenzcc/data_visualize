# File: draw_graph.py
# Aim: Draw the graph using "geographic_frame.json" and "edge.json"
# * "geographic_frame.json" is generated from "load_location_json.py"
# * "edge.json" is generated from "geographic_analysis.py"


# -----------------------------------------------------------------------
import json
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex as rgb2hex
import numpy as np
import pandas as pd
import pdb
import seaborn as sns

from tqdm.auto import tqdm, trange

from . import beside
from . import logger
from . import config

colormap_name = 'icefire'

# -----------------------------------------------------------------------
# Load geographic info,
# columns are Province | City | Position
geo_frame = pd.read_json(beside(config.get('Geography', 'filename')))
edge = json.load(open(beside('edge.json'), 'r'))

print('Geographic info')
print(geo_frame)

# -----------------------------------------------------------------------
# Make colormap
provinces = geo_frame.Province.unique()
colors = sns.color_palette(colormap_name, n_colors=len(provinces))
colormap = dict()
for j, prov in enumerate(provinces):
    colormap[prov] = rgb2hex(colors[j])
print('Colormap')
print(colormap)

# -----------------------------------------------------------------------
# Draw the graph

# Make property DataFrame,
# geo_frame: Add Longitude and Latitude to the frame,
#            new frame has columns: Province | City | Position | Lon | Lat
# edge_frame: DataFrame of lines,
#             columns: Unit | Name | Lon | Lat | Province
#                      Unit: the unit part used as the unique dst for sns.lineplot unit
#                      Name: src or dst
#                      Province: province name of the dst
#                      thus, there are 2 records for one path, one for src and another for dst
geo_frame['Lon'] = geo_frame.Position.map(lambda x: x[0])
geo_frame['Lat'] = geo_frame.Position.map(lambda x: x[1])
geo_frame['Color'] = geo_frame.Province.map(lambda x: colormap[x])
print('Geographic frame:\n', geo_frame)

edge_frames = dict()
for name, iterator in zip(['src', 'dst'],
                          [edge.keys(), edge.values()]):
    df = pd.DataFrame(iterator)
    df.columns = ['Unit']
    df['Idx'] = df.Unit
    df['Name'] = name
    for col in ['Lon', 'Lat', 'Province']:
        df[col] = df['Unit'].map(lambda x: geo_frame[col].loc[int(x)])
    edge_frames[name] = df

edge_frames['src']['Unit'] = edge_frames['dst']['Unit']
edge_frames['src']['Province'] = edge_frames['dst']['Province']
edge_frame = pd.concat([edge_frames['src'], edge_frames['dst']])
print('Edge frame:\n', edge_frame)

# Draw
# Prepare canvas
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
# Add vertexes in scatters as city
sns.scatterplot(data=geo_frame, x='Lon', y='Lat',
                hue=geo_frame.Province.to_list(),
                palette=colormap,
                picker=5,
                ax=ax)

# Add edges in lines as road
sns.lineplot(data=edge_frame, x='Lon', y='Lat',
             units=edge_frame.Unit.to_list(), estimator=None,
             hue=edge_frame.Province.to_list(),
             palette=colormap,
             ax=ax)

# Compute ratio of the graphic
width = geo_frame.Lon.max() - geo_frame.Lon.min()
height = geo_frame.Lat.max() - geo_frame.Lat.min()
# The "/2" is because the lat is of 0 ~ 90 degrees,
#                         lon is of 0 ~ 180 degrees
ratio = height / width * 2
print(f'Setting aspect to {ratio}')
ax.set_aspect(ratio)

ax.set_title('Graph of global shortest length')

idx = 0
se = geo_frame.loc[idx]
note = ax.plot(se['Lon'], se['Lat'], marker='o', c='black')


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))


def onpick(event):
    # picked = event.artist
    idx = event.ind[0]
    se = geo_frame.loc[idx]
    print(se)
    note[0].set_data(se['Lon'], se['Lat'])
    # fig.canvas.draw()
    ax.redraw_in_frame()
    ax.draw_artist(note[0])
    fig.canvas.blit(ax.bbox)


cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('pick_event', onpick)
plt.show(block=False)

input('Press "Enter" to exit.')
