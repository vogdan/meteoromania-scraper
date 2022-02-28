#!/usr/bin/python

from bs4 import BeautifulSoup

import requests as req
import re
import os
from datetime import datetime

resp = req.get('http://www.meteoromania.ro/')

soup = BeautifulSoup(resp.text, 'lxml')

data = soup.find('ul', class_='slides')

dlist = []
for slide in data.find_all('li'):
    d = dict()
    loc = slide.h2.text
    dt = slide.find('div', class_='subtitle').text.split()
    data = dt[0]
    ora = dt[2]
    info = slide.find('div', class_='text')

    d['Loc'] = loc
    d['Data'] = data
    d['Ora'] = ora
    
    for rex in ['Temp*', 'V.nt*', 'Nebuloz*', 'Pres*', 'Umez*', 'Strat*']:
        tname = info.find('b', text=re.compile(rex))
        if tname is not None:
            tval = tname.next_sibling
            if rex == 'V.nt*':
                vd = tval.split(',')
                if len(vd) > 1:
                    d[tname.text + '_vit'] = vd[0].strip(': ')
                    d[tname.text + '_dir'] = vd[1].split(':')[1].strip()
                else:
                    d[tname.text + '_vit'] = tval.strip(': ')
                    d[tname.text + '_dir'] = tval.strip(': ')
            else:
                d[tname.text] = tval.strip(': ')
    dlist.append(d)

out = 'istoric_meteo'
out = out + '-' + datetime.today().strftime("%Y-%m")
if os.path.exists(out):
    mode = 'a'
else:
    mode = 'w'
with open(out, mode) as f:
    if mode == 'w':
        header = dlist[1].keys()
        f.write('|'.join(header))
        f.write('\n')
    for d in dlist:
        f.write('|'.join(d.values()))
        f.write('\n')
#that is it
