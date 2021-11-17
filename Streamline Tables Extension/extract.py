# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 16:19:02 2021

@author: L
"""

import requests
import pandas as pd
import urllib

url = 'https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.114.010389?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%20%200pubmed'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

'''       
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}


data = pd.read_html(url, header=header, attrs = {'class': 'article-table-content'})

tablenum = len(data)
print(tablenum)
'''

html = requests.get(url, headers=header).content

'''Get all tables'''
tables_list = pd.read_html(html)
table = tables_list[-1]
print(table)
table.to_csv('table3.csv', encoding='utf_8_sig')