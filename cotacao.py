import pandas as pd
import requests as rq
import time
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
import utils.logger_config as logger_config
import logging

def main():
    fileSavers = FileSavers()
    transformData = TransformData()
    webPageDataScrapers = WebPageDataScrapers()
    generalTools = GeneralTools()
    try:
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        data = time.strftime("%Y-%m-%d %H:%M:%S")
        logger_config.setup_logger(data)
        df = pd.DataFrame()
        nameDirectory = f"Moedas_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}"
        for index, coin in enumerate(jsonData['coins']):
            logging.info(f"Acessando link referente a moeda {coin}.")
            html, soup = webPageDataScrapers.specificGetRequest(f"{jsonData['source']['specificLink']['fonte']}{coin}") if len(jsonData['coins']) != '' else webPageDataScrapers.requestGetDefault(jsonData['source']['generalLink']['fonte'])
            logging.info(f"Salvando página html referente a moeda {coin}.")
            fileSavers.saveHTML(html, f"html_{generalTools.hyphenToNull(coin)}_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}.txt", nameDirectory)
            logging.info(f"Extraindo conteúdo desejado referente a moeda {coin}.")
            
            #jsonData['source']['specificLink']['atributos']
            #Continuar daqui, passar no extractContent
            
            aboutCoin, padrao = transformData.extractContent(soup, 'span', 'class',  'sc-16891c57-0 dxubiK base-text', coin)
            aboutCoin, padrao = transformData.extractContent(soup, 'div', 'class', 'sc-aef7b723-0 sc-5219c53f-0 hPqPqM', coin)
            aboutCoin, padrao = transformData.extractContent(soup, 'dd', 'class', 'sc-16891c57-0 fRWxhs base-text', coin)
            aboutCoin, padrao = transformData.extractContent(soup, 'dd', 'class', 'sc-16891c57-0 fRWxhs base-text', coin)
            
            logging.info(f"Dados da Moeda: {coin} coletados com sucesso.")

            logging.info(f"Salvando informações referente a moeda {coin}.")
            dictionary = {
                'Moeda': coin.replace("-"," ").title(),
                'Preco': float(aboutCoin[0].replace("R$","").replace(",","").replace(".","").replace (" ","")),
                'Sigla_Preco': 'BRL',
                'Data_Captura': data.split(' ')[0],
                'Hora_Captura': data.split(' ')[1],
                'Variacao': float(aboutCoin[1].replace("%","")),
                'Periodo_Qtde': padrao.group(1),
                'Periodo_Und': padrao.group(2)
            }
            logging.info(f"Informações referente a moeda {coin} salva com sucesso.")
            df = fileSavers.concatDataFrame(df, dictionary, index)

        file_name = f"Moedas_{data.split(' ')[0].replace('-','')}"
        fileSavers.saveDataFrame(df, file_name, '\t', nameDirectory)
    except FileNotFoundError as err:
        logging.error(f"Erro: {err}, o arquivo JSON (data.json) não foi encontrado")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"Erro durante a requisição: {err}")
    except Exception as err:
        logging.error(f"Erro desconhecido: {err}")

if __name__ == '__main__':
    main()