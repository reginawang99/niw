import json
import matplotlib.pyplot as plt
import datetime
import urllib2, urllib
import pandas as pd
import sys

db = pd.read_csv(sys.argv[1])
db['Date'] = db['Date'].apply(pd.to_datetime)
t = db['Date']
t = t.reindex(t)
by_day = t.groupby(lambda x: x.day).size()
by_day.plot(kind='bar')
plt.title('Number of events by day')
plt.savefig(sys.argv[2],format='png')