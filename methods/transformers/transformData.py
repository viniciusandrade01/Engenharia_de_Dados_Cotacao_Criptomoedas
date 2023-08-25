import re
import time
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class TransformData:
    def __init__(self):
        pass

    def extractContent(self, html, parentTag: str, childTag: str, content: str, coin: str):
        try:
            aboutCoin = [item for item in html.find(f'{parentTag}', attrs={f'{childTag}':f'{content}'}).text.split("\xa0") if item != '']
            padrao = re.match(r'(\d+)([A-Za-z]+)', aboutCoin[-1][1:-1])
        except Exception as e:
            logging.error(f"Erro: {e}, não foi possível encontrar as informações sobre a moeda {coin}.")
        
        return aboutCoin, padrao
