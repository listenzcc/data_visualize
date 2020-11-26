# File: load_location_json.py
# Aim: Load locations form json file,
# ! This script is designed to be used once on the machine has the json file.

# %%
import json
import pandas as pd
from tqdm.notebook import tqdm

fpath = '../../learning_mapbox/locations.json'
locations = json.load(open(fpath, 'rb'))
locations

# %%
frame = pd.DataFrame(columns=['Province', 'City', 'Position'])
for prov in tqdm(locations):
    for city in tqdm(locations[prov], desc=prov):
        posi = locations[prov][city]
        frame = frame.append(dict(
            Province=prov,
            City=city,
            Position=[float(e) for e in posi]
        ), ignore_index=True)

# %%
# * The frame has geographic infomation of cities in China,
# * columns are | Province | City | Position |
frame.to_json('geographic_frame.json')
frame

# %%
