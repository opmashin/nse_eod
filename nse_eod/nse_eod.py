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

def download_data_from_nse(symbol, from_date, to_date):
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
    return response.content

def get_period_data(symbol, period):
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
    	    ('dateRange', period),
    	    ('fromDate', ''),
    	    ('toDate', ''),
    	    ('dataType', 'PRICEVOLUMEDELIVERABLE'),
    	    )
    response = requests.get('https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp', headers=headers, params=params)
    return export_data_to_pandas(response.content)

def get_historical_data(symbol, from_date, to_date):
    from_year = int(from_date.split('-')[-1])
    to_year = int(to_date.split('-')[-1])
    if( from_year < to_year ):
        eod_data_html = download_data_from_nse(symbol, from_date, '31-12-'+str(from_year))
        eod_data_df = export_data_to_pandas(eod_data_html)
        from_year += 1
        while( from_year < to_year):
            eod_data_html = download_data_from_nse(symbol, '01-01-'+str(from_year), '31-12-'+str(from_year))
            eod_data_df = eod_data_df.append(export_data_to_pandas(eod_data_html), ignore_index=True)
            from_year += 1
        eod_data_html = download_data_from_nse(symbol, '01-01-'+str(from_year), to_date)
        eod_data_df = eod_data_df.append(export_data_to_pandas(eod_data_html), ignore_index=True)
    else:
        eod_data_html = download_data_from_nse(symbol, from_date, to_date)
        eod_data_df = export_data_to_pandas(eod_data_html)
    return eod_data_df
