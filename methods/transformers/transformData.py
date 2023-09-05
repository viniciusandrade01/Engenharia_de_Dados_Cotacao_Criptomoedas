import time
import pandas as pd
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))
from utils.tools import GeneralTools
from methods.loaders.filesSave import FileSavers
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
generalTools = GeneralTools()
fileSavers = FileSavers()
webPageDataScrapers = WebPageDataScrapers()
data = time.strftime("%Y-%m-%d %H:%M:%S")

class TransformData:
    def __init__(self):
        self.aboutCoin = []
        self.padrao = []

    def extractContent(self, html, tags: dict, coin: str):
        self.aboutCoin.clear()
        df = pd.DataFrame()
        try:
            for chave, valor in tags.items():
                if isinstance(valor, str):
                    if coin != 'GERAL':
                        self.aboutCoin.append([item for item in html.find(f'{chave}', attrs={f'class':f'{valor}'}).text.split("\xa0") if item != ''])
                    else:
                        response, responsejson = webPageDataScrapers.requestGetApi(tags['base_url'], tags['endpoint'], tags['params'], tags['headers'])
                        self.aboutCoin.clear()
                        for index, valor in enumerate(responsejson['data']):
                            #self.aboutCoin.append(valor)
                            dictionary = fileSavers.saveDictionary(coin, valor, data)
                            df = fileSavers.concatDataFrame(df, dictionary, index)
                        return df
                else:
                    for value in valor:
                        self.aboutCoin.append([item for item in html.find(f'{chave}', attrs={f'class':f'{value}'}).text.split("\xa0") if item != ''])
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL ENCONTRAR AS INFORMAÇÕES SOBRE A MOEDA {coin}.")
        
        return [item for sublist in self.aboutCoin for item in sublist]