# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 18:58:13 2017

@author: YIWEI HUANG
"""
# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import urllib.request as ur
from bs4 import BeautifulSoup as bs

url ='https://www.51go.com.au/Category/baby-products'

info = bs(ur.urlopen(url), 'html.parser')

            
#%%         
qiangguang = {}
for k in info.find_all('div', attrs={'class':'jingxuan_main'}):
    temp_name = k.find(name='p', attrs={'class':'jingxuan_tl'}).get_text()[1:-1]
    qg = k.find('div', attrs={'class':'qiangugang'})
    if qg is not None:
        qiangguang[temp_name] = '已抢光'
        
#%%
        
a = pd.DataFrame({'a':[1,2,3],
                  'b':[4,5,6]})
    
[1,2,3]