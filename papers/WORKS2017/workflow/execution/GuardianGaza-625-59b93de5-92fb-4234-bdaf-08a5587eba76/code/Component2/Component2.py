import json
import matplotlib.pyplot as plt
import datetime
import urllib2, urllib
import pandas as pd
import sys

def parse_loc(loc, ret_lon=True):
    try:
        lon, lat = loc.split(',')
        lon, lat = lon.strip(' '), lat.strip(' ')
        lon, lat = map(float, [lon, lat])
        if ret_lon:
            return lon
        else:
            return lat
    except:
        return None

db = pd.read_csv(sys.argv[1])
db['lon'] = db['Location (approximate)'].apply(lambda x: parse_loc(x))
db['lat'] = db['Location (approximate)'].apply(lambda x: parse_loc(x, ret_lon=False))
db['Date'] = db['Date'].apply(pd.to_datetime)
db.to_csv(sys.argv[2])
db.head()