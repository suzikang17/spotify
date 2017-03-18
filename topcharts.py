import csv as csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplt
import re
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.style.use('ggplot')


spotify_data = pd.read_csv("regional-global-daily-latest.csv")
artists = spotify_data["Artist"]

baseurl = 'http://en.wikipedia.org/w/api.php'

# create a dictionary for queries


query_attr = {}
query_attr['action'] = 'query'
query_attr['prop'] = 'revisions'
query_attr['rvprop'] = 'content'
query_attr['rvsection'] = 0
query_attr['format'] = 'xml'


birth_dict = {}
list = []
for person in artists:
    query_attr['titles'] = person
    response = requests.get(baseurl, query_attr)
    soup = BeautifulSoup(response.text, "xml")

# create a dictionary of musician:birth_year

    try:
        birth_re = re.search(r'(birth_date(.*?)}})', soup.revisions.getText())
        birth_data = birth_re.group(0).split('|')
        birth_dict[person] = birth_data
    except Exception:
        list.append(person)
#
# response = requests.get(baseurl, query_attr)
# soup = BeautifulSoup(response.text, "xml")

key_list = []

for i,j in birth_dict.items():
    key_list.append(j)


year_list = []
no_year = []

for i in key_list:
    try:
        res = re.search(r'19[3-9][0-9]', str(i))
        year = res.group(0)
        year_list.append(year)
    except Exception:
        no_year.append(i)

year_df = pd.Series(year_list).astype(int)
year_df.plot.hist(bins=15)
pyplt.show()
