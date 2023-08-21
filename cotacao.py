import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs4
import time

df = pd.DataFrame()
coins = ['bitcoin', 'ethereum', 'tether', 'bnb', 'xrp', 'usd-coin', 'cardano']
for coin in coins:
    html = rq.get('https://coinmarketcap.com/pt-br/currencies/{coin}/')
    soup = bs4(html.text, 'html.parser')

    aboutCoin = [item for item in soup.find('div', attrs={'class':'sc-16891c57-0 hqcKQB flexStart alignBaseline'}).text.split("\xa0") if item != '']

    dictionary = {
        'Moeda': 'Ronaldinho',
        'Preco_Captura': aboutCoin[0].replace("R$","").replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.'),
        'Sigla_Preco:':'BRL',
        'Data_Captura': time.strftime("%Y-%m-%d %H:%M:%S"),
        'Variacao': aboutCoin[1],
        'Periodicidade': aboutCoin[2]
    }
    _=1