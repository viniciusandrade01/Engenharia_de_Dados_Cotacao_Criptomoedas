import requests as rq
from bs4 import BeautifulSoup as bs4
import time
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class WebPageDataScrapers:
    def __init__(self):
        pass

    def requestGetDefault(self, link: str):
        try:
            html = rq.get(link)
            html.raise_for_status()
            soup = bs4(html.text, 'html.parser')

        except rq.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP: {http_err}")
        except rq.exceptions.RequestException as req_err:
            logging.error(f"Erro de Requisição: {req_err}")
        except Exception as err:
            logging.error(f"Erro Desconhecido: {err}")
        
        return html, soup
    
    def specificGetRequest(self, coins: str):
        try:
            html = rq.get(f'https://coinmarketcap.com/pt-br/currencies/{coins}/')
            html.raise_for_status()
            soup = bs4(html.text, 'html.parser')

        except rq.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP: {http_err}")
        except rq.exceptions.RequestException as req_err:
            logging.error(f"Erro de Requisição: {req_err}")
        except Exception as err:
            logging.error(f"Erro Desconhecido: {err}")
        
        return html, soup