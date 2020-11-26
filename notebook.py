# %%
from economyZone import config
from economyZone.date import Date
from economyZone import simulation

date = Date()
for j in range(10):
    print(j, date.string())
    date.next()
