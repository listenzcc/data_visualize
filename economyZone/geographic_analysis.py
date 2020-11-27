# File: geographic_analysis.py
# Aim: Necessary geographic analysis
# * Compute neighborhood links between cities, using global shortest method.

# -----------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
import seaborn as sns

from tqdm.auto import tqdm, trange

from . import beside
from . import logger
from . import config

# -----------------------------------------------------------------------
# Load geographic info,
# columns are Province | City | Position
geo_frame = pd.read_json(beside(config.get('Geography', 'filename')))
print('Geographic info')
print(geo_frame)

num = len(geo_frame)
posi = np.array(geo_frame.Position.to_list())

# -----------------------------------------------------------------------
# Generate [matrix] as num x num matrix
matrix = np.zeros((num, num))
print('Computing distance matrix')
for i in tqdm(range(num)):
    matrix[i] = np.linalg.norm(posi - posi[i], axis=1)
matrix += np.diag([np.nan for _ in range(num)])

# -----------------------------------------------------------------------
# Build shortest global path


class ShortestPathGraph(object):
    # Generating mapping graph across all the vertex
    def __init__(self, matrix):
        # [matrix] is the distance matrix of all the vertex
        self.matrix = matrix.copy()
        self.matrix[np.isnan(self.matrix)] = np.inf

    def generate_path(self, src):
        # Start generating the shortest path,
        # [src] is the beginning vertex
        # Init variables,
        # num: number of vertex,
        # remain: remaining of unlinked vertexes,
        # min_path: path dict from linked vertexes to remaining vertexes,
        # self.edge: Generated graph edges, format is "des: src" refers from [src] to [des]
        num = len(matrix)
        remain = [e for e in range(num)]
        min_path = dict()
        self.edge = dict()

        # Init the graph from the [src] vertex
        remain.remove(src)

        def _update_min_path(idx):
            # Built in method,
            # update or insert [idx] item into [min_path] dict
            coord = np.argmin(self.matrix[idx][remain])
            min_path[idx] = (matrix[idx][remain][coord],
                             remain[coord])

        _update_min_path(src)

        # Iteration starts,
        # generate the graph using shortest global length method
        print('Generating shortest path graph')
        for _ in trange(num-1):
            # Find shortest path from [src] to [des]
            des_tuple = sorted(min_path.items(), key=lambda x: x[1][0])[0]
            src = des_tuple[0]
            des = des_tuple[1][1]
            # Record path
            self.edge[des] = src
            remain.remove(des)
            if len(remain) == 0:
                break
            # Update src and insert des in min_path dict
            # _update_min_path(src)
            _update_min_path(des)
            for s in min_path:
                if min_path[s][1] == des:
                    _update_min_path(s)


spg = ShortestPathGraph(matrix)
spg.generate_path(0)
print(len(spg.edge))

# -----------------------------------------------------------------------
# Draw the graph

# Make property DataFrame,
# geo_frame: Add Longitude and Latitude to the frame,
#            new frame has columns: Province | City | Position | Lon | Lat
# edge_frame: DataFrame of lines,
#             columns: Dst or Src | Name | Lon | Lat | Province
#                      Dst and Src: the Dst idx of the path
#                      Name: src or dst
#                      Province: province name of the dst
#                      thus, there are 2 records for one path, one for src and another for dst
geo_frame['Lon'] = geo_frame.Position.map(lambda x: x[0])
geo_frame['Lat'] = geo_frame.Position.map(lambda x: x[1])

edge_frames = dict()
for name, iterator in zip(['src', 'dst'],
                          [spg.edge.keys(), spg.edge.values()]):
    df = pd.DataFrame(iterator)
    df.columns = ['Dst']
    df['Name'] = name
    for col in ['Lon', 'Lat', 'Province']:
        df[col] = df['Dst'].map(lambda x: geo_frame[col].loc[x])
    edge_frames[name] = df

edge_frames['src']['Dst'] = edge_frames['dst']['Dst']
edge_frames['src']['Province'] = edge_frames['dst']['Province']
edge_frame = pd.concat([edge_frames['src'], edge_frames['dst']])

# Draw
# Prepare canvas
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
# Add vertexes in scatters as city
sns.scatterplot(data=geo_frame, x='Lon', y='Lat',
                hue=geo_frame.Province.to_list(), ax=ax)
# Add edges in lines as road
sns.lineplot(data=edge_frame, x='Lon', y='Lat',
             units=edge_frame.Dst.to_list(), estimator=None, ax=ax)

plt.show()
