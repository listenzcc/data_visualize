# File: geographic_analysis.py
# Aim: Necessary geographic analysis
# * Compute neighborhood links between cities, using global shortest method.

# -----------------------------------------------------------------------
import pdb
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from . import beside
from . import logger
from . import config

import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------
geo_frame = pd.read_json(beside(config.get('Geography', 'filename')))
print(geo_frame)

num = len(geo_frame)
posi = np.array(geo_frame.Position.to_list())

# -----------------------------------------------------------------------
matrix = np.zeros((num, num))
for i in tqdm(range(num)):
    matrix[i] = np.linalg.norm(posi - posi[i], axis=1)

print(matrix)

sns.heatmap(matrix)
plt.show()

# -----------------------------------------------------------------------
# Build shortest global path
inside = set()


def inside_add(id):
    inside.add(id)
    matrix[:, id] = np.inf


inside_add(0)
