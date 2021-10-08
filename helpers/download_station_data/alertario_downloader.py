import os
import requests
import shutil
from bs4 import BeautifulSoup


def download_meteorological_data():    
    years = list(range(1997, 2022))
    path_out = "/home/adriano/cap421homework0203/data/alertario/meteorological"
    
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    
    for i, year in enumerate(years):
        # create session and get CSRF middleware token
        url = "http://websempre.rio.rj.gov.br/dados/pluviometricos/met/"
        session = requests.session()
        req = session.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']
        
        
        # Create request body
        stids = [1, 11, 16, 19, 20, 22, 28, 32, 100]
        payload = {"csrfmiddlewaretoken": token}
        for stid in stids:
            payload[f"{stid}-check"] = "on"
            payload[f"{stid}-choice"] = f"{year}"
        payload[f"all-check"] = "on"
        payload[f"choice"] = f"{year}"
    
        # Create request headers
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "319",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "websempre.rio.rj.gov.br",
            "Origin": "http://websempre.rio.rj.gov.br",
            "Referer": "http://websempre.rio.rj.gov.br/dados/pluviometricos/met/",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        filename = f"{path_out}/METEOROLOGICAL-YEAR-{year}.zip"
        if not os.path.exists(filename):
            print(f"Download meteorological data in year: {year}")
            with session.post(url, data=payload, headers=headers, stream=True) as req:
                with open(filename, 'wb') as handle:
                    shutil.copyfileobj(req.raw, handle)
                
if __name__ == "__main__":
    download_meteorological_data()
