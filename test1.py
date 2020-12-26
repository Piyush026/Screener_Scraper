"""import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

res = requests.get("http://www.nationmaster.com/country-info/stats/Media/Internet-users")
soup = BeautifulSoup(res.content, 'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))

# print(df)
# print( tabulate(df[0], headers='keys', tablefmt='psql') )
# print(df[0].to_json(orient='records'))
hj = df[0].to_json(orient='records')
# print(hj)


print(type(df))
# users = df["AMOUNT"].tolist()
# print(countries)"""

import os
from multiprocessing import Pool

processes = ('process1.py', 'process2.py', 'process3.py')


def run_process(process):
    os.system('python {}'.format(process))


pool = Pool(processes=3)
pool.map(run_process, processes)
