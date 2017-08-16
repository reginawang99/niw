import json as simplejson
import matplotlib.pyplot as plt
import datetime
import urllib2, urllib
import pandas as pd
import sys

# Trick from http://stackoverflow.com/questions/7800213/can-i-use-pythons-csv-reader-with-google-fusion-tables
api_key = sys.argv[1]
request_url = sys.argv[3]
query = sys.argv[2]

url = "%s?%s" % (request_url, urllib.urlencode({'sql': query, 'key': api_key}))
serv_req = urllib2.Request(url=url)
serv_resp = urllib2.urlopen(serv_req)
table = serv_resp.read()
print '\nLast pull of data from the Google FusionTable: ', datetime.datetime.now()
csv = simplejson.loads(table)
del csv['kind']
csv['data'] = csv['rows']
del csv['rows']
db = pd.read_json(simplejson.dumps(csv), orient='split')
db.to_csv(sys.argv[4], header=True, index=False, encoding='utf-8')