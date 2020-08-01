import requests
import os
import sys
from bs4 import BeautifulSoup
import pandas as pd

def export_data_to_pandas(data):
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find(id='csvContentDiv')
    table_rows = table.get_text().split(':')
    table_rows.remove('')
    l=[]
    for tr in table_rows:
        row = tr.split(',')
        row = [val.replace(" ","") for val in row]
        l.append(row)
    column_names = l.pop(0)
    return pd.DataFrame(l, columns=column_names )


def get_historical_data(symbol, from_date, to_date):
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    	    'Accept': '*/*',
    	    'Accept-Language': 'en-US,en;q=0.5',
    	    'X-Requested-With': 'XMLHttpRequest',
    	    'Connection': 'keep-alive',
    	    'Referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm',
        }
    params = (
            ('symbol', symbol),
    	    ('segmentLink', '3'),
    	    ('symbolCount', '2'),
    	    ('series', 'EQ'),
    	    ('dateRange', ''),
    	    ('fromDate', from_date),
    	    ('toDate', to_date),
    	    ('dataType', 'PRICEVOLUMEDELIVERABLE'),
    	    )

    response = requests.get('https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp', headers=headers, params=params)
    data_pd = export_data_to_pandas(response.content)
    return data_pd


NIFTY=pd.read_csv('ind_nifty200list.csv')
NIFTYnse=NIFTY['Symbol'].values
os.system('mkdir -p ../Data/')
from_date=sys.argv[1]
to_date=sys.argv[2]
for comp in NIFTYnse:
    try:
        comp_data=get_historical_data(comp, from_date, to_date)
        comp_data.to_csv('../Data/'+comp+'.csv')
        print(comp+' done')
    except:
        print('couldnt get '+comp)

