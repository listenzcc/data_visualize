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
geo_frame = pd.read_json(beside(config.get('Geography', 'filename')))
geo_frame['Lon'] = geo_frame.Position.map(lambda x: x[0])
geo_frame['Lat'] = geo_frame.Position.map(lambda x: x[1])
print(geo_frame)

num = len(geo_frame)
posi = np.array(geo_frame.Position.to_list())

# -----------------------------------------------------------------------
matrix = np.zeros((num, num))
for i in tqdm(range(num)):
    matrix[i] = np.linalg.norm(posi - posi[i], axis=1)
matrix += np.diag([np.nan for _ in range(num)])

# -----------------------------------------------------------------------
# Build shortest global path


class ShortestPathGraph(object):
    # Generating mapping graph across all the vertex
    def __init__(self, matrix):
        # [matrix] is the distance matrix of all the vertex
        self.matrix = matrix
        self.matrix[np.isnan(self.matrix)] = np.inf

    def generate_path(self, idx):
        # Start generating the shortest path,
        # [idx] is the beginning vertex
        num = len(matrix)
        self.vertex = []
        self.edge = dict()

        self.vertex.append(idx)
        self.matrix[:, idx] = np.inf

        for _ in trange(num):
            self.next_shortest()

    def next_shortest(self):
        # Find the shortest next path
        matrix = self.matrix[self.vertex]
        coord = np.unravel_index(np.argmin(matrix), matrix.shape)
        src, des = self.vertex[coord[0]], coord[1]
        self.add_edge(src, des)

    def add_edge(self, src, des):
        # Add edge to the graph
        self.vertex.append(des)
        self.matrix[:, des] = np.inf
        self.edge[des] = src


spg = ShortestPathGraph(matrix)
spg.generate_path(0)
print(len(spg.edge))


# -----------------------------------------------------------------------
# Draw the graph
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题-设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
sns.scatterplot(data=geo_frame, x='Lon', y='Lat',
                hue=geo_frame.Province.to_list(), ax=ax)

for a, b in tqdm(spg.edge.items()):
    x = [geo_frame.Lon.loc[e] for e in [a, b]]
    y = [geo_frame.Lat.loc[e] for e in [a, b]]
    sns.lineplot(x=x, y=y, ax=ax)

plt.show()
