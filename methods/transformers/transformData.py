import re
import time
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class TransformData:
    def __init__(self):
        self.regex1 = r'(\d+)([A-Za-z]+)'
        self.regex2 = r'\d+\.\d+%R\$\d{1,3}(?:,\d{3})*'

    def extractContent(self, html, parentTag: str, childTag: str, content: str, coin: str):
        try:
            aboutCoin = [item for item in html.find(f'{parentTag}', attrs={f'{childTag}':f'{content}'}).text.split("\xa0") if item != '']
            #if re.match(self.regex1, aboutCoin[-1][1:-1]):
            #    return aboutCoin, re.match(self.regex1, aboutCoin[-1][1:-1])
            #elif re.match(self.regex2, aboutCoin[-1][1:-1]):
            #    return aboutCoin, re.match(self.regex2, aboutCoin[-1][1:-1])
            #else:
            #    return logging.info("Nenhuma regex se aplica. Entre em contato com os #desenvolvedores.")
                
            padrao = re.match(self.regex1, aboutCoin[-1][1:-1])
        except Exception as e:
            logging.error(f"Erro: {e}, não foi possível encontrar as informações sobre a moeda {coin}.")
        
        return aboutCoin, padrao
