#!/usr/bin/python

import datetime, platform, rpm

try:
    # el6+
    from collections import OrderedDict
    import json
except ImportError:
    # el5
    from ordereddict import OrderedDict
    import simplejson as json

ts = rpm.TransactionSet()
pkghash = {}

for h in ts.dbMatch():
    pkghash[h['name']] = {
      'version': h['version'],
      'release': h['release'],
      'summary': h['summary'].replace("\n"," ")
    }

data = OrderedDict()
fqdn = platform.uname()[1]

data['fqdn'] = fqdn
data['last_refresh'] = datetime.datetime.now().strftime("%Y%m%d")
data['packages'] = OrderedDict(sorted(pkghash.items(), key=lambda x: x[0]))

ifile='/tmp/pkgs-%s.json' % fqdn

outfile = open(ifile, 'w')
json.dump(data, outfile, indent=2)
outfile.close()

