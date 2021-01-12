#!/usr/bin/python

from bs4 import BeautifulSoup

import requests as req
import re

resp = req.get('http://www.meteoromania.ro/')

soup = BeautifulSoup(resp.text, 'lxml')

data = soup.find('ul', class_='slides')
for slide in data.find_all('li'):
    loc = slide.h2.text
    time = slide.find('div', class_='subtitle').text
    
    info = slide.find('div', class_='text')
    print (loc)
    print (time)
  
    for rex in ['Temp*', 'V?nt*', 'Nebuloz*', 'Pres*', 'Umez*', 'Strat*']:
        tname = info.find('b', text=re.compile(rex))
        if tname is not None:
            print (tname.text)
            tval = tname.next_sibling
            print (tval)
    print('\n')




    
