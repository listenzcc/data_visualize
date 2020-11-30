# File: generate_provinceJson.py
# Aim: Generate province.json

import json
import pandas as pd
import pdb
import random

from tqdm.auto import tqdm

from . import beside
from . import config

vertex_frame = pd.read_json(beside('geographic_frame.json'))
vertex_frame['Lat'] = vertex_frame.Position.map(lambda x: x[0])
vertex_frame['Lon'] = vertex_frame.Position.map(lambda x: x[1])

# --------------------------------------------------------------------------------
# Counting cities in province


def rnd_int(start=1, stop=10):
    return random.randint(start, stop)


def rnd_chr(string='abcd', k=1):
    return random.sample(string, k)[0]


print('Counting cities in province')
province_frame = pd.DataFrame()
for prov in tqdm(vertex_frame.Province.unique()):
    df = vertex_frame.loc[vertex_frame.Province == prov]
    cities = df.City.to_list()
    lat = df.Lat.mean()
    lon = df.Lon.mean()

    province_frame = province_frame.append(dict(
        Province=prov,
        Count=len(cities),
        Lat=lat,
        Lon=lon,
        ValueA=rnd_int(),
        ValueB=rnd_int(),
        ValueC=rnd_int(),
        GrpA=rnd_chr(),
        GrpB=rnd_chr(),
        # Cities=cities,
    ), ignore_index=True)
province_frame.set_index('Province', drop=False, inplace=True)
province_frame.index.name = None
province_frame.to_json(beside('province.json'))
print(province_frame)
