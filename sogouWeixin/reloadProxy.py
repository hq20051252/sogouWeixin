#!/usr/bin/python
#-*-coding:utf-8-*-
'''
Created on Dec 16, 2014

@author: hadoop
'''

import urllib2
import json

PROXY_SERVICE = r"http://172.16.80.64:50000/select?num=500&speed=0.5"

data = urllib2.urlopen(PROXY_SERVICE).read()
proxies = json.loads(data)['ips']

def zhengli(proxies):
    result = []
    pxy = {}
    for proxy in proxies:
        key = str(proxy[u'ip'])
        pxy[key].append(proxy) if pxy.has_key(key) else pxy.update({key:[proxy,]})
        
        sorted(pxy[key], lambda x,y: cmp(x['speed'] , y['speed']))
    
    for item in pxy.values():
        result.append(item[0])
    
    return result


pxy = zhengli(proxies)        
res = []
for proxy in pxy:
    print proxy
    ip_port = {'ip_port': str(proxy[u'ip']) + ":" + str(proxy[u'port'])}
    res.append(ip_port)

with open(r'proxy.py', 'wb') as fd:
    fd.write("PROXIES = [\n")
    for item in res:
        fd.write("            %s,\n" % repr(item))
    
    fd.write("]")
    