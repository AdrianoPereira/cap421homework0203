# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import requests
import json
import logging
from string import Template
import datetime as dt
from datetime import timedelta


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)



def prepare_folder(function):
    def wrapper(*args, **kw):
        bpath = "/home/adriano/cap421homework0203/data/conventional_stations"
        folder = f"{bpath}/{kw['state']}/{kw['munic']}"
        
        if not os.path.exists(folder):
            logging.info(f"Creating directory: {folder}...")
            os.makedirs(folder)
        
        return function(*args, **kw)
    return wrapper
        

def download(url, filepath):
    logging.info(f"Downloading {url}...")
    res = requests.get(url)
    if res.status_code == 200:
        data = json.loads(res.content)
        out = pd.DataFrame()
        for row in data:
            row = {key: [value] for key, value in row.items()}
            out = out.append(pd.DataFrame(row))
        print(out)
        logging.info(f"Download complete! Saving in {filepath}...")
        out.to_csv(filename, index=False, encoding='utf-8')
        
    else:
        logging.error("Status code is not 200!")
        raise Exception("Status code is not 200!")
    
    

@prepare_folder
def download_daily_conventional_station_data(state, munic, stid, start, end):
    if isinstance(start, str): start = dt.datetime.strptime(start, "%Y-%m-%d")
    if isinstance(end, str): end = dt.datetime.strptime(end, "%Y-%m-%d")
    print(end-start)
    deltas = [timedelta(days=delta) for delta in range((end-start).days)]
    
    bpath = "/home/adriano/cap421homework0203/data/conventional_stations"
    folder = f"{bpath}/{state}/{munic}"
    filename_tmp = Template(
        f"{folder}/{state}-{munic}-{stid}-$year-$month-$day.csv"
    )
    url_tmp = Template(
        "https://apitempo.inmet.gov.br/estacao/$year-$month-$day/" \
            "$year-$month-$day/$stid"
    )
    
    for i, delta in enumerate(deltas):
        cdate = start+delta
        args = {
            'year': cdate.year, 
            'month': str(cdate.month).zfill(2), 
            'day': str(cdate.day).zfill(2),
            'stid': stid
        }
        
        filename = filename_tmp.substitute(**args)
        if not os.path.exists(filename):
            url = url_tmp.substitute(**args)
            print(filename)
            print(url)
            print()
            

filename = "/home/adriano/cap421homework0203/data/conventional_stations/PA/ITAITUBA/PA-ITAITUBA-82445-2000-01-30.csv"
url = "https://apitempo.inmet.gov.br/estacao/2000-01-30/2000-01-30/82445"

download(url, filename)
            
            
# download_daily_conventional_station_data(state='PA', munic='ITAITUBA', 
#                                          stid='82445', start='2000-01-01', 
#                                          end='2000-01-31')
    
        
    


# req = requests.get("https://apitempo.inmet.gov.br/estacao/2021-10-01/2021-10-01/82098")
