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
import argparse


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
    """
    Function to download a CSV file.

    Parameters
    ----------
    url : TYPE
        DESCRIPTION.
    filepath : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    """
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
        out.to_csv(filepath, index=False, encoding='utf-8')
        
    else:
        logging.error("Status code is not 200!")
        raise Exception("Status code is not 200!")
    
    

@prepare_folder
def download_daily_conventional_station_data(state, munic, stid, start, end):
    """
    Function to download data from conventional INMET stations.

    Parameters
    ----------
    state : TYPE
        DESCRIPTION.
    munic : TYPE
        DESCRIPTION.
    stid : TYPE
        DESCRIPTION.
    start : TYPE
        DESCRIPTION.
    end : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
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
            download(url, filename)
            

def read_and_download_convetional_INMET_stations(start, end):
    """
    Read CSV stations and download data between date interval.

    Parameters
    ----------
    start : TYPE
        DESCRIPTION.
    end : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    convs = pd.read_csv("/home/adriano/cap421homework0203/data/" \
                        "conventional_station_catalog.csv", sep=';')
    for i, station in convs.iterrows():
        args = {
            'state': station['SG_ESTADO'], 
            'munic': station['DC_NOME'], 
            'stid': station['CD_ESTACAO'], 
            'start': start, 
            'end': end
        }
        logging.info(f"Downloading data from {station['DC_NOME']}")
        download_daily_conventional_station_data(**args)
        
        logging.info(f"{station['DC_NOME']} downloaded!")
        
        
def download_individual_daily_station(state, munic, stid, start, end):
    logging.info(f"Downloading data from {munic}")
    download_daily_conventional_station_data(**args)
    
    logging.info(f"{munic} downloaded!")    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', default='2000-01-01', 
                        help="Start datetime.")
    parser.add_argument('-e', '--end', default='2021-01-01', 
                        help="End datetime.")
    parser.add_argument('-m', '--munic', 
                        help="Station location municipality.", required=True)
    parser.add_argument('-u', '--state', help="Station location state (UF)", 
                        required=True)
    parser.add_argument('-i', '--stid', help="Station ID.")
    
    args = vars(parser.parse_args())
    
    
    # print(args)    
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(
                f"/home/adriano/cap421homework0203/logs/" \
                    f"{args['stid']}-{args['start']}-{args['start']}.log"
            ),
            logging.StreamHandler()
        ]
    )    
    
    # read_and_download_convetional_INMET_stations('2000-01-01', '2021-01-01')
    download_individual_daily_station(**args)

    
