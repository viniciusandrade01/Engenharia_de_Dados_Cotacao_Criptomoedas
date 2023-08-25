import io
import os
import time
import pandas as pd
import utils.logger_config as logger_config
from utils.tools import GeneralTools
import logging
generalTools = GeneralTools()
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class FileSavers:
    def __init__(self):
        pass

    def saveHTML(self, content, file_name: str, file_directory: str):
        generalTools.makeDirectory(file_directory)
        with io.open(os.path.join(file_directory, file_name), "w", encoding="utf-8") as fp:
            fp.write(content.text)

    def saveDataFrame(self, content, file_name, sep, nameDirectory):
        try:
            if not file_name.endswith(".csv"):
                file_name += ".csv"

            df = pd.DataFrame(content)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            df.to_csv(os.path.join(nameDirectory, file_name), sep=f'{sep}', encoding='ISO-8859-1', index=False)
        except FileNotFoundError as e:
            logging.error(f"Erro: {e}, o arquivo {file_name} não existe.")
        except Exception as e:
            logging.error(f"Erro: {e}, não foi possível salvar o DataFrame.")
        
    def concatDataFrame(self, df: pd.DataFrame, dictionary: dict, index: int):
        try:
            return pd.concat([df, pd.DataFrame(dictionary, index=[index])])
        except KeyError as e:
            logging.error(f"Erro: {e}, a chave {e} não foi encontrada no dicionário.")
        except Exception as e:
            logging.error(f"Erro: {e}, não foi possível concatenar os DataFrames.")