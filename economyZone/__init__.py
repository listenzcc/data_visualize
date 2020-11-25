# File: __init__.py
# Aim: economyZone package startup script

import configparser
import datetime
import os
from .date import Date

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'setting.ini'))

date = Date(config=config)
