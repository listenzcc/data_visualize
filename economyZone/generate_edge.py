# File: generate_edge.py
# Aim: Necessary geographic analysis
# * Compute shortest length graph linking all the cities,
# * will generate "edge.json", which stores edges of the graph.

# -----------------------------------------------------------------------
import json
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
        # self.edge: Generated graph edges, format is "dst: src" refers from [src] to [dst]
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
            # Find shortest path from [src] to [dst]
            dst_tuple = sorted(min_path.items(), key=lambda x: x[1][0])[0]
            src = dst_tuple[0]
            dst = dst_tuple[1][1]
            # Record path
            self.edge[dst] = src
            remain.remove(dst)
            if len(remain) == 0:
                break
            # Update src and insert dst in min_path dict
            # _update_min_path(src)
            # Insert dst
            _update_min_path(dst)
            # Re-compute src whose shortest is dst
            for s in min_path:
                if min_path[s][1] == dst:
                    _update_min_path(s)


spg = ShortestPathGraph(matrix)
spg.generate_path(300)
json.dump(spg.edge, open(beside('edge.json'), 'w'))
# print(len(spg.edge))
