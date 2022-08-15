#!/usr/bin/python

import subprocess as sp
import datetime, platform, re

try:
    # el6+
    from collections import OrderedDict
    import json
except ImportError:
    # el5
    from ordereddict import OrderedDict
    import simplejson as json

def distribver():
  if hasattr(platform, 'linux_distribution'):
    return int(platform.linux_distribution()[1].split('.')[0])
  # else : old python; assuming it is an el5
  return 5

if distribver() > 6:
    # systemd
    cmd = 'systemctl list-unit-files --state=enabled --no-pager --no-legend | iconv -f UTF-8 -t ASCII//TRANSLIT'
    p = sp.Popen(cmd, shell=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    services = re.findall(r"([^ \n]+)\.service[\t ]+enabled[\t ]*", p.stdout.read())
else:
    # init sys V
    cmd1 = '/sbin/runlevel'
    r = sp.Popen(cmd1, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    runlevel = r.stdout.read().split()[-1]
    cmd2 = '/sbin/chkconfig --list'
    l = sp.Popen(cmd2, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    output = l.stdout.read()
    regex=r"([^ \t\n]+)[\t ]+[0][:].*"+re.escape(runlevel)+":on"
    services = re.findall(regex, output) + re.findall(r"([^ \t\n]+):[\t ]+on", output)

data = OrderedDict()
fqdn = platform.uname()[1]
services.sort()
data['fqdn'] = fqdn
data['last_refresh'] = datetime.datetime.now().strftime("%Y%m%d")
data['services'] = services

ifile='svcs-%s.json' % fqdn

outfile = open(ifile, 'w')
json.dump(data, outfile, indent=2)
outfile.close()