import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs4
import time

df = pd.DataFrame()
coins = ['bitcoin', 'ethereum', 'tether', 'bnb', 'xrp', 'usd-coin', 'cardano']

for index, coin in enumerate(coins):
    try:
        html = rq.get(f'https://coinmarketcap.com/pt-br/currencies/{coin}/')
        soup = bs4(html.text, 'html.parser')
    except rq.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP para {coin}: {e}")
        continue

    try:
        aboutCoin = [item for item in soup.find('div', attrs={'class':'sc-16891c57-0 hqcKQB flexStart alignBaseline'}).text.split("\xa0") if item != '']
    except AttributeError as e:
        print(f"Erro ao fazer parsing do HTML para {coin}: {e}")
        continue

    try:
        dictionary = {
            'Moeda': coin.replace("-"," ").title(),
            'Preco_Captura': float(aboutCoin[0].replace("R$","").replace(",","").replace(".","").replace(" ","")),
            'Sigla_Preco': 'BRL',
            'Data_Captura': time.strftime("%Y-%m-%d %H:%M:%S"),
            'Variacao': float(aboutCoin[1].replace("%","")),
            'Periodicidade': aboutCoin[2].replace("(","").replace(")","")
        }
    except (ValueError, IndexError) as e:
        print(f"Erro na conversão de dados para {coin}: {e}")
        continue
    
    try:
        df_temp = pd.DataFrame(dictionary, index=[index])
        df = pd.concat([df, df_temp])
    except pd.errors.MergeError as e:
        print(f"Erro ao inserir dados no DataFrame para {coin}: {e}")
        
print(df)