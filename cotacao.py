import pandas as pd
import requests as rq
import time
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
import utils.logger_config as logger_config
import logging

fileSavers = FileSavers()
transformData = TransformData()
webPageDataScrapers = WebPageDataScrapers()
generalTools = GeneralTools()
# Variável contendo informações das moedas a serem coletadas, aws e banco de dados
jsonData = generalTools.openJson()
data = time.strftime("%Y-%m-%d %H:%M:%S")
logger_config.setup_logger(data)

df = pd.DataFrame()
nameDirectory = f"Moedas_{data.split(' ')[0].replace('-','')}"

for index, coin in enumerate(jsonData['coins']):
    try:
        logging.info(f"Acessando link referente a moeda {coin}.")
        html, soup = webPageDataScrapers.specificGetRequest(coin)
        logging.info(f"Salvando página html referente a moeda {coin}.")
        fileSavers.saveHTML(html, f"html_{coin.replace('-','')}_{data.split(' ')[0].replace('-','')}.txt", nameDirectory)

        try:
            logging.info(f"Extraindo conteúdo desejado referente a moeda {coin}.")
            aboutCoin, padrao = transformData.extractContent(soup, 'div', 'class', 'sc-16891c57-0 hqcKQB flexStart alignBaseline', coin)
            #aboutCoin, padrao = transformData.extractContent(soup, 'dd', 'class', 'sc-16891c57-0 fRWxhs base-text', coin)
            logging.info(f"Dados da Moeda: {coin} coletados com sucesso.")
        except AttributeError as attr_err:
            logging.error(f"Erro de Atributo: {attr_err}")
    
        logging.info(f"Salvando informações referente a moeda {coin}.")
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
        logging.info(f"Informações referente a moeda {coin} salva com sucesso.")
        try:
            df = fileSavers.concatDataFrame(df, dictionary, index)
        except KeyError as e:
            logging.error(f"Erro: {e}, não foi possível encontrar a chave {e} no dicionário.")
        except Exception as e:
            logging.error(f"Erro: {e}, não foi possível concatenar os DataFrames.")
    
    except rq.exceptions.HTTPError as http_err:
        logging.error(f"Erro HTTP: {http_err}")
    except rq.exceptions.RequestException as req_err:
        logging.error(f"Erro de Requisição: {req_err}")
    except Exception as err:
        logging.error(f"Erro Desconhecido: {err}")

    try:
        file_name = f"Moedas_{data.split(' ')[0].replace('-','')}"
        fileSavers.saveDataFrame(df, file_name, '\t', nameDirectory)
    except FileNotFoundError as e:
        logging.error(f"Erro: {e}, o arquivo {file_name} não existe")
    except (KeyError, Exception) as e:
        logging.error(f"Erro: {e}, não foi possível salvar o DataFrame")