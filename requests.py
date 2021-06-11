#!/usr/bin/env python3
import requests

url = 'http://0.0.0.0:3000' #substitute for machine IP

flag = ''
v, n = '', ''

while v != 'end' and n != 'end':
    r = requests.get('%s/%s' % (url, n))
    j = r.json()
    v, n = j['value'], j['next']
    flag += v

print(flag[:-3])
