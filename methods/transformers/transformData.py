import re
import time
import pandas as pd
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))
from utils.tools import GeneralTools
from methods.loaders.filesSave import FileSavers
generalTools = GeneralTools()
fileSavers = FileSavers()
data = time.strftime("%Y-%m-%d %H:%M:%S")

class TransformData:
    def __init__(self):
        self.regex = r'(\d+)([A-Za-z]+)([A-Za-z]{3,4})(R\$\d+,\d+\.\d+)(\d+\.\d+%)(\d+\.\d+%)(\d+\.\d+%)(R\$\d+\.\d+[TB])(R\$(\d{1,3}(?:,\d{3})*,\d+))(R\$(\d{1,3}(?:,\d{3})*,\d{3},\d{3}))(\d{1,3}(?:,\d{3})*)([A-Za-z]{3,4})(\d+(?:,\d+)*)([A-Za-z]{3,4})'
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
                        table = html.find(f"{chave}")
                        table = table.find_all(f"{valor}")
                        titulos = table[0]
                        for index, valor in enumerate(table[1:]):
                            valor = generalTools.emptyValueToEmpty(valor.text).replace("USDt","")
                            correspondencias = re.search(self.regex, valor)
                            if correspondencias is None:
                                continue
                            self.aboutCoin.extend(correspondencias.groups())
                            dictionary = fileSavers.saveDictionary(coin, self.aboutCoin, data)
                            self.aboutCoin.clear()
                            df = fileSavers.concatDataFrame(df, dictionary, index)
                        return df
                else:
                    for value in valor:
                        self.aboutCoin.append([item for item in html.find(f'{chave}', attrs={f'class':f'{value}'}).text.split("\xa0") if item != ''])
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL ENCONTRAR AS INFORMAÇÕES SOBRE A MOEDA {coin}.")
        
        return [item for sublist in self.aboutCoin for item in sublist]