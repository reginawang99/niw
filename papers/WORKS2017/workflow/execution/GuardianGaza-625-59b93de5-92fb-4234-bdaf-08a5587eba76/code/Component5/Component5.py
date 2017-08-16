# You'll need cartopy for a pretty map
import json
import matplotlib.pyplot as plt
import datetime
import urllib2, urllib
import pandas as pd
import sys
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.cm as cm

db = pd.read_csv(sys.argv[1])
db['Date'] = db['Date'].apply(pd.to_datetime)
bg = cimgt.OSM()
src = ccrs.PlateCarree()

f = plt.figure(figsize=(20, 30))
ax = plt.axes(projection=bg.crs)
ax.add_image(bg, 9, alpha=0.5)

x, y = db['lon'], db['lat']
extent = [y.min(), y.max(), x.min(), 34]
extent = [34, 36, x.min(), x.max()] #Manually tweaked
for d, day in db.set_index('Date').groupby(lambda x: x.day):
    y, x = day['lon'], day['lat']
    c = cm.Set1(d/30.)
    s = plt.scatter(x, y, marker='^', color=c, label=str(d), s=40, \
                    transform=src)
ax.set_extent(extent, crs=src)
plt.legend(loc=2)
plt.title('Spatial distribution of events by day')
plt.savefig(sys.argv[2],format='png')