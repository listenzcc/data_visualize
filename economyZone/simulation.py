# File: simulation.py
# Aim: Generate simulation data

import pandas as pd
from . import beside
from .date import Date
from . import logger
from . import config

geo_frame = pd.read_json(beside(config.get('Geography', 'filename')))

date = Date(config=config)
print(geo_frame)
