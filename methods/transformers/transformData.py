#import re
import time
import utils.logger_config as logger_config
import logging
#from itertools import product
#from itertools import chain
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class TransformData:
    def __init__(self):
        self.regex = [r'R\$(\d{1,3}(?:,\d{3})*\.\d{2})',
                        r'(\d+)([A-Za-z]+)',
                        r'([\d.,]+)%R\$(\d[\d,.]+)'
        ]
        self.aboutCoin = []
        self.padrao = []

    def extractContent(self, html, tags: dict, coin: str):
        #coinTemp = [(chave_externa, chave_interna, valor) for (chave_externa, chave_interna), #valor in product(tags.items(), key=lambda x: x[1].items())]
        #coinTemp = [(chave_externa, chave_interna, valor) for chave_externa, dicionario_interno #in tags.items() for chave_interna, valor in dicionario_interno.items()]
        pares_combinados = [(chave, valor) for chave, valor in tags.items()]
        try:
            #for index, (chave, valor) in enumerate(tags.items()):
            for chave, valor in tags.items():
                self.aboutCoin.append([item for item in html.find(f'{chave}', attrs={f'class':f'{valor}'}).text.split("\xa0") if item != ''])
                #coinTemp = self.aboutCoin[-1]
                #self.aboutCoin.append([item for item in html.find(f'{chave}', attrs={f'class':f'{valor}'}).text if item != ''][0])
                #self.padrao.append(re.match(self.regex[index], self.aboutCoin[-1]))
        except Exception as e:
            logging.error(f"Erro: {e}, não foi possível encontrar as informações sobre a moeda {coin}.")
        
        #return self.aboutCoin #, self.padrao
        return [item for sublist in self.aboutCoin for item in sublist]
