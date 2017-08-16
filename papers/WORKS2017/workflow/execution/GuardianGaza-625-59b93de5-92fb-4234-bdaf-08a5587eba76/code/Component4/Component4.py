import json
import matplotlib.pyplot as plt
import datetime
import urllib2, urllib
import pandas as pd
import sys
import matplotlib.cm as cm

db = pd.read_csv(sys.argv[1])
db['Date'] = db['Date'].apply(pd.to_datetime)
f = plt.figure(figsize=(10, 6))
ax = f.add_subplot(111)
x, y = db['lon'], db['lat']
s = plt.scatter(x, y, marker='.', color='k')
for d, day in db.set_index('Date').groupby(lambda x: x.day):
    x, y = day['lon'], day['lat']
    c = cm.Set1(d/30.)
    s = plt.scatter(x, y, marker='^', color=c, label=str(d), s=20)
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_visible(False)
plt.legend(loc=2)
plt.title('Spatial distribution of events by day')
ax.set_axis_bgcolor("0.2") 
plt.savefig(sys.argv[2], format="png")