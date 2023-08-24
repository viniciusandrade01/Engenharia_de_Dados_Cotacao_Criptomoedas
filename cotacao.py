import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs4
import time
import logging
import re

df = pd.DataFrame()
data = time.strftime("%Y-%m-%d %H:%M:%S")
coins = ['bitcoin', 'ethereum', 'tether', 'bnb', 'xrp', 'usd-coin', 'cardano']
logging.basicConfig(filename="file.log", level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

for index, coin in enumerate(coins):

    try:
        html = rq.get(f'https://coinmarketcap.com/pt-br/currencies/{coin}/')
        html.raise_for_status()
        soup = bs4(html.text, 'html.parser')

        try:
            aboutCoin = [item for item in soup.find('div', attrs={'class':'sc-16891c57-0 hqcKQB flexStart alignBaseline'}).text.split("\xa0") if item != '']
            padrao = re.match(r'(\d+)([A-Za-z]+)', aboutCoin[-1][1:-1])
            logging.info(f"Dados - Moeda: {coin}")
        except AttributeError as attr_err:
            logging.error(f"Erro de Atributo: {attr_err}")
    
        dictionary = {
            'Moeda': coin.replace("-"," ").title(),
            'Preco': float(aboutCoin[0].replace("R$","").replace(",","").replace(".","").replace(" ","")),
            'Sigla_Preco': 'BRL',
            'Data_Captura': data.split(' ')[0],
            'Hora_Captura': data.split(' ')[1],
            'Variacao': float(aboutCoin[1].replace("%","")),
            'Periodo_Qtde': padrao.group(1),
            'Periodo_Und': padrao.group(2)
        }
    
        df = pd.concat([df, pd.DataFrame(dictionary, index=[index])])
    
    except rq.exceptions.HTTPError as http_err:
        logging.error(f"Erro HTTP: {http_err}")
    except rq.exceptions.RequestException as req_err:
        logging.error(f"Erro de Requisição: {req_err}")
    except Exception as err:
        logging.error(f"Erro Desconhecido: {err}")

df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)
df.to_csv(f"Cotação_{data.split(' ')[0]}.csv", sep=';', encoding='ISO-8859-1')